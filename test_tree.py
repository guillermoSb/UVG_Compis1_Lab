from Automata import Automata

# Simple or
def test_tree_1():
	# Arrange
	regex = Automata._expand_regex('a.b.c')
	print(regex)
	# Act
	tree = Automata._tree_from_regex(regex)
	# Assert
	assert tree.value == "."
	
	assert tree.right_child.value == "#"
	assert tree.left_child.value == "."
	assert tree.left_child.right_child.value == "c"
	assert tree.left_child.left_child.value == "."
	assert tree.left_child.left_child.left_child.value == "a"
	assert tree.left_child.left_child.right_child.value == "b"
	assert tree.parent == None

#Simple .
def test_tree_2():
	# Arrange
	regex = Automata._expand_regex('ab')
	# Act
	tree = Automata._tree_from_regex(regex)
	# Assert
	assert tree.value == "."
	assert tree.right_child.value == "#"
	assert tree.left_child.value == "."
	assert tree.left_child.right_child.value == "b"
	assert tree.left_child.right_child.is_leaf()
	assert tree.left_child.left_child.value == "a"
	assert tree.parent == None

# Simple |
def test_simple_or():
	# Arrange
	regex = Automata._expand_regex('a|b')
	# Act
	tree = Automata._tree_from_regex(regex)
	# Assert
	assert tree.value == "."
	assert tree.right_child.value == "#"
	assert tree.left_child.value == "|"
	assert tree.left_child.right_child.value == "b"
	assert tree.left_child.left_child.value == "a"
	assert tree.parent == None



# Simple *
def test_tree_3():
	# Arrange
	regex = Automata._expand_regex('ab*')
	# Act
	tree = Automata._tree_from_regex(regex)
	# Assert
	assert tree.value == "."
	assert tree.right_child.value == "#"
	assert tree.left_child.value == "."
	assert tree.left_child.left_child.value == "a"
	assert tree.left_child.right_child.value == "*"
	assert tree.left_child.right_child.left_child.value == "b"
	
	# assert tree.left_child.left_child.value == "a"
	
	assert tree.parent == None


def test_tree_4():
	# Arrange
	regex = ('(a|ε).#')
	# Act
	tree = Automata._tree_from_regex(regex)
	# Assert
	
	assert tree.value == "."
	assert tree.right_child.value == "#"
	assert tree.left_child.value == "|"
	assert tree.left_child.left_child.value == "a"
	assert tree.left_child.right_child.value == "ε"