class tokenizer:

    def __init__(self):
        self.jack_code = ''


    def open_and_read_file(self, file_name):
        file = open(f'./jack_code/{file_name}', 'r+')
        self.jack_code = file.readlines()
        file.close()
        print('jack_code:', self.jack_code)

