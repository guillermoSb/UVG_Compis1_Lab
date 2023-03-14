import pytest

from Automata import Automata


def test_dfa_simulation_accept():
    # Arrange
		a = Automata._from_regex('(a|b)*abb')
		a = Automata._dfa_from_nfa(a)
		# Act
		ok = a.simulate('abb')
		# Assert
		assert ok == True

def test_dfa_simulation_accept_2():
    # Arrange
		a = Automata._from_regex('(a|b)*abb')
		a = Automata._dfa_from_nfa(a)
		# Act
		ok = a.simulate('abbaaaaaabbbbbbbbbbaababababbaabbaabb')
		# Assert
		assert ok == True



def test_ndfa_simulation_accept():
    # Arrange
		a = Automata._from_regex('(a|b)*abb')
		# Act
		ok = a.simulate('abb')
		# Assert
		assert ok == True

def test_ndfa_simulation_accept_2():
    # Arrange
		a = Automata._from_regex('(a|b)*abb')
		# Act
		ok = a.simulate('abbaaaaaabbbbbbbbbbaababababbaabbaabb')
		# Assert
		assert ok == True



