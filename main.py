from Automata import Automata


# Act
a = Automata._from_regex_dfa('ab*c')
# a.minimize()
# a.draw()
a.simulate('abbbcc')




