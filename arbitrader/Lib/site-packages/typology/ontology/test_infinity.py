from typology.ontology import infinity

def test_infinity_properties():
    '''
    Test if we can define custom properties to them as dictionaries.
    After all, we want to index the real items of the world.
    '''

    KeyEvent = infinity.Concept('GH:mindey/ooio/keylogger-event')
    Date = infinity.Concept('https://github.com/infamily/terms/wiki/date')

    # We want a keyevent with 4 legs, owned by Alice.
    key = KeyEvent({'legs': 4, 'owner': 'Alice'})

    # We want a date with 4 legs, owned by Bob.
    date = Date({'legs': 4, 'owner': 'Bob'})


    assert date.details == {'legs': 4, 'owner': 'Bob'}
    assert key.details == {'legs': 4, 'owner': 'Alice'}
