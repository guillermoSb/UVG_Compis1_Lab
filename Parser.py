from graphviz import Digraph

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
							if (next_symbol, self.grammar.productions[next_symbol].index(next_production), 0) not in new_j:
								new_j = new_j.union({(next_symbol, self.grammar.productions[next_symbol].index(next_production), 0)})
			if len(new_j) == len(j):
				break
			
			j = new_j
			
		return j
	
	def go_to(self, items, symbol):
		j = set()
		for item in items:
			production = self.grammar.productions[item[0]][item[1]]
			if item[2] < len(production):
				next_symbol = production[item[2]]
				if next_symbol == symbol:
					j = j.union({(item[0], item[1], item[2] + 1)})
		return self.closure(j)
	
	def items(self):
		'''Generate the construct C'''
		start = self.closure({(self.grammar.start, 0, 0)})
		C = [self.closure({(self.grammar.start, 0, 0)})]
		transitions = {
			tuple(start): {}
		}
		while True:
			new_C = C
			for item_set in new_C:
				for symbol in self.grammar.non_terminals + self.grammar.terminals:
					go_to = self.go_to(item_set, symbol)
					if go_to is not None and len(go_to) > 0:
						if go_to not in new_C:
							new_C.append(go_to)
							if tuple(item_set) not in transitions:
								transitions[tuple(item_set)] = {}
							transitions[tuple(item_set)][symbol] = go_to
			if len(new_C) == len(C):
				break
			C = new_C

		return transitions, C

	def draw_automata(self):
		transitions, C = self.items();
		state_map = {}
		state_count = 0
		for state in C:
			state_map[tuple(state)] = state_count
			state_count += 1
		
		dot = Digraph(graph_attr={'rankdir': 'LR'})
		for state in C:
			dot.node('{}'.format(state_map[tuple(state)]), label=Parser._format_item_set(tuple(state), self.grammar), shape="box")
		for state in transitions:
			for transition in transitions[state]:
				dot.edge('{}'.format(state_map[tuple(state)]), '{}'.format(state_map[tuple(transitions[state][transition])]), label='{}'.format(transition))
		dot.render('automaton_lex.gv', view=True)
	
	@classmethod
	def _format_item_set(cls, item_set, grammar):
		item_format = ""
		for item in item_set:
			item_format +=  "{} -> ".format(item[0]) + " ".join(grammar.productions[item[0]][item[1]][:item[2]]) + " . " + " ".join(grammar.productions[item[0]][item[1]][item[2]:]) + "\n"
		return item_format

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

			


		


				
		

			
		
			
			
				
		
		

	

	

	
