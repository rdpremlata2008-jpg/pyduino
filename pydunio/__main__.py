# pydunio/__main__.py
import argparse
from pydunio.compiler import PyDunioCompiler

def main():
    parser = argparse.ArgumentParser(description="PyDunio CLI")
    parser.add_argument("script", help="PyDunio Python script")
    parser.add_argument("--board", default="arduino:avr:uno")
    parser.add_argument("--port", default="COM3")
    parser.add_argument("--upload", action="store_true")
    args = parser.parse_args()

    compiler = PyDunioCompiler()
    ino_code = compiler.compile(open(args.script).read())
    
    from pathlib import Path
    sketch_dir = Path("generated_sketch")
    sketch_dir.mkdir(exist_ok=True)
    (sketch_dir / "sketch.ino").write_text(ino_code)
    print(f"Generated: {sketch_dir / 'sketch.ino'}")

if __name__ == "__main__":
    main()
