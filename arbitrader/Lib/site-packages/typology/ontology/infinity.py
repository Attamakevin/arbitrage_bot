# -*- coding: utf-8 -*-
import metawiki
import requests
import json
import bs4
import yaml
import mistune


from .wikidata import get_lang


def Concept(infinity_uri):

    infinity_uri = metawiki.name_to_url(infinity_uri)

    if isinstance(infinity_uri, str):
        _concept = get_concept(infinity_uri)

    elif isinstance(infinity_uri, dict):
        # Example.
        _concept = {
            'aliases':
                {'en': ['one','two','three'],
                 'lt': ['vien', 'du', 'try']},
            'descriptions': {
                'en': 'number',
                'lt': 'skaicius'},
            'claims': {},
            'formats': {},
            'references': []
        }

    else:
        return

    try:
        _alias = _concept['aliases'][
            list(_concept['aliases'].keys())[0]
        ][0]
    except:
        _alias = "Undefined"


    def _init(self, details={}, fact=False):
        self.details = details
        self.fact = fact
        if self.fact:
            self.sign = '.'
        else:
            self.sign = '*'

        try:
            self.alias = _alias
        except:
            self.alias = None

    def _repr(self):
        if self.details:
            return '{}{} ({})'.format(c.sign, c.alias, c.details)

        else:
            return '{}{}'.format(self.sign, self.alias)

    def _unicode(self):
        return '%s%s' % (self.sign, self.alias,)



    class Name(): pass

    n = str(infinity_uri)
    Name.concept = _concept
    Name.aliases = _concept.get('aliases')
    Name.descriptions = _concept.get('descriptions')
    Name.__name__ = n
    Name.__init__ = _init
    Name.__repr__ = _repr
    Name.__unicode__ = _unicode
    Name.id = metawiki.url_to_name(n) if n.startswith('http') else n
    Name.url = metawiki.name_to_url(n) if not n.startswith('http') else n


    return Name


def get_concept(path):
    '''
    Retrieves concept from a wiki page.

    :path: web url or location of file on disk

    For example:

    >>> get_concept('./wiki/percent_change.md')

    >>> get_concept('https://github.com/infamily/infinity-db/blob/master/wiki/percent_change.md#1hourly')
    '''

    page = get_source(path)

    soup = bs4.BeautifulSoup(
        mistune.markdown(page),
        'html.parser')

    target = soup.find(
        'code', {'class': 'lang-yaml'})

    concept = yaml.load(target.text, Loader=yaml.FullLoader)

    headers = soup.find_all('h2')

    formats = {}

    for header in headers:
        content = header.find_next_sibling()

        target = content.find(
            'code', {'class': 'lang-yaml'})

        if target:
            formats[header.text] = yaml.load(target.text, Loader=yaml.FullLoader)

    if concept:
        if formats:
            concept['formats'] = formats
        return concept


def get_source(path):
    if str(path).startswith('https://github.com/'):
        path = path.replace(
            'https://github.com/',
            'https://raw.githubusercontent.com/'
        ).replace('/blob/', '/')

        # GitHub has just changed:
        # X https://raw.githubusercontent.com/user/repo/wiki/title#anchor
        # O https://raw.githubusercontent.com/wiki/user/repo/title.md#1hourly
        # Is Microsoft trying to unify repos to better understand all code on GH?

        if path.startswith('https://raw.githubusercontent.com/'):
            if '/wiki/' in path:
                path = '/'.join(path.split('/wiki/'))
                path = path.replace(
                    'https://raw.githubusercontent.com/',
                    'https://raw.githubusercontent.com/wiki/'
                )
                if '#' in path:
                    # Affix .md
                    path = path.replace('#', '.md#')

                elif not path.endswith('.md'):
                    path += '.md'


    if str(path).startswith('http'):
        page = requests.get(path).content.decode("utf-8")
    else:
        page = open(path,'r').read()

    return page
