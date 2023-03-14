from graphviz import Digraph


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


		def __init__(self, states, initial, final, symbols, type = 'NFA', labels = {}):
				"""Constructor for the Automata class"""				
				self._states = states
				self._initial = initial
				self._final = final
				self._type = type
				self._symbols = symbols
				self._labels = labels

		
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
									dot.node('{}'.format(self._labels[state]), shape="doublecircle")
						elif  state == self._initial:          
									dot.node('{}'.format(self._labels[state]), shape="triangle")
						else:
									dot.node('{}'.format(self._labels[state]),)

				for state in self._states.keys():
						for transition in self._states[state]:
							to = self._states[state][transition]
							
							dot.edge('{}'.format(self._labels[tuple(state)]), '{}'.format(self._labels[tuple(to)]), label=transition)

			dot.render('automaton.gv', view=True)

		

		# Class Methods
		
		
		@classmethod
		def _dfa_from_nfa(self, nfa):
			# Validate correct type of automaton
			if nfa._type != 'NFA':
				raise Exception("[NFA ERROR] The input for this method should be a NFA Automaton.")
			d_transitions = {}	# DFA transitions will be stored here
			d_states_unmarked = [nfa.e_closure(nfa._initial),]
			d_states_marked = []
			while len(d_states_unmarked) > 0:
				# Mark the new state
				d_state = tuple(sorted(d_states_unmarked.pop()))
				d_states_marked.append(set(d_state))
				for input in nfa._symbols:
					# print("Moving from", d_state, input)	
					U = set(nfa.e_closure_t(nfa.move(d_state, input)))
					if U not in d_states_marked:
						d_states_unmarked.append(tuple(U))
					if d_state in d_transitions.keys():
						d_transitions[d_state] = {
							**d_transitions[d_state],
							input: U
						}
					else: 
						d_transitions[d_state] = {
							input: U
						}
			# Create final states and state labels
			counter = 0
			final_states = []
			state_labels = {}
			# TODO: Fix bug state labels are not on order.
			for state in d_states_marked:
				state_labels[tuple(sorted(state))] = counter
				counter += 1
				if nfa._final in state:
					final_states.append(tuple(sorted(state)))
			return Automata(d_transitions, tuple(d_states_marked[0]), final_states, nfa._symbols, 'DFA', state_labels)
		

		def simulate(self, input):
			if self._type == 'DFA':
				current_state = self._initial
				for s in input:
					# Check if s is on the symbol list
					if s not in self._symbols:
						raise Exception("[Simulation Error] - {} is not on symbol list.".format(s))
					current_state = tuple(self._states[current_state][s])
				# Check if the final state is on the final states
				if current_state not in self._final:
					raise Exception("[Simulation Error] - {} was not accepted.".format(input))
				else:
					return True
			
		
		@classmethod
		def _from_regex(self, regex):		
				"""Creates an Automata from a regex"""

				self._regex = regex.replace(' ', '')	# Remove spaces from the regex
				self._check_regex(regex)	# Check that the regex is valid
				self._postfix = self._postfix_from_regex(regex)	# Convert the regex to postfix
				return self._states_from_postfix(self._postfix)	# Create the states for the automaton

		
				
		
		@classmethod
		def _check_regex(cls, regex):
			"""Checks that the regex is valid, throws an error if invalid."""
			# Check that the regex has the same number of opening and closing parentheses
			if regex.count('(') != regex.count(')'):
				raise Exception("[REGEX ERROR] The regex has a different number of opening and closing parentheses.")
			
			# Check that there are no two operators in a row
			for i in range(0, len(regex)):

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
		def _states_from_postfix(cls, postfix):
			"""Creates the staes for the automata from a postfix expression"""
			state_counter = 0
			postfix_stack = list(postfix)
			operation_stack = []
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
		def _postfix_from_regex(cls, regex):
				"""Converts a regex from postfix"""
				# Add the . to the regex to handle concatenation
				# TODO: Check how to handle concatenation without any special character
				i = 0
				while i < len(regex):
					if regex[i] not in ['|', '(', '.'] and i < len(regex) - 1:
						if regex[i + 1] not in cls.operators and regex[i + 1] != ')':
							regex = regex[:i + 1] + '.' + regex[i + 1:]
					i += 1
				
				# Stack for tokens
				token_stack = []
				# Stack for operators
				operator_stack = []
				# Regex to list
				regex_list = list(regex)
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
				

	