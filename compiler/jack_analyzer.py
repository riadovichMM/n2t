import sys
from tokenizer import tokenizer
from pathlib import Path
from parser import parser


def main():
    print(sys.argv)

    path = sys.argv[1]

    files = [f for f in Path(path).iterdir() if f.is_file()]

    for file_path in files:
        t = tokenizer()
        t.open_file(file_path)
        t.run()
        # t.generate_xml()

        p = parser(t.tokens)
        p.run()


main()