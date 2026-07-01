class parser:

    def __init__(self, tokens, file_name):
        self.tokens = tokens
        self.file_name = file_name
        self.index = 0
        self.final_tokens = ''
        self.padding = 0

    def run(self):
        self.compile_class()

    def generate_xml_file(self):
        pass

    def write_in_xml(self, xml):
        self.final_tokens = self.final_tokens + xml + '\n'

    def process(self, type, value=None):
        current_token = self.tokens[self.index]
        if current_token[0] != type:
            raise ValueError(f'Current Token type({current_token[0]}) and input token type({type}) is not matches')
        if value and current_token[1] != value:
            raise ValueError(f'Current Token value({current_token[0]}) and input token value({type}) is not matches')

        if value:
            self.write_in_xml(('  ' * self.padding) + f'<{type}>{value}</{type}>')
        else:
            self.write_in_xml(('  ' * self.padding) + f'<{type}>{current_token[1]}</{type}>')
        self.index += 1

    # grammar

    def compile_class(self):
        self.write_in_xml('<tokens>')
        self.padding += 1

        # grammar
        self.process('keyword', 'class')
        self.process('identifier')

        self.process('symbol', '{')


        current_token = self.tokens[self.index]
        while current_token[1] in ['static', 'field']:
            self.class_var_dec()


        self.padding -= 1
        self.write_in_xml('</tokens>')


        print(self.final_tokens)

    def class_var_dec(self):
        self.write_in_xml('<classVarDec>')
        self.padding += 1


        # grammar
        self.process('keyword') # static | field;
        self.type()


        self.padding -= 1
        self.write_in_xml('</classVarDec>')

    
    def type(self):
        current_token = self.tokens[self.index]
        if current_token[1] in ['int', 'char', 'boolean']:
            self.process('keyword')
        elif current_token[0] == 'identifier':
            self.process('identifier')




