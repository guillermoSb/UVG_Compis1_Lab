from Automata import Automata

def test_minimization():
		# Arrange
		a = Automata._from_regex('(a|b)*abb')
		# Act
		dfa = Automata._dfa_from_nfa(a)
		# dfa.minimize()
		# Assert
		# assert len(dfa._states) == 4