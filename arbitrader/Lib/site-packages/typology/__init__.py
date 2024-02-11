from .ontology.infinity import Concept as InfinityConcept
from .ontology.wikidata import Concept as WikidataConcept
# Later combine other ontologies

def Concept(s):
    if s.startswith('WD:') or s.startswith('https://www.wikidata.org'):
        return WikidataConcept(s)
    else:
        return InfinityConcept(s)
