
from Automata import Automata

def test_postfix():
    # Arrange 
		infix = "a*|bc"
		# Act
		postfix = Automata._postfix_from_regex(infix)
		# Assert
		assert postfix == "a*bc.|"


def test_concat_ascii():
	# Arrange
	infix = "((045|054))054"
	# Act
	concatenated = Automata._add_concat_to_regex(infix, True)
	# Assert
	assert concatenated == "((045|054)).054"

def test_concat_ascii_2():
	# Arrange
	infix = "((045|054))054333"
	# Act
	concatenated = Automata._add_concat_to_regex(infix, True)
	# Assert
	assert concatenated == "((045|054)).054.333"

def test_concat_ascii_3():
	# Arrange
	infix = "((045|054))054333?"
	# Act
	concatenated = Automata._add_concat_to_regex(infix, True)
	# Assert
	assert concatenated == "((045|054)).054.333?"

def test_concat_ascii_3():
	# Arrange
	infix = "045?(048)+"
	# Act
	concatenated = Automata._add_concat_to_regex(infix, True)
	# Assert
	assert concatenated == "045?.(048)+"

def test_concat_ascii_4():
	# Arrange
	infix = "045?(048)*"
	# Act
	concatenated = Automata._add_concat_to_regex(infix, True)
	# Assert
	assert concatenated == "045?.(048)*"

def test_posfix_ascii():
	# Arrange
	infix = "045?(048)+"
	# Act
	postfix = Automata._postfix_from_regex(infix, True);
	# Assert
	assert postfix == "045?048+."
