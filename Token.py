class Token():
		def __init__(self, name, value):
				self.name = name
				self.value = value

		@classmethod
		def _from_yalex(cls, name, yalex):
			regex = ''
			# ---- Validations ----
			
			# Check that ne number of [ and ] are the same
			if yalex.count('[') != yalex.count(']'):
				raise Exception('[YALEX ERROR]: Invalid yalex syntax - all square brackets must be closed')
			# Check that the number of ' is even
			if yalex.count("'") % 2 != 0:
				raise Exception('[YALEX ERROR]: Invalid yalex syntax - all single quotes must be closed')
			
			# ---- Convert to regex ----
			building_range = False
			range_regex = ''
			for i in range(len(yalex)):
				if yalex[i] == '[':
					building_range = True
					continue
				if yalex[i] == ']':
					# Convert range to regex
					m_regex = ''
					for j in range(len(range_regex)):
						if range_regex[j] == "-":
							start = ord(range_regex[j-2])
							end = ord(range_regex[j+2])
							for k in range(start + 1, end):
								m_regex += "'" + chr(k) + "'"
						else:
							m_regex += range_regex[j]
					regex += "(" + m_regex + ")"
					range_regex = ''
					building_range = False
					continue
				if not building_range:
					regex += yalex[i]
				else:
					range_regex += yalex[i]

			# Convert to ascii
			ascii_regex = ''
			for i in range(len(regex)):
				if i > 0 and i < len(regex) - 1:
					if regex[i - 1] == "'" and regex [i + 1] == "'":
						ascii_regex += "{0:0=3d}".format(ord(regex[i]))
						continue
				ascii_regex += regex[i]
			
			# Replace '' with |
			ascii_regex = ascii_regex.replace("''", "'|'")
			return Token(name, ascii_regex)

		