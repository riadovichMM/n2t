class parser:

    def __init__(self, tokens, file_name):
        self.tokens = tokens
        self.file_name = file_name
        self.index = 0

    def run(self):
        pass

    def generate_xml_file(self):
        pass

    def process(self, type, value):
        current_token = self.tokens[self.index]
        if current_token[0] == type:
            raise ValueError(f'Current Token type({current_token[0]}) and input token type({type}) is not matches')
        if current_token[1] == value:
            raise ValueError(f'Current Token value({current_token[0]}) and input token value({type}) is not matches')
        self.index += 1

    # grammar

    def compile_class(self):
        pass

