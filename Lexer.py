from Token import Token
from Automata import Automata

class Lexer():
		tokens = {}	# Dictionary of tokens
		actions = {}
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
				# splitted_rules = rules_string.split('|')
				# splitted_rules.pop(0)
				# for rule in splitted_rules:
				# 	# replace all tabs with just one space
				# 	rule = rule.replace('\t', ' ')
				# 	rule = rule.strip()
				# 	print(rule)
				# 	name, value = rule.split(' ', 1)
				# 	value = value.replace('{','').replace('}','').strip()
				# 	if name in self.tokens.keys():
				# 		self.actions[name] = value


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

		
		def parse_action_line(self, line):
			
			pass

		def create_automata(self):
			regex = ''
			for key in self.tokens.keys():
				regex += '(' + self.tokens[key].value + ')'
				if key != list(self.tokens.keys())[-1]:
					regex += '|'
			automata = Automata._from_regex(regex, is_ascii=True)
			return automata


			