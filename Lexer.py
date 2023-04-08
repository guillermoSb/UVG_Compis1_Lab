from Token import Token

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
					words = line.split(' ')
					# If the first word is 'let' create a token
					if words[0] == "let":
						token_name = words[1]
						# Create the token regex (todo)
						self.tokens[token_name] = "TODO"				