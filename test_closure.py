from Automata import Automata

def test_e_closure():
    # Arrange
    a = Automata._from_regex('b*')
    expected = (1,0,3)
    # Act
    closure_states = a.e_closure(1)
    
		# Assert
    assert len(closure_states) == 3
    for e in expected:
        assert e in closure_states
    
    
