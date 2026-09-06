"""
PyDunio
Python-first Arduino compiler.

Commands:

    python -m pydunio.pydunio blink.py
    python -m pydunio.pydunio blink.py --compile
    python -m pydunio.pydunio blink.py --upload COM3
"""

from pathlib import Path
import shutil
import subprocess
import sys
try:
    from .compiler import PyDunioCompiler
except ImportError:
    from compiler import PyDunioCompiler


VERSION = "0.1.0"


# ============================================================
# Messages
# ============================================================

def header():

    print()
    print("PyDunio")
    print("=======")
    print(f"Version {VERSION}")
    print()


def error(message):

    print()
    print("ERROR:")
    print(message)
    print()


def success(message):

    print()
    print("SUCCESS:")
    print(message)
    print()


# ============================================================
# Find Arduino CLI
# ============================================================
def find_arduino_cli():
    import shutil
    from pathlib import Path

    # First check PATH
    found = shutil.which("arduino-cli")

    if found:
        return found

    # Common Arduino CLI locations
    locations = [
        Path.home() / "AR" / "Arduino IDE" / "resources" / "app" / "lib" / "backend" / "resources" / "arduino-cli.exe",
        Path.home() / "AppData" / "Local" / "Programs" / "Arduino IDE" / "resources" / "app" / "lib" / "backend" / "resources" / "arduino-cli.exe",
        Path("C:/Program Files/Arduino IDE/resources/app/lib/backend/resources/arduino-cli.exe"),
        Path("C:/Program Files/Arduino CLI/arduino-cli.exe"),
    ]

    for path in locations:
        if path.exists():
            return str(path)

    return None


# ============================================================
# Generate Arduino code
# ============================================================

def generate(filename):
    from pathlib import Path

    source_path = Path(filename)

    if not source_path.exists():
        raise FileNotFoundError(
            f"Python file not found: {filename}"
        )

    if source_path.suffix.lower() != ".py":
        raise ValueError(
            "PyDunio programs must use .py files."
        )

    print("Reading Python program:")
    print(f"  {source_path.name}")
    print()

    source = source_path.read_text(
        encoding="utf-8"
    )

    compiler = PyDunioCompiler()

    cpp = compiler.compile(source)

    # Create build/program-name/
    build_dir = (
        source_path.parent
        / "build"
        / source_path.stem
    )

    build_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # Create program-name.ino
    ino_file = (
        build_dir
        / f"{source_path.stem}.ino"
    )

    ino_file.write_text(
        cpp,
        encoding="utf-8"
    )

    print("SUCCESS:")
    print("Arduino code generated:")
    print(f"  {ino_file}")

    return ino_file

# ============================================================
# Compile Arduino code
# ============================================================

def compile_arduino(ino_file):
    import subprocess

    cli = find_arduino_cli()

    if not cli:
        print("\nERROR:")
        print("Arduino CLI was not found.")
        return False

    print("\nArduino CLI found:")
    print(f"  {cli}")

    print("\nCompiling Arduino program...")

    command = [
        cli,
        "compile",
        "--fqbn",
        "arduino:avr:uno",
        str(ino_file.parent)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("\nERROR:")
        print("Arduino compilation failed.")
        print(result.stderr or result.stdout)
        return False

    print("\nSUCCESS:")
    print("Arduino program compiled!")

    return True
# ============================================================
# Upload
# ============================================================

def upload_arduino(ino_file, port):
    import subprocess

    cli = find_arduino_cli()

    if not cli:
        print("\nERROR:")
        print("Arduino CLI was not found.")
        return False

    print("\nUploading Arduino program...")
    print(f"  Port: {port}")

    command = [
        cli,
        "upload",
        "-p",
        port,
        "--fqbn",
        "arduino:avr:uno",
        str(ino_file.parent)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("\nERROR:")
        print("Arduino upload failed.")
        print(result.stderr or result.stdout)
        return False

    print("\nSUCCESS:")
    print("UPLOAD COMPLETE!")

    return True


# ============================================================
# Help
# ============================================================

def help_message():

    print("""
PyDunio
=======

Python-first Arduino programming.

USAGE

    python -m pydunio.pydunio FILE

Generate Arduino code:

    python -m pydunio.pydunio blink.py

Compile:

    python -m pydunio.pydunio blink.py --compile

Compile and upload:

    python -m pydunio.pydunio blink.py --upload COM3

EXAMPLE

    from pydunio import *

    led = LED(13)

    while True:
        led.on()
        sleep(1000)

        led.off()
        sleep(1000)
""")


# ============================================================
# Main
# ============================================================

def main():

    header()

    if len(sys.argv) < 2:

        help_message()
        return

    if sys.argv[1] in (
        "--help",
        "-h"
    ):

        help_message()
        return

    filename = sys.argv[1]

    compile_requested = (
        "--compile"
        in sys.argv
    )

    upload_requested = (
        "--upload"
        in sys.argv
    )

    port = None

    if upload_requested:

        try:

            index = sys.argv.index(
                "--upload"
            )

            port = sys.argv[
                index + 1
            ]

        except IndexError:

            error(
                "You must specify a COM port.\n\n"
                "Example:\n"
                "  --upload COM3"
            )

            return

    # -----------------------------------------
    # Generate
    # -----------------------------------------

    try:

        print(
            f"Reading Python program:\n"
            f"  {filename}"
        )

        ino_file = generate(
            filename
        )

    except SyntaxError as e:

        error(
            "Your PyDunio program contains "
            "invalid Python syntax.\n\n"
            f"{e}"
        )

        return

    except FileNotFoundError as e:

        error(str(e))

        return

    except Exception as e:

        error(
            "PyDunio could not translate "
            "your program.\n\n"
            f"{type(e).__name__}: {e}"
        )

        return

    success(
        f"Arduino code generated:\n"
        f"  {ino_file}"
    )

    # -----------------------------------------
    # Compile
    # -----------------------------------------

    if compile_requested or upload_requested:

        if not compile_arduino(
            ino_file
        ):

            return

    # -----------------------------------------
    # Upload
    # -----------------------------------------

    if upload_requested:

        upload_arduino(
            ino_file,
            port
        )


if __name__ == "__main__":
    main()