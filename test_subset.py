from Automata import Automata

def test_subset_state_count():
		# Arrange
		a = Automata._from_regex('b*')
		# Act
		dfa = Automata._dfa_from_nfa(a)
		# Assert
		print(dfa._states)
		assert dfa._type == "DFA"
		assert len(dfa._states) == 2