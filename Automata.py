from graphviz import Digraph
from Node import Node


class Automata:
		
		# Define precedences for regex operators
		operators = {
			'*': 1,
			'+': 1,
			'?': 1,
			'.': 2,
			'|': 3
		}

		
		# Initializers


		def __init__(self, states, initial, final, symbols, type = 'NFA'):
				"""Constructor for the Automata class"""				
				self._states = states
				self._initial = initial
				self._final = final
				self._type = type
				self._symbols = symbols


		
		# Instance methods


		def e_closure(self, s):
			"""Set of NFA states that are reachable from state s on epsilon transitions"""
			return self.e_closure_t((s,))
		

		def e_closure_t(self, T):
			"""Set of NFA states reachable from any s state in T on epsilon transitions"""
			e_closure_t = T
			state_stack = list(T)
			while len(state_stack) > 0:
				t = state_stack.pop()
				if 'ε' in self._states[t].keys():
					for u in self._states[t]['ε']:
						if u not in e_closure_t:
							e_closure_t += (u,)
							state_stack.append(u)
			return e_closure_t
		
		def move(self,T,a):
			"""Set of NFA states that can be reached from any state in T using the symbol a"""
			reachable_states = ()

			for t in T:
				if a in self._states[t].keys():
					reachable_states += self._states[t][a]
			return reachable_states
		

		def draw(self):
			"""Draws an automaton diagram"""
			# create a new directed graph
			dot = Digraph(graph_attr={'rankdir': 'LR'})
			if self._type == 'NFA':
				# add nodes to the graph
				for state in self._states.keys():
						if state == self._final:          
									dot.node('{}'.format(state), shape="doublecircle")
						elif  state == self._initial:          
									dot.node('{}'.format(state), shape="triangle")
						else:
									dot.node('{}'.format(state),)

				for state in self._states.keys():
						for transition in self._states[state]:
										for to in self._states[state][transition]:
														dot.edge('{}'.format(state), '{}'.format(to), label=transition)
			elif self._type == 'DFA':
				# add nodes to the graph
				for state in self._states.keys():
						if state in self._final:          
									dot.node('{}'.format(state), shape="doublecircle")
						elif  state == self._initial:          
									dot.node('{}'.format(state), shape="triangle")
						else:
									dot.node('{}'.format(state),)

				for state in self._states.keys():
						for transition in self._states[state]:
							to = self._states[state][transition]
							dot.edge('{}'.format(state), '{}'.format(to), label=transition)

			dot.render('automaton.gv', view=True)

		
		def simulate(self, input):
			"""Simulates an Automaton"""
			if self._type == 'DFA':
				current_state = self._initial
				for s in input:
					# Check if s is on the symbol list
					if s not in self._symbols:
						raise Exception("[Simulation Error] - {} is not on symbol list.".format(s))
					if s not in self._states[current_state]:
						raise Exception("[Simulation Error] - {} was not accepted.".format(input))
					current_state = self._states[current_state][s]
				# Check if the final state is on the final states
				if current_state not in self._final:
					raise Exception("[Simulation Error] - {} was not accepted.".format(input))
				else:
					return True
			else:
				S = self.e_closure(self._initial)
				i = 0
				while i != len(input):
					if input[i] not in self._symbols:
						raise Exception("[Simulation Error] - {} is not on symbol list.".format(input[i]))
					S = self.e_closure_t(self.move(S, input[i]))
					i += 1
				if len(set(S).intersection({self._final})) > 0:
					return True
				else:
					raise Exception("[Simulation Error] - {} was not accepted.".format(input))
				

		def minimize(self):
			F = []
			NF = []
			for final_state in self._final:
				F.append(final_state)
			for state in self._states.keys():
				if state not in F:
					NF.append(state)
			partition = [tuple(F), tuple(NF)]
			new_partition = [tuple(F.copy()), tuple(NF.copy())]	# List of sets of tuples
		
			while  True:
				for group in partition:
					if len(group) == 1:
						continue
					new_group = self.create_partiion(group, partition.copy())
					
					if len(new_group[1]) == 0:
						continue
					idx = new_partition.index(group)
					del new_partition[idx]
					for g in new_group:
						new_partition.append(g)
				
				if partition == new_partition:
					break
				partition = new_partition
			
			# Create the states
			for group in partition:
				if len(group) == 1:
					continue
				representative = group[0]
				for i in range(1, len(group)):
					del self._states[group[i]]
					for s in self._states.keys():
						for a in self._symbols:
							if self._states[s][a] == group[i]:
								self._states[s][a] = representative
				
			dead_states = []
			for state in self._states:
				if len(set(self._states[state].values())) == 1 and list(self._states[state].values())[0] == state and state not in self._final:
					dead_states.append(state)
			for state in dead_states:
				for k in self._states:
					for s in self._symbols:
						if self._states[k][s] == state:
							del self._states[k][s]
				
				del self._states[state]
		

		def create_partiion(self, group, groups):
			# Partition group in subgroups
			distringuishable = {}
			for s in group:
					for t in group:
						for a in self._symbols:
							dest_s = self._states[s][a]
							dest_t = self._states[t][a]
							# Find if the destinations fall on the same group
							for i in range(0, len(groups)):
								if dest_s in groups[i]:
									dest_s_group = i
								if dest_t in groups[i]:
									dest_t_group = i
							if dest_s_group != dest_t_group:
								distringuishable[(s,t)] = True
								break
						if (s,t) not in distringuishable:
							distringuishable[(s,t)] = False

			# Build the groups
			new_groups = []
			for pair in distringuishable.keys():
				s, t = pair
				if distringuishable[pair]:
					if len(new_groups) == 0:
						new_groups.append(tuple())
						new_groups.append(tuple())
					if t not in new_groups[1] and t not in new_groups[0]:
						new_groups[1] = new_groups[1] + (t,)
				else:
					if len(new_groups) == 0:
						new_groups.append(tuple())
						new_groups.append(tuple())
					if s not in new_groups[1] and s not in new_groups[0]:
						new_groups[0] = new_groups[0] + (s,)
					if t not in new_groups[1] and t not in new_groups[0]:
						new_groups[0] = new_groups[0] + (t,)
			
			return new_groups
						

		# Class Methods

		@classmethod
		def _group_for_item(self, groups, item):
			for g in groups:
				if tuple(item) in g:
					return g
		
		@classmethod
		def _dfa_from_nfa(self, nfa):
			# Validate correct type of automaton
			if nfa._type != 'NFA':
				raise Exception("[NFA ERROR] The input for this method should be a NFA Automaton.")
			d_transitions = {}	# DFA transitions will be stored here
			d_states_unmarked = [nfa.e_closure(nfa._initial),]
			d_states_marked = []

			counter = 0
			labels = {}
			labels[tuple(sorted(d_states_unmarked[0]))] = counter
			counter += 1
			final_states = []
			nfa._symbols = tuple(set(nfa._symbols).difference({'ε'}))
			while len(d_states_unmarked) > 0:
				# Mark the new state
				d_state = tuple(sorted(d_states_unmarked.pop()))
				if set(d_state) not in d_states_marked:
					d_states_marked.append(set(d_state))
				for input in nfa._symbols:
					U = set(nfa.e_closure_t(nfa.move(d_state, input)))
					if tuple(sorted(U)) not in labels:
						labels[tuple(sorted(U))] = counter
						counter += 1
					if U not in d_states_marked:
						d_states_unmarked.append(tuple(U))
					if labels[d_state] not in d_transitions:
						d_transitions[labels[d_state]] = {}
					d_transitions[labels[d_state]] = {
							**d_transitions[labels[d_state]],
							input: labels[tuple(sorted(U))]
					}
			for state in d_states_marked:
				counter += 1
				if nfa._final in state:
					final_states.append(labels[tuple(sorted(state))])
			return Automata(d_transitions, 0, final_states, nfa._symbols, 'DFA')
			
		
		@classmethod
		def _from_regex(self, regex, is_ascii = False):		
				"""Creates an Automata from a regex"""
				self._regex = regex.replace(' ', '')	# Remove spaces from the regex
				self._check_regex(regex)	# Check that the regex is valid
				self._postfix = self._postfix_from_regex(regex, is_ascii)	# Convert the regex to postfix
				return self._states_from_postfix(self._postfix, is_ascii)	# Create the states for the automaton


		@classmethod
		def _expand_regex(self, regex):
			"""Expands a regex"""
			regex = self._add_concat_to_regex(regex)
			regex = list(regex)
			new_regex = []
			for i in range(0, len(regex)):
				# Implement the ? identity
				if regex[i] == "?":
					# Check if the prev char is not a )
					if regex[i - 1] != ")":
						operand = new_regex.pop(len(new_regex) - 1)
						new_regex += "({}|ε)".format(operand)
					else:
						operand = []
						j = i - 1
						count = 0
						while True:
							operand.insert(0, regex[j])
							if regex[j] == ")":
								count += 1
							elif regex[j] == "(":
								count -= 1
							j -= 1
							if count == 0:
								break
						end = len(new_regex)
						start = len(new_regex) - 1
						count = 0
						while True:
							if regex[start] == ")":
								count += 1
							elif regex[start] == "(":
								count -= 1
							if count == 0:
								break
							start -= 1
						del new_regex[start: end + 1]
						operand = ''.join(operand)
						new_regex.append("({}|ε)".format(operand))
				elif regex[i] == "+":
					# Check if the prev char is not a )
					if regex[i - 1] != ")":
						operand = new_regex.pop(len(new_regex) - 1)
						new_regex += "{}.{}*".format(operand, operand)
					else:
						operand = []
						j = i - 1
						count = 0
						while True:
							operand.insert(0, regex[j])
							if regex[j] == ")":
								count += 1
							elif regex[j] == "(":
								count -= 1
							j -= 1
							if count == 0:
								break
							
						end = len(new_regex)
						start = len(new_regex) - 1
						count = 0
						while True:
							
							if regex[start] == ")":
								count += 1
							elif regex[start] == "(":
								count -= 1
							if count == 0:
								break
							start -= 1
						del new_regex[start: end + 1]
						del new_regex[start: end + 1]
						operand = ''.join(operand)
						new_regex += "{}.{}*".format(operand, operand)
				else:
					new_regex.append(regex[i])
			new_regex.insert(0, '(')
			new_regex.append(').#')
			return ''.join(new_regex)




		@classmethod
		def _from_regex_dfa(self, regex):
			"""Creates a DFA automata from a regex"""
			self._regex = regex.replace(' ', '')	# Remove spaces from the regex
			self._check_regex(regex)	# Check that the regex is valid
			# 1. Expand regex
			self._regex = self._expand_regex(self._regex)
			# 2. Build syntax tree
			tree, nodes = Automata._tree_from_regex(self._regex)
			label_values = {}
			followpos = {}
			for n in nodes:
				if n.label is not None:
					label_values[n.label] = n.value
				if n.value in ['.', '*']:
					nodefollowpos = n.followpos()
					for k in nodefollowpos:
							if k not in followpos:
								followpos[k] = tuple()
							followpos[k] = tuple(sorted(followpos[k] + nodefollowpos[k]))
			
			followpos[len(label_values) - 1] = tuple()
			# Create transition table
			key_counter = 0
			keys = {():len(label_values) - 1}
			d_states = {} # Key<int> value {Key<string>, value <int>}	
			keys[tree.firstpos()] = key_counter
			key_counter += 1
			unsearched = [tree.firstpos()]
			marked = []
			final_states = tuple()

			while len(unsearched) > 0:
				item = tuple(sorted(unsearched.pop()))
				marked.append(item)
				# Create a new states
				for s in set(label_values.values()):
					add_state = False
					if s == "#":
						continue
					new_state = tuple()
					add_state = False
					for k in item:
						if s in label_values[k]:
							add_state = True
							new_state += followpos[k]
					if new_state not in marked and len(new_state) > 0:
						keys[new_state] = key_counter
						key_counter += 1
						unsearched.append(new_state)
					if keys[item] not in d_states:
						marked.append(item)
						d_states[keys[item]] = {}
						if len(label_values) - 1 in item:
							final_states += (keys[item],)
					if add_state:
						d_states[keys[item]][s]	= keys[new_state]
			
			symbols = set(label_values.values()).difference({'#',})
			return Automata(d_states, 0, final_states, symbols, 'DFA')
		
		@classmethod
		def _tree_from_regex(cls, regex):
			"""Creates a tree from a given regex"""
			# 1. Create the root
			root = Node(None, None, None, None)
			nodes = []
			# 2. Iterate on the regex
			current_node = root
			leaf_counter = 0
			nodes.append(current_node)
			for a in regex:
				if a == '(':
					group = Node(None,None,None,None)
					current_node.left_child = group
					group.parent = current_node
					current_node = group
					nodes.append(group)
				elif a == ')':
					if current_node.value is None and current_node.right_child is None and current_node.left_child.value is not None and current_node.left_child.value is not ['|', '.', '*', '(', ')']:
						current_node.value = current_node.left_child.value
						current_node.label = current_node.left_child.label
						idx = nodes.index(current_node.left_child)
						nodes.pop(idx)
						current_node.left_child = None
					elif current_node.value is None:
						current_node.value = '.'
					
					current_node = current_node.parent
					
				elif a == '.' or a == '|':
					if current_node.value == a:
						# Reparenting
						node = Node(current_node, None, a, current_node.parent)
						nodes.append(node)
						current_node.parent.left_child = node
						current_node.parent = node
						current_node = node
					else:
						current_node.value = a

				elif a == '*':
					# Wrap the current node with a *
					if current_node.value:
						node = Node(None, None, a, current_node)
						nodes.append(node)
						# Wrap the right child of the current node
						to_wrap = current_node.right_child
						node.left_child = to_wrap
						to_wrap.parent = node
						current_node.right_child = node
					elif current_node.left_child.value:
						node = Node(None, None, a, current_node)
						nodes.append(node)
						to_wrap = current_node.left_child
						node.left_child = to_wrap
						to_wrap.parent = node
						current_node.left_child = node	
				elif a not in cls.operators.keys() and a not in ['(', ')']:
					node = Node(None,None, a, None)
					nodes.append(node)
					node.label = leaf_counter
					leaf_counter += 1
					if current_node.left_child is None:
						# If the current node left child is empty
						current_node.left_child = node
						node.parent = current_node
					elif current_node.value in ['.', '|']:
						# If the left child is not empty and the current node has a .
						current_node.right_child = node
						node.parent = current_node
			return current_node, nodes
		
		
		@classmethod
		def _check_regex(cls, regex):
			"""Checks that the regex is valid, throws an error if invalid."""
			# Check that the regex has the same number of opening and closing parentheses
			if regex.count('(') != regex.count(')'):
				raise Exception("[REGEX ERROR] The regex has a different number of opening and closing parentheses.")
			
			# Check that there are no two operators in a row
			for i in range(0, len(regex)):
				if regex[i] == "#":
					raise Exception("[REGEX ERROR] Operator # is not allowed.")			
				if regex[i] in cls.operators.keys() and i < len(regex) - 1:
					if regex[i+1] in ['*', '?', '+']:
						raise Exception("[REGEX ERROR] There are two operators in a row.")			
			
			# The last character of the regex cannot be an | operator
			if regex[-1] in ['|']:
				raise Exception("[REGEX ERROR] The last character of the regex cannot be the | operator.")
			
			# The first character of the regex cannot be an | operator
			if regex[0] in cls.operators:
				raise Exception("[REGEX ERROR] The first character of the regex cannot be an operator.")

			# The first character of the regex cannot be an uniary operator
			if regex[0] in ['*', '?', '+']:
				raise Exception("[REGEX ERROR] The first character of the regex cannot be an uniary operator.")
				

		@classmethod
		def _states_from_postfix(cls, postfix, is_ascii=False):
			"""Creates the staes for the automata from a postfix expression"""
			state_counter = 0
			print("Posfix is", postfix)
			if not is_ascii:
				postfix_stack = list(postfix)
			else:
				postfix_stack = []	
				i = 0
				while i < len(postfix):
					if postfix[i] not in ['|', '(', ')', '?', '*', '.']:
						postfix_stack.append(postfix[i:i+3])
						i += 3			
					else:
						postfix_stack.append(postfix[i])
						i += 1
			
			operation_stack = []
			print("POSFIX STACK IS: ", postfix_stack)
			while len(postfix_stack) > 0:
				token = postfix_stack.pop(0)
				if token in cls.operators.keys():
					if token == "*":
						operand = operation_stack.pop()
						new_states = {
									**operand._states, # Append the previous states
						}
						# Create two new states
						start_state = state_counter
						end_state = state_counter + 1
						# Create the transitions between the new states
						new_states[start_state] = {'ε': (operand._initial, end_state)}
						new_states[end_state] = {}
						# Keep epsilon transitions from the previous final state
						if 'ε' in operand._states[operand._final].keys():
							prev_transitions = operand._states[operand._final]['ε']
						else:
							prev_transitions = tuple()
						
						new_transitions = prev_transitions + (operand._initial, end_state)
						# Add the new epsilon transition to the final state
						new_states[operand._final] = {
							**new_states[operand._final],
							**{'ε': new_transitions}
						}
						state_counter += 2
						operation_stack.append(Automata(new_states, start_state, end_state, operand._symbols))
					elif token == "+":
						operand = operation_stack.pop()	
						new_states = {
									**operand._states, # Append the previous states
						}
						# Create the new states
						start_state = state_counter
						end_state = state_counter + 1
						# Cerate the epsilon transition between the start state and the initial state
						new_states[start_state] = {'ε': (operand._initial,)}
						new_states[end_state] = {}
						if 'ε' in operand._states[operand._final].keys():
							prev_transitions = operand._states[operand._final]['ε']
						else:
							prev_transitions = tuple()
						
						# Add an epsilon transition that goes from the initial state to the end state
						new_transitions = prev_transitions + (operand._initial, end_state)
						
						new_states[operand._final] = {
							**new_states[operand._final],
							**{'ε': new_transitions}
						}
						state_counter += 2

						operation_stack.append(Automata(new_states, start_state, end_state, operand._symbols))
					elif token == ".":
						operand_2 = operation_stack.pop()
						operand_1 = operation_stack.pop()
						# Keep the operands states
						new_states = {
									**operand_1._states,
									**operand_2._states,
						}
						# End state of operand 1 connects to start state of operand 2
						new_states[operand_1._final] = {'ε': (operand_2._initial,)}

						operation_stack.append(Automata(new_states, operand_1._initial, operand_2._final, operand_1._symbols.union(operand_2._symbols)))
					elif token == "?":
						operand_1 = operation_stack.pop()
						# Keep the operands states
						new_states = {
									**operand_1._states,
						}
						# Create the new states
						start_state = state_counter
						end_state = state_counter + 1
						# Create the epsilon transitions between the new states - the initial state can go to the end state
						new_states[start_state] = {'ε': (operand_1._initial, end_state)}
						new_states[end_state] = {}
						# Keep epsilon transitions from the previous final state
						if 'ε' in operand_1._states[operand_1._final].keys():
							prev_transitions_1 = operand_1._states[operand_1._final]['ε']
						else:
							prev_transitions_1 = tuple()
						new_states[operand_1._final] = {
							**new_states[operand_1._final],
							**{'ε': (end_state,) + prev_transitions_1}
						}
						state_counter += 2
						operation_stack.append(Automata(new_states, start_state, end_state, operand_1._symbols))	
					elif token == "|":
						operand_2 = operation_stack.pop()
						operand_1 = operation_stack.pop()
						# Keep the operands states
						new_states = {
									**operand_1._states,
									**operand_2._states,
						}
						# Create the new states
						start_state = state_counter
						end_state = state_counter + 1
						# Create the epsilon transitions between the new states
						new_states[start_state] = {'ε': (operand_1._initial, operand_2._initial)}
						new_states[end_state] = {}
						# Keep epsilon transitions
						if 'ε' in operand_1._states[operand_1._final].keys():
							prev_transitions_1 = operand_1._states[operand_1._final]['ε']
						else:
							prev_transitions_1 = tuple()
						# Keep epsilon transitions
						if 'ε' in operand_2._states[operand_2._final].keys():
							prev_transitions_2 = operand_2._states[operand_2._final]['ε']
						else:
							prev_transitions_2 = tuple()
						# Add the new epsilon transitions
						new_states[operand_1._final] = {
							**new_states[operand_1._final],
							**{'ε': (end_state,) + prev_transitions_1}
						}
						new_states[operand_2._final] = {
							**new_states[operand_2._final],
							**{'ε': (end_state,) + prev_transitions_2}
						}
						state_counter += 2
						operation_stack.append(Automata(new_states, start_state, end_state, operand_1._symbols.union(operand_2._symbols)))	
				else:
					# Append a base Automata to the operation stack, this state has two initial states with a connection between them
					operation_stack.append(Automata({state_counter: {token: (state_counter + 1,)}, state_counter + 1: {}}, state_counter, state_counter + 1, {token,}))
					
					state_counter += 2
			
			return operation_stack[0]
		


		@classmethod
		def _add_concat_to_regex(cls, regex, is_ascii = False):
			i = 0
			while i < len(regex):
					if regex[i] not in ['|', '(', '.'] and i < len(regex) - 1:
						if not is_ascii:
							if regex[i + 1] not in cls.operators and regex[i + 1] != ')':
									regex = regex[:i + 1] + '.' + regex[i + 1:]
									i += 1
						else:
							if regex[i] == ")" or regex[i] == "?" or regex[i] == "*" or regex[i] == "+":
								if regex[i+1] not in cls.operators and regex[i + 1] != ')':
									regex = regex[:i + 1] + '.' + regex[i + 1:]
									
							else:
									if i + 3 < len(regex):
										if regex[i + 3] not in cls.operators and regex [i + 3] != ')':			
												regex = regex[:i + 3] + '.' + regex[i + 3:]
												i += 3
					if not is_ascii:
						i += 1
					else:
						# if it is a digit, skip 3
						if regex[i] not in ['|', '(', ')', '?', '*', '.']:
							i += 3
						else:
							i += 1
			print("Concat regex", regex)
			return regex

		@classmethod
		def _postfix_from_regex(cls, regex, is_ascii = False):
				"""Converts a regex from postfix. If it is ASCII it has three digits"""
				# Add the . to the regex to handle concatenation
				regex = cls._add_concat_to_regex(regex, is_ascii)
				
				# Stack for tokens
				token_stack = []
				# Stack for operators
				operator_stack = []
				# Regex to list
				if not is_ascii:
					regex_list = list(regex)
				else:
					regex_list = []
					i = 0
					while i < len(regex):
						if regex[i] not in ['|', '(', ')', '?', '*', '.']:
							regex_list.append(regex[i:i+3])
							i += 3
						else:
							regex_list.append(regex[i])
							i += 1
				# Start the Shuntingh Yard Algorithm
				
				# Implementation of the Shunting Yard Algorithm (https://brilliant.org/wiki/shunting-yard-algorithm/
				for token in regex_list:
					is_operator = token in cls.operators.keys()	
					if not is_operator and token not in ['(', ')']:
						token_stack.append(token)	# For simple tokens, just append them to the stack
					elif token in ['(', ')']:
						if token == '(':
							operator_stack.append(token)
						else:
							# Pop all operators until the matching parenthesis is found
							while len(operator_stack) > 0 and operator_stack[-1] != '(':
								token_stack.append(operator_stack.pop())
							operator_stack.pop()	
					else:
						precedence = cls.operators[token]	# The precedence helps to determine which order the operators are evaluated	
						while len(operator_stack) > 0:
							if operator_stack[-1] == "(":
								break	# Don't to anything if the last operator is a parenthesis
							if not cls.operators[operator_stack[-1]] < precedence:
								break	# Don't do anything if the last operator has a higher precedence
							token_stack.append(operator_stack.pop()) 	# Append the last operator to the token stack
						operator_stack.append(token)	# Append the current operator to the operator stack
				while len(operator_stack) > 0:
					token_stack.append(operator_stack.pop()) # Last part of the algorithm: append remaining operators to the token stack
				return ''.join(token_stack)	# The output is a string in postfix notation			