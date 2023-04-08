class Token():
		def __init__(self, name, value):
				self.name = name
				self.value = value

		@classmethod
		def _from_yalex(cls, name, yalex):
			regex = ''
			# Validations
			# Check that ne number of [ and ] are the same
			if yalex.count('[') != yalex.count(']'):
				raise Exception('[YALEX ERROR]: Invalid yalex syntax - all square brackets must be closed')
			# Check that the number of ' is even
			if yalex.count("'") % 2 != 0:
				raise Exception('[YALEX ERROR]: Invalid yalex syntax - all single quotes must be closed')
			# Convert to ascii
			return Token(name, yalex)

		