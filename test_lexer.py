from Lexer import Lexer

def test_parse_token01():
	# Arrange
	lexer = Lexer()
	# Act
	token = lexer.parse_token('numero', "['1''2''3']")
	# Assert
	assert token.value == "(049|050|051)"

def test_parse_token02():
	# Arrange
	lexer = Lexer()
	# Act
	token = lexer.parse_token('letra', "['a'-'d']")
	# Assert
	assert token.value == "(097|098|099|100)"