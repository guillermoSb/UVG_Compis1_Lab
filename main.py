from Automata import Automata


# ab*ab

a = Automata._from_regex('(054|045|041|034)011*', is_ascii=True)


a.draw()





