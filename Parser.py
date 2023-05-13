

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
				self.non_terminals.insert(0, self.start)
				self.productions[self.start] = [self.start[0]]

class Parser():

	def __init__(self, grammar):
		grammar.augment()
		self.grammar = grammar

	def closure(self, items):
		j = items
		c = 0
		while c < 10:
			new_j = j
			for item in new_j:
				# Each item is a tuple (non_terminal, production_number, position)
				production = self.grammar.productions[item[0]][item[1]]
				if item[2] < len(production):
					next_symbol = production[item[2]]
					if next_symbol in self.grammar.non_terminals:
						for next_production in self.grammar.productions[next_symbol]:
							new_j = new_j.union({(next_symbol, self.grammar.productions[next_symbol].index(next_production), 0)})
				
				# for production in self.grammar.productions:
					
				# 	if production == production_head:
				# 		print("yay")
			
			if len(new_j) == len(j):
				break
			
			j = new_j
			
		return j


	@classmethod
	def _from_file(cls, file_name):
		file = open(file_name, 'r')
		terminals = []
		ignore = []
		non_terminals = []
		productions = {}

		can_read_tokens = True
		# Read the file line by line
		for line in file:
			line = line.strip()	# Remove leading and trailing whitespace			
			if line.startswith('%token') and can_read_tokens:
				terminals = terminals + line.split()[1:]
			elif line.startswith('IGNORE'):
				ignore = ignore + line.split()[1:]
			elif line == "%%":
				can_read_tokens = False
				break;
		
		# Read the file line by line again to read the productions
		is_making_production = False
		current_production = ''
		for line in file:
			line = line.strip()
			# Handle error: cannot declare token
			if line.startswith('%token'):
				raise Exception("[PARSER ERROR] Cannot declare token after %%")
			# Skip comments
			if line.startswith('/*'):
				continue
			if not is_making_production:
				for char in line:
					if char == ":":
						is_making_production = True
						productions[current_production] = []
						break
					current_production += char
			else:
				if line == ";":
					non_terminals.append(current_production)
					is_making_production = False
					current_production = ''
				else:
					if line.startswith('|'):
						line = line[1:]
						line = line.strip()
					productions[current_production].append(line)
		
		return Parser(Grammar(non_terminals, terminals, productions, list(productions.keys())[0]))

			


		


				
		

			
		
			
			
				
		
		

	

	

	
