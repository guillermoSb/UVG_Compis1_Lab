import pytest

from Automata import Automata


def test_dfa_simulation_accept():
    # Arrange
		a = Automata._from_regex('(a|b)*abb')
		a = Automata._dfa_from_nfa(a)
		# Act
		state = a.simulate('abb')
		# Assert
		
		assert state == a._final[0]

def test_dfa_simulation_accept_2():
    # Arrange
		a = Automata._from_regex('(a|b)*abb')
		a = Automata._dfa_from_nfa(a)
		# Act
		state = a.simulate('abbaaaaaabbbbbbbbbbaababababbaabbaabb')
		# Assert
		assert state in a._final



def test_ndfa_simulation_accept():
    # Arrange
		a = Automata._from_regex('(a|b)*abb')
		# Act
		states = a.simulate('abb')
		
		# Assert
		assert a._final in states

def test_ndfa_simulation_accept_2():
    # Arrange
		a = Automata._from_regex('(a|b)*abb')
		# Act
		states = a.simulate('abbaaaaaabbbbbbbbbbaababababbaabbaabb')
		# Assert
		assert a._final in states






