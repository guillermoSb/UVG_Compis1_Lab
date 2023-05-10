

class Grammar():
		'''A Grammar is used to define a language'''
		def __init__(self, non_terminals, terminals, productions, start):
				self.non_terminals = non_terminals
				self.terminals = terminals
				self.productions = productions
				self.start = start

		def augment(self):
				'''Augment the grammar'''
				self.start = self.start + "'"
				self.non_terminals.append(self.start)
				self.productions[self.start] = [self.start[0]]

class Parser():
	def __init__(self, grammar):
		'''A Parser is used to parse a language. It takes a grammar as input and provides a parse method.'''
		self.grammar = grammar

	

	
