class Node():
		def __init__(self, left_child, right_child, value,parent = None, label=None):
				self.parent = parent
				self.left_child = left_child
				self.right_child = right_child
				self.value = value
				self.label = label
		
		def is_leaf(self):
			return self.left_child == None and self.right_child == None