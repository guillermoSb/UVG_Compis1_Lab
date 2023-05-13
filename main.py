from Lexer import Lexer
from Parser import Parser
from Automata import Automata

# l = Lexer('yalex2.txt')
# # a = l.create_automata()
# # a.draw()
# l.create_program()

parser = Parser._from_file('yapar.txt')
print(parser.grammar.productions)
