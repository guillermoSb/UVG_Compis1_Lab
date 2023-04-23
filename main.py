from Lexer import Lexer
from Automata import Automata

l = Lexer('yalex2.txt')




token_dict = {}
actions_dict = {}
automata_dict = {}

# Read the token dictionary

for token in l.tokens:
	token_dict[token] = l.tokens[token].value

for action in l.actions:
	actions_dict[action] = l.actions[action].value

for token in l.tokens:
	automata_dict[token] = Automata._from_regex(token_dict[token], is_ascii=True)
	if token in actions_dict:
		automata_dict[token]._action = actions_dict[token]


# Read the input file
accepted_automatas = {}

with open('input.txt', 'r') as input_file:
	input = input_file.read()
	input_file.close()

	# Read every character in the input
	buffer = ""
	lexeme_begin = 0
	i = 0
	print(actions_dict)
	while i < len(input):
		char = input[i]
		buffer += char		
		stop_search = True

		for automata in automata_dict:
			states = automata_dict[automata].simulate(buffer)
			if len(states) > 0:
				stop_search = False
				if automata_dict[automata]._final in states:
					# The automata accepted the buffer
					accepted_automatas[automata] = (lexeme_begin, i + 1)
		if stop_search:
			# The buffer was not accepted by any automata
			# Check if there is an accepted automata
			if len(accepted_automatas) > 0:
				# Find the automata with the longest prefix
				automata = max(accepted_automatas, key=lambda x: accepted_automatas[x][1] - accepted_automatas[x][0])
				# print(automata, input[accepted_automatas[automata][0]:accepted_automatas[automata][1]])
				action = automata_dict[automata]._action
				if action is not None:
					exec(action)
				else:
					print("Accion no disponible: ", automata)
				lexeme_begin = accepted_automatas[automata][1]
				# Reset state of simulation
				accepted_automatas = {}
				buffer = ""
				i = lexeme_begin - 1
		i += 1

