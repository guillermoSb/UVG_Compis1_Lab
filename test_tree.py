from Automata import Automata

# Simple or
def test_tree_1():
	# Arrange
	regex = Automata._expand_regex('a|b')
	# Act
	tree = Automata._tree_from_regex(regex)
	# Assert
	assert tree.value == "."
	assert tree.right_child.value == "#"
	assert tree.left_child.value == "|"
	assert tree.left_child.right_child.value == "a"
	assert tree.left_child.left_child.value == "b"
	assert tree.parent == None

# Simple .
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
	assert tree.left_child.left_child.value == "."
	assert tree.left_child.left_child.right_child.value == "a"
	assert tree.left_child.left_child.right_child.is_leaf()
	assert tree.left_child.left_child.left_child == None
	assert tree.parent == None