from Lexer import Lexer


l = Lexer('yalex.txt')
l.replace_constructions()
l.draw_automata()