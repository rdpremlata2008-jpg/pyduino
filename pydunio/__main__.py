# pydunio/__main__.py
import argparse
from pydunio.compiler.parser import convert_to_arduino
from pydunio.compiler.uploader import compile_and_upload

def main():
    parser = argparse.ArgumentParser(description="PyDunio CLI")
    parser.add_argument("script", help="PyDunio Python script")
    parser.add_argument("--board", default="arduino:avr:uno")
    parser.add_argument("--port", default="COM3")
    parser.add_argument("--upload", action="store_true")
    args = parser.parse_args()

    ino_code = convert_to_arduino(args.script)
    compile_and_upload(ino_code, args.board, args.port, args.upload)

if __name__ == "__main__":
    main()
