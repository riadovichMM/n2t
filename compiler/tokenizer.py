import re

class tokenizer:
    
    def __init__(self, file_path):
        self.code = ''
        self.index = 0
        self.file_path = file_path


        self.keywords = {
            "class", "constructor", "function", "method",
            "field", "static", "var", "int", "char",
            "boolean", "void", "true", "false", "null",
            "this", "let", "do", "if", "else",
            "while", "return"
        }
        self.symbols = {
            "{", "}", "(", ")", "[", "]",
            ".", ",", ";", "+", "-", "*",
            "/", "&", "|", "<", ">", "=", "~"
        }

        self.tokens = []


    def remove_comments_simple(self, jack_code):
        code = re.sub(r'//.*', '', jack_code)
        code = re.sub(r'/\*[\s\S]*?\*/', '', code)
        return code

    def open_file(self):
        file = open(self.file_path, 'r+')
        jack_code_array = file.readlines()
        file.close()

        for line in jack_code_array:
            self.code += line

        self.code = self.remove_comments_simple(self.code)



    def run(self):
        while self.index < len(self.code):

            if self.code[self.index].isspace():
                self.index += 1
                continue
            
            if self.code[self.index].isalpha() or self.code[self.index] == '_':
                self.get_keyword_or_identifier()
            if self.code[self.index] in self.symbols:
                self.get_symbol()
            if self.code[self.index] == '"':
                self.get_string_constant()
            if self.code[self.index].isdigit():
                self.get_int_constant()
                
        


    def get_keyword_or_identifier(self):
        token = ''
        while True:
            if (not self.code[self.index].isalpha()) and (not self.code[self.index].isdigit()) and (not self.code[self.index] == '_'):
                break
            token += self.code[self.index]
            self.index += 1
        
        if token in self.keywords:
            self.tokens.append(['keyword', token])
        else:
            self.tokens.append(['identifier', token])


    def get_symbol(self):
        if self.code[self.index] in self.symbols:
            self.tokens.append(['symbol', self.code[self.index]])
            self.index += 1
        


    def get_string_constant(self):
        token = ''
        token += self.code[self.index]
        self.index+= 1
        while True:
            if self.code[self.index] == '"':
                token += self.code[self.index]
                self.index+=1
                break
            else:
                token += self.code[self.index]
                self.index+= 1
        
        self.tokens.append(['stringConstant', token])


    def get_int_constant(self):
        token = ''

        while True:
            if not self.code[self.index].isdigit():
                break
            token += self.code[self.index]
            self.index += 1
        
        self.tokens.append(['integerConstant', token])

    def generate_xml_file(self):
        # windows
        # file_name = str(self.file_path).split('\\')[1]

        # mac os
        file_name = str(self.file_path).split('/')[1]

        clean_file_name = file_name.split('.')[0]
        print(clean_file_name)

        file = open('xml/' + clean_file_name + 'T.xml', 'w+')
        file.write('<tokens>\n')
        for token in self.tokens:
            file.write(f'  <{token[0]}> {token[1]} </{token[0]}>\n')
        file.write('</tokens>')
        file.close()