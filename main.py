from Automata import Automata


a = Automata._from_regex('(a|b)*abb')
a = Automata._dfa_from_nfa(a)
a.simulate('abb')
# a.draw()
