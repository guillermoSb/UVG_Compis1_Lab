from Lexer import Lexer
from Automata import Automata

l = Lexer('yalex2.txt')
a = l.create_automata()
a.draw()
# l.create_program()
