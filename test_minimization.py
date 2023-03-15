from Automata import Automata

def test_minimization():
		# Arrange
		a = Automata._from_regex('(a|b)*abb')
		
		# Act
		dfa = Automata._dfa_from_nfa(a)
		# dfa.minimize()
		# Assert
		# assert len(dfa._states) == 4

def test_partition():
	# Arrange
	a = Automata._from_regex('(a|b)*abb')
	a = Automata._dfa_from_nfa(a)
	# Act
	partition = a.create_partiion((0,1,2,3), [(0,1,2,3), (4,)])
	# Assert
	assert len(partition) == 2
	assert partition[0] == (0,1,2)
	assert partition[1] == (3,)

def test_partition_2():
	# Arrange
	a = Automata._from_regex('(a|b)*abb')
	a = Automata._dfa_from_nfa(a)
	# Act
	partition = a.create_partiion((0,1,2), [(0,1,2), (3,), (4,)])
	# Assert
	assert len(partition) == 2