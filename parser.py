class Parser:
	
	def __init__(self, vm_file):
		self.line_list = []

		with open(vm_file, 'r') as vm_code:
			for line in vm_code:
				self.line_list.append(line)

		self.current_line_ix = None
		self.current_line = None
		self.line_total = len(self.line_list)
		self.arith_op_list = ['add','sub','neg','eq','gt','lt','and','or','not']

	def hasMoreCommands(self):
		if self.current_line_ix != None:
			return self.current_line_ix < self.line_total - 1
		else:
			return True # Parser has not begun parsing hence current_line_ix = None

	def advance(self):
		if self.current_line_ix != None:
			self.current_line_ix += 1
		else:
			self.current_line_ix = 0

		self.current_line = self.line_list[self.current_line_ix]

		if '//' == self.current_line[:2] or '\n' == self.current_line :
			self.advance()
		else:
			comment_ix = self.current_line.find('//')
			if comment_ix != -1:
				self.current_line = self.current_line[:comment_ix]
			for char in ['\n','\r']: # spaces are not included
				self.current_line = self.current_line.replace(char, '')
			self.current_line = self.current_line.strip(' ')
			print(r"{}".format(self.current_line))

	def commandType(self):
		if 'push' in self.current_line:
			return 'C_PUSH'
		elif 'pop' in self.current_line:
			return 'C_POP'
		elif any(arith_op in self.current_line for arith_op in self.arith_op_list):
			return 'C_ARITHMETIC'			
		else:
			return None

	def arg1(self, commandType):
		if commandType == 'C_ARITHMETIC':
			return self.current_line
		elif commandType != 'C_RETURN':
			return self.current_line.split(' ')[1]
		else:
			return None

	def arg2(self, commandType):
		if commandType in ['C_PUSH','C_POP','C_FUNCTION','C_CALL']:
			return self.current_line.split(' ')[2]	
		else:
			return None

if __name__ == '__main__':
	parser = Parser('SimpleAdd.vm')
	print(parser.hasMoreCommands())
	parser.advance()
	command_type = parser.commandType()
	print(parser.commandType())
	print(parser.arg1(command_type))
	print(parser.arg2(command_type))


