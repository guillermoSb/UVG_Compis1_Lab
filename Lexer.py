from Token import Token
from Automata import Automata, Action

class Lexer():
		tokens = {}	# Dictionary of tokens
		actions = {} # Dictionary of actions
		def __init__(self, file):
				# Varaibles to keep track of the parsing
				# Open file and read it
				self.file = open(file, 'r')
				self.text = self.file.read()
				self.file.close()
				# Remove double spaces
				self.text = self.text.replace('  ', ' ')
				# Split the text with new line
				lines = self.text.splitlines()
				# Remove empty lines
				lines = [line for line in lines if line != '']
				rules_string = ""
				# Iterate over lines
				rules = False
				for line in lines:
					if line.replace(' ', '') == 'ruletokens=':
						rules = True
					if rules:
						rules_string += line.strip()
						continue
					# Split the line in words
					
					splitted = line.split(' = ')
					# If the first word is 'let' create a token
					if splitted[0].split(' ')[0] == "let":
						right = splitted[1]
						left = splitted[0].split(' ')
						token_name = left[1]
						# Create the token regex (todo)
						self.tokens[token_name] = Token._from_yalex(token_name, right)
				self.replace_constructions()

				# Process rules
				# Split rules by |
				splitted_rules = rules_string.split('|')
				splitted_rules.pop(0)
				for line in splitted_rules:
					action = self.parse_action_line(line)
					self.actions[action.name] = action


		def replace_constructions(self):
				sorted_names = sorted(list(self.tokens.keys()), key=len, reverse=True)
				for key in self.tokens.keys():
						# Replace constructions
						search = True
						while search:
							for name in sorted_names:
								while name in self.tokens[key].value:
									self.tokens[key].value = self.tokens[key].value.replace(name, self.tokens[name].value)
									
							search = False
						# Replace quotes
						self.tokens[key].value = self.tokens[key].value.replace("'", '')

		def create_automata(self):
			regex = ''
			for key in self.tokens.keys():
				regex += '(' + self.tokens[key].value + ')'
				if key != list(self.tokens.keys())[-1]:
					regex += '|'
			automata = Automata._from_regex(regex, is_ascii=True)
			return automata


		
		def parse_action_line(self, line):
			# Parse a line of the form: 'token' {action}
			name = ''
			value = ''
			type = 'token'
			parsing_action = False
			for char in line:
				if char == "{":
					parsing_action = True
					continue
				if char == "}":
					parsing_action = False
					break
				if parsing_action:
					value += char
					continue
				if char == "'":
					type = 'keyword'
					continue
				if char not in [ " ", '\t', '\n', "'"] and not parsing_action:
					name += char
			value = value.strip()
			new_action = Action(type, name, value)
			if new_action.type == 'keyword':
				token_value = ''
				for char in new_action.name:
					token_value += "{0:0=3d}".format(ord(char))
				new_token = Token(new_action.name, token_value)
				self.tokens[new_action.name] = new_token
			return new_action
		

		def create_program(self):
			# Will create a new file called lexical_analyzer.py

			with open('lexical_analyzer.py', 'w') as f:
				# Write all the contents of Automata.py on the new file
				with open('Automata.py', 'r') as automata_file:
					f.write(automata_file.read())
					automata_file.close()	# Close the file
				
				# Write all the code contents
				f.write('if __name__ == "__main__":')

				f.write("""
					with open('input.txt', 'r') as input_file:
						input = input_file.read()
						input_file.close()
				""")
				
				f.close()	# Close the file
					
				
			