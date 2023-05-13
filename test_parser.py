from Parser import Parser

def test_parser01():
  # Arrange
	parser = Parser._from_file('yapar.txt')
	first_item = (parser.grammar.start,0,0) # First item to be used on the closure
	# Act
	closure = parser.closure({first_item})
	print("FINAL CLOSURE: ", closure)
	print(parser.grammar.productions)
	assert True == False