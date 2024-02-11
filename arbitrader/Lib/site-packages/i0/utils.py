import requests
import bs4
import os


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def make_driver_template(name, from_package):
    if from_package == '0proto':
        print("Assuming 0 - Driver for protocol resource.")
    elif from_package == '1app':
        print("Assuming 1 - Driver for app resource.")

    sources = bs4.BeautifulSoup(
        requests.get(f'https://pypi.org/simple/{from_package}/').content, 'html.parser')

    last = sources.find_all('a')[-1]

    # 1. Download: https://pypi.org/project/{from_package}/
    if is_downloadable(last.attrs['href']):
        r = requests.get(last.attrs['href'], allow_redirects=True)
        open(last.text, 'wb').write(r.content)

    # 2. Extract
        os.system(f'tar -xzvf {last.text}')
        os.system(f'rm {last.text}')
        folder = last.text.replace('.tar.gz','')
        os.system(f'mv {folder} {name}')
        version = folder.rsplit('-', 1)[-1]

    # 3. Find and replace
        os.system(f'rm {name}/PKG-INFO')
        os.system(f'rm {name}/setup.cfg')
        os.system(f'rm -rf {name}/{from_package}.egg-info')
        os.system(f'mv {name}/{from_package} {name}/{name}')
        os.system(f"sed -i 's/{from_package}/{name}/g' setup.py")
        # Renaming inside files
        os.system(f"sed -i 's/{from_package}/{name}/g' {name}/setup.py")
        os.system(f"sed -i 's/{version}/0.0.0/g' {name}/setup.py")
        os.system(f"sed -i 's/{from_package}/{name}/g' {name}/README.md")
        os.system(f"sed -i 's/{from_package}/{name}/g' {name}/{name}/main.py")
        with open(f'{name}/.gitignore', 'w') as f:
            f.write(f'''.env
*__pycache__*
dist
{name}.egg-info/''')
