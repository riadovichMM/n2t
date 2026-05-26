import os
import sys

class virtual_machine:

    def __init__(self):
        self.files_codes = {}
        self.label_count = 0
        self.current_filename = ''
        self.asm_code = ''

        self.write('@256')
        self.write('D=A')
        self.write('@SP')
        self.write('M=D')
        self.write('@Sys.init')
        self.write('0;JMP')



    def get_files_codes(self):
        directory = sys.argv[1]
        files = os.listdir(directory)

        for file_name in files:
            self.current_filename = file_name
            f = open(os.path.join(directory, file_name), 'r+')
            self.files_codes[file_name] = f.readlines()
            f.close()

    def _pop_to_d(self):
        self.write('@SP')
        self.write('M=M-1')
        self.write('A=M')
        self.write('D=M')


    def write(self, code):
        self.asm_code = self.asm_code + code + '\n'


    def write_asm_in_file(self):
        file = open('program.asm', 'w+')
        file.write(self.asm_code)
        file.close()

    def _compare(self, command):
        self._pop_to_d()
        self.write('@SP')
        self.write('M=M-1')
        self.write('A=M')
        self.write('D=M-D')

        self.write(f'@TRUE_{self.label_count}')
        if command == 'eq':
            self.write('D;JEQ')
        if command == 'gt':
            self.write('D;JGT')
        if command == 'lt':
            self.write('D;JLT')

        self.write('@SP')
        self.write('A=M')
        self.write('M=0')
        self.write(f'@END_{self.label_count}')
        self.write('0;JMP')

        self.write(f'(TRUE_{self.label_count})')
        self.write('@SP')
        self.write('A=M')
        self.write('M=-1')

        self.write(f'(END_{self.label_count})')
        self.write('@SP')
        self.write('M=M+1')


    def translate_logic_arithmetic(self, command):
        if command == 'add':
            # _pop_to_d()
            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('M=D+M')

            self.write('@SP')
            self.write('M=M+1')
        if command == 'sub':
            self._pop_to_d()

            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('M=M-D')

            self.write('@SP')
            self.write('M=M+1')

        if command == 'neg':
            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('M=-M')

            self.write('@SP')
            self.write('M=M+1')
            
        if command == 'not':
            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('M=!M')

            self.write('@SP')
            self.write('M=M+1')

        if command == 'or':
            self._pop_to_d()
            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('M=D|M')

            self.write('@SP')
            self.write('M=M+1')

        if command == 'and':
            self._pop_to_d()
            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('M=D&M')

            self.write('@SP')
            self.write('M=M+1')

        if command in ['eq', 'gt', 'lt']:
            self._compare(command)


    def translate_push(self, segment, index):
        if segment == 'constant':
            self.write(f'@{index}')
            self.write('D=A')

            self.write('@SP')
            self.write('A=M')
            self.write('M=D')
            
            self.write('@SP')
            self.write('M=M+1')
        if segment == 'local':
            self.write('@LCL')
            self.write('D=M')

            self.write(f'@{index}')
            self.write('A=D+A')
            self.write('D=M')

            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M+1')
        if segment == 'argument':
            self.write('@ARG')
            self.write('D=M')

            self.write(f'@{index}')
            self.write('A=D+A')
            self.write('D=M')

            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M+1')
        if segment == 'this':
            self.write('@THIS')
            self.write('D=M')

            self.write(f'@{index}')
            self.write('A=D+A')
            self.write('D=M')

            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M+1')
        if segment == 'that':
            self.write('@THAT')
            self.write('D=M')

            self.write(f'@{index}')
            self.write('A=D+A')
            self.write('D=M')

            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M+1')
        if segment == 'temp':
            self.write('@5')
            self.write('D=A')

            self.write(f'@{index}')
            self.write('A=D+A')
            self.write('D=M')

            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M+1')
        if segment == 'static':
            self.write(f'@{self.current_filename}.{index}')
            self.write('D=M')

            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M+1')
        if segment == 'pointer':
            self.write('@3')
            self.write('D=A')

            self.write(f'@{index}')
            self.write('A=D+A')
            self.write('D=M')

            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M+1')



    def translate_pop(self, segment, index):
        if segment == 'local':
            self.write('@LCL')
            self.write('D=M')

            self.write(f'@{index}')
            self.write('D=D+A')

            self.write('@R13')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        if segment == 'argument':
            self.write('@ARG')
            self.write('D=M')

            self.write(f'@{index}')
            self.write('D=D+A')

            self.write('@R13')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        if segment == 'this':
            self.write('@THIS')
            self.write('D=M')

            self.write(f'@{index}')
            self.write('D=D+A')

            self.write('@R13')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        if segment == 'that':
            self.write('@THAT')
            self.write('D=M')

            self.write(f'@{index}')
            self.write('D=D+A')

            self.write('@R13')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write('@R13')
            self.write('A=M')
            self.write('M=D')

        if segment == 'temp':
            self.write('@5')
            self.write('D=A')

            self.write(f'@{index}')
            self.write('D=D+A')

            self.write('@R13')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        if segment == 'pointer':
            self.write('@3')
            self.write('D=A')

            self.write(f'@{index}')
            self.write('D=D+A')

            self.write('@R13')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        if segment == 'static':
            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write(f'@{self.current_filename}.{index}')
            self.write('M=D')


    def translate_label(self, command, label_name):
        if command == 'label':
            self.write(f"({label_name})")
        if command == 'goto':
            self.write(f'@{label_name}')
            self.write('0;JMP')
        if command == 'if-goto':
            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write(f'@END_{self.label_count}')
            self.write('D;JEQ')

            self.write(f'@{label_name}')
            self.write('0;JMP')

            self.write(f'(END_{self.label_count})')


    def translate_function(self, function_name, n_local_vars):
        self.write(f'(function_{function_name})')

        self.write(f'@{n_local_vars}')
        self.write('D=A')

        self.write('@R13')
        self.write('M=D')

        self.write(f'(LOOP_{self.label_count})')

        self.write('@R13')
        self.write('M=M-1')

        self.write('@SP')
        self.write('A=M')
        self.write('M=0')

        self.write('@SP')
        self.write('M=M+1')

        self.write('@R13')
        self.write('D=M')

        self.write(f'@LOOP_{self.label_count}')
        self.write('D;JNE')


    def translate_call(self, function_name, n_vars_arg):
        self.write(f'@return_address_{function_name}_{self.label_count}')
        self.write('D=A')

        self.write('@SP')
        self.write('A=M')
        self.write('M=D')

        self.write('@SP')
        self.write('M=M+1')

        self.write('@LCL')
        self.write('D=M')

        self.write('@SP')
        self.write('A=M')
        self.write('M=D')

        self.write('@SP')
        self.write('M=M+1')


        self.write('@ARG')
        self.write('D=M')

        self.write('@SP')
        self.write('A=M')
        self.write('M=D')

        self.write('@SP')
        self.write('M=M+1')

        
        self.write('@THIS')
        self.write('D=M')

        self.write('@SP')
        self.write('A=M')
        self.write('M=D')

        self.write('@SP')
        self.write('M=M+1')


        self.write('@THAT')
        self.write('D=M')

        self.write('@SP')
        self.write('A=M')
        self.write('M=D')

        self.write('@SP')
        self.write('M=M+1')


        # настраеваем новый ARG
        self.write('@SP')
        self.write('D=M')
        self.write(f'@{5 + int(n_vars_arg)}')
        self.write('D=D-A')
        self.write('@ARG')
        self.write('M=D')

        # настраеваем новый LCL
        self.write('@SP')
        self.write('D=M')
        self.write('@LCL')
        self.write('M=D')

        # прыгаем на функцию
        self.write(f'@function_{function_name}')

        # адрес возврата
        self.write(f'(return_address_{function_name}_{self.label_count})')


    def translate_return(self):
        # реузльтат выносим на аргументы функции
        self.write('@SP')
        self.write('M=M-1')
        self.write('A=M')
        self.write('D=M')

        self.write('@ARG')
        self.write('A=M')
        self.write('M=D')

        self.write('@ARG')
        self.write('D=M')
        self.write('@SP')
        self.write('M=D+1')

        self.write('@LCL')
        self.write('D=M')
        
        self.write('@R13')
        self.write('M=D')

        self.write('@R13')
        self.write('D=M')

        # востанавливаем THAT
        self.write('A=D-1')
        self.write('D=M')
        self.write('@THAT')
        self.write('M=D')

        # востанавливаем THIS
        self.write('@2')
        self.write('A=D-A')
        self.write('D=M')
        self.write('@THIS')
        self.write('M=D')

        # востанавливаем ARG
        self.write('@3')
        self.write('A=D-A')
        self.write('D=M')
        self.write('@ARG')
        self.write('M=D')

        # востанавливаем LCL
        self.write('@4')
        self.write('A=D-A')
        self.write('D=M')
        self.write('@LCL')
        self.write('M=D')

        # востанавливаем return_address
        self.write('@5')
        self.write('A=D-A')
        self.write('A=M')
        self.write('0;JMP')



    def process(self):
        for file_name in self.files_codes:
            for line in self.files_codes[file_name]:
                # delete comments
                line = line.strip()
                if not line or line.startswith('//'):
                    continue
                if '//' in line:
                    line = line[:line.index('//')].strip()
                
                self.write(f'// {line}')

                parts = line.split()

                command = parts[0]

                if command in  ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
                    # logic arithmetic
                    self.translate_logic_arithmetic(command)
                if command == 'push':
                    self.translate_push(parts[1], parts[2])
                if command == 'pop':
                    self.translate_pop(parts[1], parts[2])
                if command in ['label', 'goto', 'if-goto']:
                    self.translate_label(parts[0], parts[1])
                if command == 'function':
                    self.translate_function(parts[1], parts[2])
                if command == 'call':
                    self.translate_call(parts[1], parts[2])
                if command == 'return':
                    self.translate_return()

                self.label_count += 1
    
    
