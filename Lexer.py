from Token import Token
from Automata import Automata

class Lexer():
		tokens = {}	# Dictionary of tokens
		actions = {}
		def __init__(self, file):
				# Varaibles to keep track of the parsing
				created_rules = False
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
				rule_lines = []
				# Iterate over lines
				for line in lines:
					if created_rules:
						rule_lines.append(line)
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

		def replace_constructions(self):
				sorted_names = sorted(list(self.tokens.keys()), key=len, reverse=True)
				for key in self.tokens.keys():
						# Replace constructions
						search = True
						while search:
							for name in sorted_names:
								if name in self.tokens[key].value:
									self.tokens[key].value = self.tokens[key].value.replace(name, self.tokens[name].value)
									break
							search = False
						# Replace quotes
						self.tokens[key].value = self.tokens[key].value.replace("'", '')
		
		def draw_automata(self):
			regex = ''
			for key in self.tokens.keys():
				regex += '(' + self.tokens[key].value + ')'
				if key != list(self.tokens.keys())[-1]:
					regex += '|'
			automata = Automata._from_regex(regex, is_ascii=True)
			automata.draw()


			