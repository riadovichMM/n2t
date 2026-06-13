import sys
from tokenizer import tokenizer

def main():
    print(sys.argv)
    t = tokenizer()
    t.open_and_read_file(sys.argv[1])
    pass


main()