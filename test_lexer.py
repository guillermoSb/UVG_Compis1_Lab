from Lexer import Lexer
from Token import Token
from Automata import Automata

def test_tokens():
	# Arrange and Act
	lexer = Lexer('yalex.txt')	
	# Assert
	assert len(lexer.tokens.keys()) == 7
	assert 'delimitador' in lexer.tokens.keys()
	assert 'identificador' in lexer.tokens.keys()
	assert 'numero' in lexer.tokens.keys()
	assert 'digito' in lexer.tokens.keys()
	assert 'letra' in lexer.tokens.keys()
	assert 'espacioEnBlanco' in lexer.tokens.keys()
	assert 'decimal' in lexer.tokens.keys()

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
	assert token.value == "('097'|'098'|'065'|'066')"

def test_from_yalex_02():
	# Arrange
	yalex = "['0'-'3''a''b']"
	# Act
	token = Token._from_yalex('digito', yalex)
	# Assert
	assert token.name == 'digito'
	assert token.value == "('048'|'049'|'050'|'051'|'097'|'098')"

def test_from_yalex_03():
	# Arrange
	yalex = "'-'?digito+"
	# Act
	token = Token._from_yalex('numero', yalex)
	# Assert
	assert token.name == 'numero'
	assert token.value == "'045'?digito+"


def test_from_yalex_04():
	# Arrange
	lexer = Lexer('yalex.txt')	
	# Assert
	print(lexer.tokens['decimal'].value)
	assert len(lexer.tokens.keys()) == 7
	assert lexer.tokens['numero'].value == "045?(048|049|050|051|052|053|054|055|056|057)+"

def test_create_automata_from_yalex():
	# Arrange
	lexer = Lexer('yalex.txt')	
	# Act
	automata = Automata._from_regex('045048', is_ascii=True)
	
	# Assert
	assert len(lexer.tokens.keys()) == 7
	assert lexer.tokens['numero'].value == "45?(048|049|050|051|052|053|054|055|056|057)+"
