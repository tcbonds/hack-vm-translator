import os
import sys
from parser import Parser
from codewriter import CodeWriter

class VMTranslator:

	def __init__(self,path):
		pass

	def translate_single_file(self, vm_file, codewriter):

		assembly_code = []
		parser = Parser(vm_file)
		while parser.hasMoreCommands():
			parser.advance()

			command_type = parser.commandType()
			arg1 = parser.arg1(command_type)
			arg2 = parser.arg2(command_type)

			print(command_type)
			print(arg1)
			print(arg2)

			if command_type in ['C_PUSH','C_POP']:
				code_line = codewriter.WritePushPop(command_type, arg1, arg2)
			elif command_type == 'C_ARITHMETIC':
				code_line = codewriter.writeArithmetic(arg1)
			else:
				code_line = None
			
			print(code_line)
			assembly_code.append(code_line)


		filename = vm_file.split('.')[0]
		with open(f'{filename}.asm', 'w') as output_file:
			for line in assembly_code:
				output_file.write(line)

		output_file.close()

	def translate(self):

		codewriter = CodeWriter(path)

		if os.path.isdir(path):
			os.chdir(path)
			for vm_file in os.listdir('.'):
				if os.path.splitext(vm_file)[1] == '.vm':
					print(vm_file)
					self.translate_single_file(vm_file, codewriter)
		else:
			self.translate_single_file(path, codewriter)
		

if __name__ == "__main__":

	path = sys.argv[1]

	vmtranslator = VMTranslator(path)
	vmtranslator.translate()