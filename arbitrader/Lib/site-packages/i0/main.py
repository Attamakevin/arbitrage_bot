from i0 import settings, utils
import os
import metaform

import datetime
import PyRSS2Gen
from dateutil.parser import parse as dateparse


# ------- HTTP Server --------- #
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse


METADRIVE_DIR = os.path.expanduser(settings.BASE_DIR)
DATA_DIR =  os.path.join(METADRIVE_DIR, 'data')

app = FastAPI()

@app.get("/")
def read_root(request: Request):
    base_url = str(request.base_url).strip('/')
    return dict({'subscriptions': f'{base_url}/opml'}, **{it: {'interface': f'{base_url}/feed/{it}',
                 'primary_feed': f'{base_url}/feed/{it}/Post?format=rss'}
            for it in os.listdir(DATA_DIR)})

@app.get("/feed/{name}")
def read_types(request: Request, name: str, q: str = None):
    base_url = str(request.base_url).strip('/')
    types = os.listdir(f'{DATA_DIR}/{name}')
    return {it: f'{base_url}/feed/{name}/{it}' for it in types}

@app.get("/feed/{name}/{type}")
def read_feed(request: Request, type: str, name: str, q: str = None):

    base_url = str(request.base_url).strip('/')
    fnames = os.listdir(f'{DATA_DIR}/{name}/{type}')
    items = []
    for fname in fnames:
        item = metaform.load(os.path.join(f'{DATA_DIR}/{name}/{type}', fname))
        items.append(item)

    fmt = request.query_params.get('format')

    if fmt == 'rss':

        rss = PyRSS2Gen.RSS2(
            title = f'{name} / {type}',
            link = f'{base_url}/feed/{name}/{type}',
            description = '',
            lastBuildDate = datetime.datetime.utcnow(),
            items = [
                PyRSS2Gen.RSSItem(
                    title = item.get('title', ''),
                    link = item.get('link', ''),
                    description = item.get('summary', '') or item.get('description', ''),
                    guid = PyRSS2Gen.Guid(item.get('link', '')),
                    pubDate = dateparse(item.get('published', '2000-01-01')).astimezone(datetime.timezone.utc)
                )
                for item in items
            ]
        )

        text = rss.to_xml()

        return PlainTextResponse(text)

    return items

@app.get("/opml")
def read_opml(request: Request):
    base_url = str(request.base_url).strip('/')
    opml = '''<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
<head>
    <title>Feed Subscriptions</title>
</head>
<body>{text}
</body>
</opml>
'''
    line = '''  <outline text="{text}" title="{title}" type="rss"
    xmlUrl="{rss_url}" htmlUrl="{html_url}" entryContent="3"/>'''

    text = ''
    for it in os.listdir(DATA_DIR):
        text += '\n'+line.format(text=f'{it} / Post', title=f'{it} / Post', rss_url=f'{base_url}/feed/{it}/Post?format=rss', html_url=f'{base_url}/feed/{it}')

    return PlainTextResponse(opml.format(text=text), headers={'content-type': 'application/xml'})


# ------- CLI Launcher -------- #
import typer

cli = typer.Typer()

@cli.command()
def publish(path: str = '~/.metadrive', host: str = '0.0.0.0', port: str = '1111'):
    uvicorn.run("i0.main:app", host=host, port=port, log_level="info")

# ------- APP Cookiecutter -------- #
packmaker = typer.Typer()

@packmaker.command()
def package():
    print("What kind of driver you want to create?")
    print("[0] Generic, e.g., protocol-level: 0rss, 0imap, etc.")
    print("[1] Specific, e.g., app-level: 1twitter, 1airbnb, etc.")
    kind = input("Enter the number 0 or 1: ")

    print("What will be package name?")
    name = input("Name: ")

    if kind == '0':

        if not name.startswith('0'):
            print('Protocol driver package must start with "0". Try again.')
            return

        if name:
            utils.make_driver_template(name, from_package='0proto')

    elif kind == '1':

        if not name.startswith('1'):
            print('Protocol driver package must start with "1". Try again.')
            return

        if name:
            utils.make_driver_template(name, from_package='1app')
    else:
        print(f"You entered '{kind}', which is neither 0 nor 1. Closing. Try again.")
