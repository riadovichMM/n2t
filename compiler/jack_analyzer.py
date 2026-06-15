import sys
from tokenizer import tokenizer
from pathlib import Path

def main():
    print(sys.argv)

    path = sys.argv[1]

    files = [f for f in Path(path).iterdir() if f.is_file()]
    for file_path in files:
        t = tokenizer()
        t.open_file(file_path)
        t.process()


main()