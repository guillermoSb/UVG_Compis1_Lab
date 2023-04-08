from Lexer import Lexer
from Token import Token

def test_tokens():
	# Arrange and Act
	lexer = Lexer('yalex.txt')	
	# Assert
	assert len(lexer.tokens.keys()) == 6
	assert 'delimitador' in lexer.tokens.keys()
	assert 'identificador' in lexer.tokens.keys()
	assert 'numero' in lexer.tokens.keys()
	assert 'digito' in lexer.tokens.keys()
	assert 'letra' in lexer.tokens.keys()
	assert 'espacioEnBlanco' in lexer.tokens.keys()

def test_init():
	# Arrange and Act
	lexer = Lexer('yalex.txt')
	# Assert
	assert lexer.file != None
	assert lexer.text != None
	assert len(lexer.text) > 0

def test_from_yalex_01():
	# Arrange
	yalex = "['a'-'b''A'-'B']"
	# Act
	token = Token._from_yalex('letra', yalex)
	# Assert
	assert token.name == 'letra'
	assert token.value == '(097|098|065|066)'