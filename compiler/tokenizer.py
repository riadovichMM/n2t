import re

class tokenizer:

    def __init__(self):
        self.code = ''
        self.state = 'start'
        self.index = 0

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

    def open_file(self, path):
        file = open(path, 'r+')
        jack_code_array = file.readlines()
        file.close()

        for line in jack_code_array:
            self.code += line
        
        self.code = self.remove_comments_simple(self.code)


    def process(self):
        while self.index < len(self.code):
            if self.code[self.index].isspace():
                self.index += 1
                continue
            if self.code[self.index].isalpha() or self.code[self.index] == '_':
                self.get_keyword_or_identifier()
            if self.code[self.index] == '"':
                self.get_string_constant()
            if self.code[self.index].isdigit():
                self.get_integer_constant()
            if self.code[self.index] in self.symbols:
                self.get_symbol()
        print(self.tokens)


    def get_keyword_or_identifier(self):
        start_index = self.index

        flag = True
        while flag:
            if self.code[self.index].isalpha() or self.code[self.index] == '_':
                self.index += 1
            else:
                flag = False
        
        token = self.code[start_index:self.index]
        if token in self.keywords:
            self.tokens.append(['keyword', token])
        else:
            self.tokens.append(['identifier', token])


    def get_string_constant(self):
        start_index = self.index
        self.index += 1
        flag = True
        while flag:
            if self.code[self.index] != '"':
                self.index += 1
            else:
                flag = False
                self.index += 1
            pass
        print(self.code[start_index:self.index])
        self.tokens.append(['stringConstant', self.code[start_index:self.index]])

    def get_integer_constant(self):
        start_index = self.index
        flag = True

        while flag:
            if self.code[self.index].isdigit():
                self.index +=1
            else:
                flag = False
        self.tokens.append(['integerConstant', self.code[start_index:self.index]])

    def get_symbol(self):
        self.tokens.append(['symbol', self.code[self.index]])
        self.index += 1