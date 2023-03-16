class Node():
		def __init__(self, left_child, right_child, value,parent = None, label=None):
				self.parent = parent
				self.left_child = left_child
				self.right_child = right_child
				self.value = value
				self.label = label

		def nullable(self):
			if self.value == 'ε':
				return True
			elif self.value == '*':
				return True
			elif self.value == '|':
				return self.left_child.nullable() or self.right_child.nullable()
			elif self.value == '.':
				return self.left_child.nullable() and self.right_child.nullable()
			else:
				return False
			
		
		def firstpos(self):
			if self.value == 'ε':
				return tuple()
			elif self.value == '*':
				return self.left_child.firstpos()
			elif self.value == '|':
				return tuple(set(self.left_child.firstpos()).union(set(self.right_child.firstpos())))
			elif self.value == '.':
				if self.left_child.nullable():
					return tuple(set(self.left_child.firstpos()).union(set(self.right_child.firstpos())))
				else:
					return tuple(set(self.left_child.firstpos()))
			else:
				return tuple({self.label,})
			
		def lastpos(self):
			if self.value == 'ε':
				return tuple()
			elif self.value == '*':
				return self.left_child.lastpos()
			elif self.value == '|':
				return tuple(set(self.left_child.lastpos()).union(set(self.right_child.lastpos())))
			elif self.value == '.':
				if self.right_child.nullable():
					return tuple(set(self.left_child.lastpos()).union(set(self.right_child.lastpos())))
				else:
					return tuple(set(self.right_child.lastpos()))
			else:
				return tuple({self.label,})
			
		def followpos(self):
			positions = {}
			if self.value == ".":
				last_c1 = self.left_child.lastpos()
				first_c2 = self.right_child.firstpos()
				for last_pos in last_c1:
					positions[last_pos] = first_c2
			if self.value == '*':
				first = self.left_child.firstpos()
				last = self.left_child.lastpos()
				for last_pos in last:
					positions[last_pos] = first
			return positions



		def is_leaf(self):
			return self.left_child == None and self.right_child == None