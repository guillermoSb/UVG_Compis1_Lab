from Parser import Grammar, Parser

def test_grammar_augment():
    # Arrange 
		non_terminals = ['E', 'T', 'F']
		terminals = ['+', '*', '(', ')', 'id']
		productions = {
			'E': ['E+T', 'T'],
			'T': ['T*F', 'F'],
			'F': ['(E)', 'id']
		}
		# Act
		grammar = Grammar(non_terminals, terminals, productions, 'E')
		grammar.augment()
		# Assert
		assert grammar.start == 'E\''
		assert grammar.non_terminals == ['E\'', 'E', 'T', 'F']
		assert grammar.productions == {
			'E': ['E+T', 'T'],
			'T': ['T*F', 'F'],
			'F': ['(E)', 'id'],
			'E\'': ['E']
		}