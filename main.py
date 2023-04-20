from Lexer import Lexer


l = Lexer('yalex2.txt')

automata = l.create_automata()
print(automata._final)