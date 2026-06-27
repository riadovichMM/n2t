class parser:

    def __init__(self, tokens, file_path):
        self.tokens = tokens
        self.index = 0
        self.finish_tokens = ''
        self.level_tab = 0
        self.file_path = file_path

    def run(self):
        self.compile_class()
        self.generate_xml()

    def get_current_token(self):
        return self.tokens[self.index]

    def write_in_xml(self, text):
        self.finish_tokens += self.level_tab * '  ' + text + '\n'

    def advance(self):
        token = self.tokens[self.index]
        self.index += 1
        return token

    def show_not_passed_tokens(self):
        i = self.index
        while i < len(self.tokens):
            print(self.tokens[i])
            i += 1

    def process(self, type, value=None):
        current_token = self.tokens[self.index]
        if current_token[0] != type:
            raise Exception(f'Expected {type}, got {current_token[0]} at token: {current_token}')
        if value:
            if current_token[1] != value:
                raise Exception(f'Expected {value}, got {current_token[1]} at token: {current_token}')
        
        if type in ['keyword', 'symbol', 'identifier']:
            self.write_in_xml(f'<{type}> {current_token[1]} </{type}>')
        elif type == 'integerConstant':
            self.write_in_xml(f'<integerConstant> {current_token[1]} </integerConstant>')
        elif type == 'stringConstant':
            self.write_in_xml(f'<stringConstant> {current_token[1]} </stringConstant>')
        
        self.index += 1

    def generate_xml(self):
        output_filename = str(self.file_path).split('\\')[1].split('.')[0]
        f = open('xml/' + output_filename + '.xml', 'w+')
        f.write(self.finish_tokens)
        f.close()

    # ===== GRAMMAR =====

    def compile_class(self):
        self.write_in_xml('<class>')
        self.level_tab += 1
        self.process('keyword', 'class')
        self.process('identifier')
        self.process('symbol', '{')

        current_token = self.get_current_token()
        while current_token[1] == 'field' or current_token[1] == 'static':
            self.class_var_dec()
            current_token = self.get_current_token()

        current_token = self.get_current_token()
        while current_token[1] == 'constructor' or current_token[1] == 'function' or current_token[1] == 'method':
            self.subroutine_dec()
            current_token = self.get_current_token()

        self.process('symbol', '}')
        self.level_tab -= 1
        self.write_in_xml('</class>')
        print(self.finish_tokens)

    def class_var_dec(self):
        self.write_in_xml('<classVarDec>')
        self.level_tab += 1
        
        self.process('keyword')  # static | field
        
        # get type
        self.handle_type()
        
        self.process('identifier')

        current_token = self.get_current_token()
        while current_token[1] == ',':
            self.process('symbol', ',')
            self.process('identifier')
            current_token = self.get_current_token()
        self.process('symbol', ';')
        self.level_tab -= 1
        self.write_in_xml('</classVarDec>')

    def subroutine_dec(self):
        self.write_in_xml('<subroutineDec>')
        self.level_tab += 1

        self.process('keyword')  # constructor | function | method
        self.handle_type_or_void()
        self.process('identifier')
        self.process('symbol', '(')
        
        self.parameter_list()
        
        self.process('symbol', ')')
        
        self.subroutine_body()

        self.level_tab -= 1
        self.write_in_xml('</subroutineDec>')

    def handle_type_or_void(self):
        current_token = self.get_current_token()
        if current_token[1] == 'void':
            self.process('keyword', 'void')
        else:
            self.handle_type()

    def parameter_list(self):
        self.write_in_xml('<parameterList>')
        self.level_tab += 1

        current_token = self.get_current_token()
        if current_token[1] != ')':
            self.handle_type()
            self.process('identifier')

            current_token = self.get_current_token()
            while current_token[1] == ',':
                self.process('symbol', ',')
                self.handle_type()
                self.process('identifier')
                current_token = self.get_current_token()

        self.level_tab -= 1
        self.write_in_xml('</parameterList>')

    def handle_type(self):
        current_token = self.get_current_token()
        
        if current_token[0] == 'keyword':  # int, char, boolean
            self.process('keyword')
        elif current_token[0] == 'identifier':  # class name
            self.process('identifier')

    def subroutine_body(self):
        self.write_in_xml('<subroutineBody>')
        self.level_tab += 1
        self.process('symbol', '{')
        
        current_token = self.get_current_token()
        while current_token[1] == 'var':
            self.var_dec()
            current_token = self.get_current_token()

        self.statements()
        self.process('symbol', '}')

        self.level_tab -= 1
        self.write_in_xml('</subroutineBody>')

    def var_dec(self):
        self.write_in_xml('<varDec>')
        self.level_tab += 1

        self.process('keyword', 'var')
        self.handle_type()
        self.process('identifier')

        current_token = self.get_current_token()
        while current_token[1] == ',':
            self.process('symbol', ',')
            self.process('identifier')
            current_token = self.get_current_token()

        self.process('symbol', ';')

        self.level_tab -= 1
        self.write_in_xml('</varDec>')

    def statements(self):
        self.write_in_xml('<statements>')
        self.level_tab += 1
        
        current_token = self.get_current_token()
        while current_token[1] in ['let', 'if', 'while', 'do', 'return']:
            if current_token[1] == 'let':
                self.let_statement()
            elif current_token[1] == 'if':
                self.if_statement()
            elif current_token[1] == 'while':
                self.while_statement()
            elif current_token[1] == 'do':
                self.do_statement()
            elif current_token[1] == 'return':
                self.return_statement()
            
            current_token = self.get_current_token()

        self.level_tab -= 1
        self.write_in_xml('</statements>')

    def let_statement(self):
        self.write_in_xml('<letStatement>')
        self.level_tab += 1
        self.process('keyword', 'let')
        self.process('identifier')

        current_token = self.get_current_token()
        if current_token[1] == '[':
            self.process('symbol', '[')
            self.expression()
            self.process('symbol', ']')

        self.process('symbol', '=')
        self.expression()
        self.process('symbol', ';')

        self.level_tab -= 1
        self.write_in_xml('</letStatement>')

    def if_statement(self):
        self.write_in_xml('<ifStatement>')
        self.level_tab += 1
        
        self.process('keyword', 'if')
        self.process('symbol', '(')
        self.expression()
        self.process('symbol', ')')
        self.process('symbol', '{')
        self.statements()
        self.process('symbol', '}')

        current_token = self.get_current_token()
        if current_token[1] == 'else':
            self.process('keyword', 'else')
            self.process('symbol', '{')
            self.statements()
            self.process('symbol', '}')

        self.level_tab -= 1
        self.write_in_xml('</ifStatement>')

    def while_statement(self):
        self.write_in_xml('<whileStatement>')
        self.level_tab += 1
        
        self.process('keyword', 'while')
        self.process('symbol', '(')
        self.expression()
        self.process('symbol', ')')
        self.process('symbol', '{')
        self.statements()
        self.process('symbol', '}')

        self.level_tab -= 1
        self.write_in_xml('</whileStatement>')

    def do_statement(self):
        self.write_in_xml('<doStatement>')
        self.level_tab += 1
        
        self.process('keyword', 'do')
        self.subroutine_call()
        self.process('symbol', ';')

        self.level_tab -= 1
        self.write_in_xml('</doStatement>')

    def return_statement(self):
        self.write_in_xml('<returnStatement>')
        self.level_tab += 1
        
        self.process('keyword', 'return')
        
        current_token = self.get_current_token()
        if current_token[1] != ';':
            self.expression()
        
        self.process('symbol', ';')

        self.level_tab -= 1
        self.write_in_xml('</returnStatement>')

    def expression(self):
        self.write_in_xml('<expression>')
        self.level_tab += 1

        self.term()

        # операторы: + - * / & | < > =
        ops = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        
        current_token = self.get_current_token()
        while current_token[1] in ops:
            self.process('symbol', current_token[1])
            self.term()
            current_token = self.get_current_token()

        self.level_tab -= 1
        self.write_in_xml('</expression>')

    def term(self):
        self.write_in_xml('<term>')
        self.level_tab += 1
        
        current_token = self.get_current_token()
        token_type = current_token[0]
        token_value = current_token[1]
        
        # integerConstant
        if token_type == 'integerConstant':
            self.process('integerConstant')
        
        # stringConstant
        elif token_type == 'stringConstant':
            self.process('stringConstant')
        
        # keyword constant: true, false, null, this
        elif token_type == 'keyword' and token_value in ['true', 'false', 'null', 'this']:
            self.process('keyword')
        
        # унарный оператор: - или ~
        elif token_type == 'symbol' and token_value in ['-', '~']:
            self.process('symbol')
            self.term()
        
        # выражение в скобках: (expression)
        elif token_type == 'symbol' and token_value == '(':
            self.process('symbol', '(')
            self.expression()
            self.process('symbol', ')')
        
        # идентификатор (переменная, массив или вызов)
        elif token_type == 'identifier':
            self.process('identifier')
            
            next_token = self.get_current_token()
            next_value = next_token[1]
            
            # массив: arr[expr]
            if next_value == '[':
                self.process('symbol', '[')
                self.expression()
                self.process('symbol', ']')
            
            # вызов: func() или obj.method()
            elif next_value == '(' or next_value == '.':
                if next_value == '.':
                    self.process('symbol', '.')
                    self.process('identifier')
                
                self.process('symbol', '(')
                self.expression_list()
                self.process('symbol', ')')
        
        self.level_tab -= 1
        self.write_in_xml('</term>')

    def subroutine_call(self):
        # вызывается из do_statement
        # сначала идет имя подпрограммы или класса/объекта
        self.process('identifier')
        
        current_token = self.get_current_token()
        if current_token[1] == '.':
            self.process('symbol', '.')
            self.process('identifier')
        
        self.process('symbol', '(')
        self.expression_list()
        self.process('symbol', ')')

    def expression_list(self):
        self.write_in_xml('<expressionList>')
        self.level_tab += 1
        
        current_token = self.get_current_token()
        if current_token[1] != ')':
            self.expression()
            
            current_token = self.get_current_token()
            while current_token[1] == ',':
                self.process('symbol', ',')
                self.expression()
                current_token = self.get_current_token()
        
        self.level_tab -= 1
        self.write_in_xml('</expressionList>')