# -*- coding: utf-8 -*-
import json
import requests
import copy
import metawiki
from hanziconv import HanziConv

BASE_URL = 'https://www.wikidata.org/w/api.php'

def get_json(wikidata_id):
    try:
        dicts = json.loads(
            requests.get(BASE_URL,
                params={'action': 'wbgetentities',
                        'ids': wikidata_id,
                        'format': 'json'}
            ).content)
        return dict(dicts, **{'success': True})
    except:
        return {'success': False}

def get_lang(d, languages=['en', 'zh', 'de', 'ru', 'fr', 'cn']):
    '''
    INPUT
    d :         dictionary with keys as language codes
    languages:  list of language codes in a priority descending order

    OUTPUT
    value of the first key that's available, or the first existing key,
    if none of the preferred languages are available

    EXAMPLE
    >>> get_lang({'en': 'love', 'zh': u'爱'})
    love
    '''
    for lang in languages:
        if d.get(lang):
            return d[lang]
    return d.values()[0]

def Concept(wikidata_id):

    '''
    INPUT
    The wikidata ID (str), or (dict). If there is no internet connection
    to WikiData API, you can simply pass a dict.

    OUTPUT
    class of WikiData type

    EXAMPLES

    >>> Dog1 = Concept('Q144')
    >>> Dog1
    <class asterisk.wikidata.Q144 at 0x7fc2b498c188>
    >>> Dog2 = Concept({'en': 'dog', 'lt': u'šuo'})
    >>> Dog2
    <class asterisk.wikidata.Q0 at 0x7fc2b43853f8>

    In the second case, the class is always of 'Q0' type, which does not
    correspond to any WikiData concept. However, objects derived from both
    types then have representations based on their languages. For example:

    >>> d1 = Dog1()
    >>> d1
    狗
    >>> d2 = Dog2()
    >>> d2
    šuo

    The derived objects can have different representations, and default
    languages are specified in .languages attribute, e.g.:

    >>> d2.languages
    ['lt', 'en']

    The value is returned in the order of .languages:

    >>> d2.set_langs(['en', 'lt'])
    >>> d2

    The first available language specified is returned, or if it is not
    available, the first available language is returned:

    >>> d1.set_langs([])
    >>> d1
    σκυλί

    The WikiData information about claims and aliases is available in
    .claims and .aliases respectively:

    >>> d1.aliases
    {u'el': [{u'value': u'\u03c3\u03ba\u03c5\u03bb\u03af', u'language': u'el'}...
    >>> d1.claims
    {u'P646': [{u'type': u'statement', u'references': [{u'snaks': {...
    >>> d2.aliases
    {'lt': [{'value': u'\u0161uo'}], 'en': [{'value': 'dog'}]}
    >>> d2.claims
    {}

    Additionally, each claim (property) is available as an attribute,
    for example 'Q189539' represents a loan,

    >>> Loan = Concept('Q189539')

    We can know that loans have qualitiy (P1552) of:

    >>> Loan.P1552
    interest rate
    lender
    issue date
    Term
    Collateral
    Debtor
    entity
    quantity

    The knowledge of qualities may allow us to formulate goals, and know
    in advance, what to look for in this type of things.

    Each property, in turn, can have nested information provided about
    itself in terms of P and Q values.

    We can create instances with details

    >>> l1 = Loan({'lender': 'John', 'debtor': 'Julia', 'amount': 1000})
    >>> l1
    préstamo ({'lender': 'John', 'debtor': 'Julia', 'amount': 1000})

    Now, we will later implement the method "save" to save the instances
    to general database as:

    >>> l1.save()

    This will allow to keep one database of any things. As described in the
    ``ai.py``, we could use several custom constructors to record the Goals
    and Facts about the world:

    >>> imaginary_loan = Loan.goal({'lender': 'John', 'debtor': 'Julia', 'amount': 1000})
    >>> actual_loan = Loan.fact({'lender': 'John', 'debtor': 'Julia', 'amount': 1000})

    Or:

    >>> Spaceship = Concept('Q40218')
    >>> imaginary_spaceship = Spaceship.goal({'tons to Low-Earth Orbit': 500})
    >>> existing_spaceship = Spaceship.fact({'tons to Low-Earth Orbit': 10})

    '''

    # Defining Classes Programmatically:
    # http://chimera.labs.oreilly.com/books/1230000000393/ch09.html#_defining_classes_programmatically

    if isinstance(wikidata_id, str):
        if wikidata_id.startswith('https://www.wikidata.org/wiki/'):
            wikidata_id = wikidata_id.rsplit('https://www.wikidata.org/wiki/')[-1]
        elif wikidata_id.startswith('WD:Q') or wikidata_id.startswith('WD:P'):
            wikidata_id = wikidata_id[3:]
        _concept = get_json(wikidata_id)
    elif isinstance(wikidata_id, dict):
        _concept = {'entities': {'Q0': {'aliases': {v:[{'value':wikidata_id[v], 'language': v}] for k,v in enumerate(wikidata_id)}, 'claims': {} }} }
        wikidata_id = 'Q0'
    else:
        return None

    _languages = _concept['entities'][wikidata_id]['aliases'].keys()
    _popular = ['en', 'es', 'de', 'fr', 'ru', 'zh', 'cn']
    _descriptions = _concept['entities'][wikidata_id]['descriptions']
    try:
        _alias = get_lang(_concept['entities'][wikidata_id]['aliases'], _popular)[0]['value']
    except:
        _alias = None

    _aliases = {}
    for k,v in enumerate(_concept['entities'][wikidata_id]['aliases']):
        L = _concept['entities'][wikidata_id]['aliases'][v]
        _aliases[v] = [l['value'] for l in L]

    _labels = {}
    for k,v in enumerate(_concept['entities'][wikidata_id]['labels']):
        L = _concept['entities'][wikidata_id]['labels'][v]
        _labels[v] = [L['value']]

    class Name(): pass

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

        self.aliases = self.__class__.concept['entities'][wikidata_id]['aliases']
        self.labels = self.__class__.concept['entities'][wikidata_id]['labels']
        self.claims = self.__class__.concept['entities'][wikidata_id]['claims']

    def _neg(self):
        return self

    def _set_langs(self, language_codes):
        '''
        INPUT
        languages a list of language codes, in order of priority to be displayed
        if exists

        OUTPUT
        sets the .alias, which is used in __repr__
        '''
        self.languages = language_codes
        self.alias = get_lang(self.aliases, self.languages)[0]['value']
        self.label = get_lang(self.labels, self.languages)['value']

    def _repr(self):
        if self.details:
            return ('%s%s (%s)' % (self.sign, self.alias, self.details)).encode('utf8')
        else:
            return ('%s%s' % (self.sign, self.alias)).encode('utf8')

    def _unicode(self):
        return '%s%s' % (self.sign, self.alias,)

    def _sub(self, other):
        result = copy.deepcopy(self)

        for key in other.details.keys():
            if key not in self.details.keys():
                result.details[key] = other.details[key]
            else:
                if hasattr(result.details[key], '__sub__'):
                    result.details[key] -= other.details[key]
                else:
                    if isinstance(self.details[key], str) :
                        result.details[key] = set([self.details[key]])-set([other.details[key]])

                    elif isinstance(self.details[key], tuple) or \
                         isinstance(self.details[key], list):
                        result[key] = set(self.details[key])-set(other.details[key])

        return result

    propositions = ''

    for key in _concept['entities'][wikidata_id]['claims'].keys():
        setattr(Name, key, _concept['entities'][wikidata_id]['claims'][key])
        for claim in _concept['entities'][wikidata_id]['claims'][key]:
            value = claim.get('mainsnak').get('datavalue')
            propositions += '%s : %s\n' % (key, value)

    qualities = ''
    HAS_QUALITY = 'P1552'

    if HAS_QUALITY in _concept['entities'][wikidata_id]['claims'].keys():
        for claim in _concept['entities'][wikidata_id]['claims'][HAS_QUALITY]:
            key = claim.get('mainsnak').get('datavalue').get('value').get('id')
            setattr(Name, key, claim.get('mainsnak'))
            qualities += '%s : %s\n' % (key, claim)

    _doc = """%s (%s)\n\nPropositions\n============\n%s\n\nQualities (P1552)\n=================\n%s""" % (wikidata_id, _aliases, propositions, qualities)

    _concept['aliases'] = copy.copy(_aliases)
    _concept['labels'] = copy.copy(_labels)
    _descriptions = {v: _descriptions[v]['value'] for k,v in enumerate(_descriptions)}
    _concept['descriptions'] = copy.copy(_descriptions)

    if 'cn' not in _aliases:
        if 'zh-cn' in _aliases:
            _aliases['cn'] = _aliases['zh-cn']
        elif 'zh-hans' in _aliases:
            _aliases['cn'] = _aliases['zh-hans']
        elif 'zh' in _aliases:
            _aliases['cn'] = [HanziConv.toSimplified(item) for item in _aliases['zh']]
        elif 'zh-hant' in _aliases:
            _aliases['cn'] = [HanziConv.toSimplified(item) for item in _aliases['zh-hant']]
        elif 'zh-hk' in _aliases:
            _aliases['cn'] = [HanziConv.toSimplified(item) for item in _aliases['zh-hk']]
        elif 'zh-mo' in _aliases:
            _aliases['cn'] = [HanziConv.toSimplified(item) for item in _aliases['zh-mo']]
        elif 'zh-my' in _aliases:
            _aliases['cn'] = [HanziConv.toSimplified(item) for item in _aliases['zh-my']]
        elif 'zh-sg' in _aliases:
            _aliases['cn'] = [HanziConv.toSimplified(item) for item in _aliases['zh-sg']]
        elif 'zh-tw' in _aliases:
            _aliases['cn'] = [HanziConv.toSimplified(item) for item in _aliases['zh-tw']]

    if 'cn' not in _labels:
        if 'zh-cn' in _labels:
            _labels['cn'] = _labels['zh-cn']
        elif 'zh-hans' in _labels:
            _labels['cn'] = _labels['zh-hans']
        elif 'zh' in _labels:
            _labels['cn'] = [HanziConv.toSimplified(item) for item in _labels['zh']]
        elif 'zh-hant' in _labels:
            _labels['cn'] = [HanziConv.toSimplified(item) for item in _labels['zh-hant']]
        elif 'zh-hk' in _labels:
            _labels['cn'] = [HanziConv.toSimplified(item) for item in _labels['zh-hk']]
        elif 'zh-mo' in _labels:
            _labels['cn'] = [HanziConv.toSimplified(item) for item in _labels['zh-mo']]
        elif 'zh-my' in _labels:
            _labels['cn'] = [HanziConv.toSimplified(item) for item in _labels['zh-my']]
        elif 'zh-sg' in _labels:
            _labels['cn'] = [HanziConv.toSimplified(item) for item in _labels['zh-sg']]
        elif 'zh-tw' in _labels:
            _labels['cn'] = [HanziConv.toSimplified(item) for item in _labels['zh-tw']]


    Name.__name__ = str(wikidata_id)
    Name.concept = _concept
    Name.__init__ = _init
    Name.__unicode__ = _unicode
    Name.__repr__ = _repr
    Name.set_langs = _set_langs
    Name.languages = _languages
    Name.descriptions = _descriptions
    Name.aliases = _labels
    Name.labels = _aliases
    Name.__doc__ =  _doc
    Name.__neg__ = _neg
    Name.__sub__ = _sub

    n = 'WD:'+Name.__name__
    Name.id = metawiki.url_to_name(n) if n.startswith('http') else n
    Name.url = metawiki.name_to_url(n) if not n.startswith('http') else n

    return Name

def Instance(wikidata_id):
    concept = Concept(wikidata_id)
    if concept:
        return concept()
    else:
        return None
