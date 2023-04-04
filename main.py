from Automata import Automata


# ab*ab

a = Automata._from_regex_dfa('ab*ab*')


a.simulate('bbb')





