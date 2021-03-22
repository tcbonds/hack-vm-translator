class CodeWriter:
	

	def __init__(self,vm_file):
		self.filename = vm_file.split('.')[0]

		self.eq_count = 0
		self.gt_count = 0
		self.lt_count = 0

		self.non_ineq_mapping = \
				{
					'add':
							'''
								@SP
								A=M
								A=A-1
								D=M
								A=A-1
								D=D+M

								@SP
								M=M-1
								A=M-1
								M=D
							''',
					'sub':
							'''
								@SP
								A=M
								A=A-1
								D=M
								A=A-1
								D=D-M
								D=-D

								@SP
								M=M-1
								A=M-1
								M=D
							''',
					'neg':
							'''
								@SP
								A=M
								A=A-1
								M=-M
							''',
					'and':
							'''
								@SP
								A=M
								A=A-1
								D=M
								A=A-1
								D=D&M

								@SP
								M=M-1
								A=M-1
								M=D
							''',
					'or':
							'''
								@SP
								A=M
								A=A-1
								D=M
								A=A-1
								D=D|M

								@SP
								M=M-1
								A=M-1
								M=D
							''',
					'not':
							'''
								@SP
								A=M
								A=A-1
								M=!M
							''',
				}

		self.segment_mapping = \
		{
			'local': 'LCL', 
			'argument': 'ARG',
			'this': 'THIS', 
			'that': 'THAT',
			'temp': '5',
			'pointer': '3',
		}

	def setFileName():
		pass

	def close():
		pass

	def increment_ineq_count(self, command):
		if command == 'eq':
			self.eq_count += 1
			return self.eq_count
		elif command == 'gt':
			self.gt_count += 1
			return self.gt_count
		elif command == 'lt':
			self.lt_count += 1
			return self.lt_count

	@staticmethod
	def clean_assembly(code):
	    code = code.replace('\n\n\t','\n\t')
	    code = code.replace('\t','')
	    if code[0] == '\n':
	    	code = code[1:]
	    return code

	def writeArithmetic(self, command):
		if command not in ['eq','lt','gt']:
			final_code = self.non_ineq_mapping.get(command)
		else:
			ineq_count = self.increment_ineq_count(command)

			command = command.upper()
			ineq_label = f'{command}{ineq_count}'
			end_ineq_label = f'END_{command}{ineq_count}'
			jump_command = f'J{command}'

			final_code = \
			'''	
				@2
				D=A
				@SP
				A=M
				A=A-D
				D=M
				A=A+1
				D=D-M

				@{0}
				D;{2}

				D=0
				@{1}
				0;JMP

				({0})
				D=-1

				({1})
				@SP
				M=M-1
				A=M-1
				M=D
			'''.format(ineq_label, end_ineq_label, jump_command)

		return self.clean_assembly(final_code)

	def WritePushPop(self, command, segment, ix):
		
		segment_code = self.segment_mapping.get(segment)
		print(segment)
		if segment in ['local','argument','this','that']:
			if command == 'C_PUSH':
					
				final_code = \
						'''
							@{}
							D=A

							@{}
							A=M+D
							D=M

							@SP
							A=M
							M=D

							@SP
							M=M+1
						'''.format(ix, segment_code)

			elif command == 'C_POP':

				final_code = \
						'''
							@{}
							D=A

							@{}
							D=D+M

							@addr
							M=D

							@SP
							M=M-1
							A=M
							D=M

							@addr
							A=M
							M=D
						'''.format(ix, segment_code)
		elif segment == 'constant':
			final_code = \
						'''
							@{}
							D=A

							@SP
							A=M
							M=D

							@SP
							M=M+1
						'''.format(ix)

		elif segment == 'static':
			static_name = self.filename + '.' + ix
			if command == 'C_PUSH':
					
				final_code = \
						'''
							@{}
							D=M

							@SP
							A=M
							M=D

							@SP
							M=M+1
						'''.format(static_name)

			elif command == 'C_POP':

				final_code = \
						'''
							@SP
							M=M-1
							A=M
							D=M

							@{}
							M=D
						'''.format(static_name)

		elif segment == 'temp':

			if command == 'C_PUSH':

				final_code = \
						'''
						@5
						D=A

						@{}
						A=D+A
						D=M

						@SP
						A=M
						M=D

						@SP
						M=M+1
						'''.format(ix)

			elif command == 'C_POP':

				final_code = \
						'''
						@5
						D=A

						@{}
						D=D+A

						@addr
						M=D

						@SP
						M=M-1
						A=M
						D=M

						@addr
						A=M
						M=D
						'''.format(ix)

		elif segment == 'pointer':
			this_that_mapping = \
				{
					'0':'THIS',
					'1': 'THAT'
				}

			if command == 'C_PUSH':

				final_code = \
						'''
						@{}
						D=M

						@SP
						A=M
						M=D

						@SP
						M=M+1
						'''.format(this_that_mapping[ix])

			elif command == 'C_POP':

				final_code = \
						'''
						@SP
						M=M-1
						A=M
						D=M

						@{}
						M=D
						'''.format(this_that_mapping[ix])


		return self.clean_assembly(final_code)


if __name__ == '__main__':
	codewriter = CodeWriter('SimpleAdd.vm')
	print(codewriter.WritePushPop('C_POP','static','7'))

