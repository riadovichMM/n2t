class parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.finish_tokens = ''
        self.level_tab = 0


    def run(self):
        self.compile_class()

    def get_current_token(self):
        return self.tokens[self.index]

    def write_in_xml(self, text):
        self.finish_tokens += self.level_tab * ' ' + text + '\n'

    def advance(self):
        self.index += 1

    def show_not_passed_tokens(self):
        i = self.index

        while i < len(self.tokens):
            print(self.tokens[i])
            i+=1
        

    def process(self, type, value=None):
        current_token = self.tokens[self.index]
        if (current_token[0] != type):
            raise Exception('token type != type')
        if value:
            if current_token[1] != value:
                raise Exception('token value != value')
        if value:
            self.write_in_xml(f'<{type}>{value}</{type}>')
        else:
            self.write_in_xml(f'<{type}>{current_token[1]}</{type}>')

        self.index += 1

    # grammar

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

        self.level_tab -= 1
        self.write_in_xml('</class>')
        print(self.finish_tokens)



    def class_var_dec(self):
        self.write_in_xml('<classVarDec>')
        self.level_tab += 1

        
        self.process('keyword') # static | field

        # get type
        current_token = self.get_current_token()

        self.write_in_xml(f'<{current_token[0]}>{current_token[1]}</{current_token[0]}>')
        self.advance()

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

        self.process('keyword') # constructor | function | method 
        self.handle_type()
        self.process('identifier')
        self.process('symbol', '(')
        
        current_token = self.get_current_token()
        if current_token[1] != ')':
            self.parameter_list()
        else:
            self.write_in_xml('<parameterList>')
            self.write_in_xml('</parameterList>')

        self.process('symbol', ')')
        
        self.subroutine_body()

        # todo
        self.level_tab -= 1
        self.write_in_xml('</subroutineDec>')


    def parameter_list(self):
        self.write_in_xml('<parameterList>')

        self.handle_type()
        self.process('identifier')

        current_token = self.get_current_token()
        while current_token[1] == ',':
            self.process('symbol', ',')
            self.handle_type()
            self.process('identifier')
            current_token = self.get_current_token()

        self.write_in_xml('</parameterList>')

    def handle_type(self):
        current_token = self.get_current_token()

        self.write_in_xml(f'<{current_token[0]}>{current_token[1]}</{current_token[0]}>')
        self.advance()

    def subroutine_body(self):
        self.write_in_xml('<subroutineBody>')
        self.level_tab += 1
        self.process('symbol', '{')
        
        current_token = self.get_current_token()
        while current_token[1] == 'var':
            self.var_dec()
            current_token = self.get_current_token()

        self.statements()


        # self.process('symbol', '}')

        self.level_tab -= 1
        self.write_in_xml('</subroutineBody>')

    def var_dec(self):
        # она работает?
        self.write_in_xml('<varDec>')
        self.level_tab += 1

        self.process('keyword', 'var')
        self.handle_type()
        self.process('identifier')


        current_token = self.get_current_token()
        while current_token[1] == ',':
            print(current_token)
            self.process('symbol', ',')
            self.process('identifier')
            current_token = self.get_current_token()

        self.process('symbol', ';')

        self.level_tab -= 1
        self.write_in_xml('</varDec>')

    def statements(self):
        pass




