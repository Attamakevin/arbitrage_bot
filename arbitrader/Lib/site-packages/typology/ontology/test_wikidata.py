from typology.ontology import wikidata

def test_wikidata_properties():
    '''
    Test if we can define custom properties to them as dictionaries.
    After all, we want to index the real items of the world.
    '''

    Dog = wikidata.Concept('Q144')
    Cat = wikidata.Concept('Q146')

    # We want a dog with 4 legs, owned by Bob.
    dog = Dog({'legs': 4,
               'owner': 'Bob'})

    # We want a cat with 4 legs, owned by Alice.
    cat = Cat({'legs': 4,
               'owner': 'Alice'})

    assert dog.details == {'legs': 4, 'owner': 'Bob'}
    assert cat.details == {'legs': 4, 'owner': 'Alice'}

def test_wikidata_concepts_and_algebra():
    '''
    Test defining reality and desirity.

    #NOTE: Later, will move the concecpt algebra to general functionality, for all ontologies to have.
    '''

    Universe = wikidata.Concept('Q1')

    fact_universe = Universe({'gravitational constant': 6.67408e-11}, fact=True)
    goal_universe = Universe({'gravitational constant': 6.69408e-11})
    diff_universe = goal_universe - fact_universe

    assert fact_universe.sign == '.'
    assert goal_universe.sign == '*'
    assert diff_universe.details['gravitational constant'] == 1.9999999999999672e-13
