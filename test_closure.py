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

def test_e_closure_t():
		# Arrange
		a = Automata._from_regex('b*')
		expected = (1,2,0,3)
		# Act
		e_closure_t = a.e_closure_t((1,2))
		# Assert
		assert len(e_closure_t) == len(expected)
		for e in expected:
				assert e in e_closure_t
