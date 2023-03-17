from Automata import Automata


# Act
a = Automata._from_regex('(a|b)*a(a|b)(a|b)')
a = Automata._dfa_from_nfa(a)
a.minimize()
a.draw()
# print(tree.value)
# print(tree.right_child.value)

# print(tree.left_child.value)
# print(tree.left_child.right_child.value)


# print(tree.left_child.left_child.value)
# print(tree.left_child.left_child.right_child.value)

# print(tree.left_child.left_child.left_child.value)
# print(tree.left_child.left_child.left_child.right_child.value)

# print(tree.left_child.left_child.left_child.left_child.value)
# print(tree.left_child.left_child.left_child.left_child.followpos())






