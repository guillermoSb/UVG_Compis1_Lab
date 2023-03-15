from Automata import Automata

def test_expand():
	# Arrange
	r = '(a|b)?b'
	# Act
	r = Automata._expand_regex(r)
	# Assert
	assert r == "((a|b)|ε).b.#"

def test_expand_2():
	# Arrange
	r = 'a?b'
	# Act
	r = Automata._expand_regex(r)
	# Assert
	assert r == "(a|ε).b.#"

def test_expand_3():
	# Arrange
	r = '(a|b)+abc?'
	# Act
	r = Automata._expand_regex(r)
	# Assert
	assert r == "(a|b).(a|b)*.a.b.(c|ε).#"

def test_expand_4():
	# Arrange
	r = 'a+b'
	# Act
	r = Automata._expand_regex(r)
	# Assert
	assert r == "a.a*.b.#"

def test_expand_5():
	# Arrange
	r = '(a(bc))+'
	# Act
	r = Automata._expand_regex(r)
	# Assert
	assert r == "(a.(b.c)).(a.(b.c))*.#"


def test_expand_6():
	# Arrange
	r = '(a(bc))?'
	# Act
	r = Automata._expand_regex(r)
	# Assert
	assert r == "((a.(b.c))|ε).#"