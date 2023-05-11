

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
		grammar.augment()
		self.grammar = grammar
	
	@classmethod
	def _from_file(cls, file_name):
		file = open(file_name, 'r')
		terminals = []
		ignore = []
		non_terminals = []
		productions = {}

		can_read_tokens = True
		token_line = None
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
					is_making_production = False
					current_production = ''
				else:
					if line.startswith('|'):
						line = line[1:]
						line = line.strip()
					productions[current_production].append(line)
		
		return Parser(Grammar(non_terminals, terminals, productions, list(productions.keys())[0]))

			


		


				
		

			
		
			
			
				
		
		

	

	

	
