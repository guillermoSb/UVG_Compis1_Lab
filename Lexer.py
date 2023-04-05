from Token import Token

class Lexer():
		tokens = {}	# Dictionary of tokens
		
		
		def parse_token(self, name, value):
			new_value = ''
			# Build the range
			for i in range(len(value)):
				if value[i] == "-":
					start = ord(value[i-2])
					end = ord(value[i+2])
					for j in range(start, end + 1):
						new_value += "'{}'".format(chr(j))
						if j != end:
							new_value += "|"
			if new_value != '':
				value = new_value	
				new_value = ''
			# Insert an | between each '' in the value
			for i in range(len(value)):	
				if i + 1 < len(value):
						if value[i] == "'" and value[i + 1] == "'":
							new_value += "|"										
				if i > 0 and i + 1 < len(value):
					if value[i-1] == "'" and value[i+1] == "'" and value[i] != "|":
						# Get ascii representation of the character
						new_value += "{0:0=3d}".format(ord(value[i]))
					elif value[i] == "|":
						new_value += value[i]
			# Replace [] with ()

			new_value = "(" + new_value + ")"
			return Token(name, new_value)

			

				
