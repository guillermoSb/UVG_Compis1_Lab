from Automata import Automata

def test_direct_dfa_1():
    # Arrange
		regex = 'ab'
		# Act
		a = Automata._from_regex_dfa(regex)
		
		# Assert
		assert a._states[0]['a'] == 1
		assert a._states[1]['b'] == 2
		assert len(a._states) == 3