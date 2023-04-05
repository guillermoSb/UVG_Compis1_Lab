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

def test_parse_token03():
	# Arrange
	lexer = Lexer()
	# Act
	token = lexer.parse_token('letra', "['a'-'d''A'-'D']")
	# Assert
	assert token.value == "(097|098|099|100|065|066|067|068)"

def test_parse_token04():
	# Arrange
	lexer = Lexer()
	# Act
	token = lexer.parse_token('letra', "['a'-'d''A'-'D''0'-'9']")
	# Assert
	assert token.value == "(097|098|099|100|065|066|067|068|048|049|050|051|052|053|054|055|056|057)"