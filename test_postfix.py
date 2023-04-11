
from Automata import Automata

def test_postfix():
    # Arrange 
		infix = "a*|bc"
		# Act
		postfix = Automata._postfix_from_regex(infix)
		# Assert
		assert postfix == "a*bc.|"

def test_posfix_ascii():
	# Arrange
	infix = "045?(048)+"
	# Act
	postfix = Automata._postfix_from_regex(infix, True);
	# Assert
	print(postfix);
	assert False == True
