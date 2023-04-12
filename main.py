from Lexer import Lexer


l = Lexer('yalex2.txt')
l.replace_constructions()
l.draw_automata()