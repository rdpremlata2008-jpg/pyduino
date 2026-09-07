import argparse
import shutil
import subprocess
from pathlib import Path

from .compiler import PyDunioCompiler


VERSION = "0.1.2"


def find_arduino_cli():
    cli = shutil.which("arduino-cli")

    if cli:
        return cli

    possible_paths = [
        Path.home()
        / "AR"
        / "Arduino IDE"
        / "resources"
        / "app"
        / "lib"
        / "backend"
        / "resources"
        / "arduino-cli.exe"
    ]

    for path in possible_paths:
        if path.exists():
            return str(path)

    raise FileNotFoundError(
        "Arduino CLI was not found."
    )


def generate(filename):
    filename = Path(filename)

    if not filename.exists():
        raise FileNotFoundError(
            f"File not found: {filename}"
        )

    print()
    print("Reading Python program:")
    print(f"  {filename}")

    source = filename.read_text(
        encoding="utf-8"
    )

    compiler = PyDunioCompiler()

    cpp = compiler.compile(source)

    build_dir = (
        Path("build")
        / filename.stem
    )

    build_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    ino_file = (
        build_dir
        / f"{filename.stem}.ino"
    )

    ino_file.write_text(
        cpp,
        encoding="utf-8"
    )

    print()
    print("SUCCESS:")
    print("Arduino code generated:")
    print(f"  {ino_file}")

    return ino_file


def compile_arduino(ino_file):
    cli = find_arduino_cli()

    print()
    print("Arduino CLI found:")
    print(f"  {cli}")

    print()
    print("Compiling Arduino program...")

    result = subprocess.run(
        [
            cli,
            "compile",
            "--fqbn",
            "arduino:avr:uno",
            str(ino_file.parent)
        ]
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Arduino compilation failed."
        )

    print()
    print("SUCCESS:")
    print("Arduino program compiled!")


def upload_arduino(ino_file, port):
    cli = find_arduino_cli()

    print()
    print("Uploading Arduino program...")
    print(f"  Port: {port}")

    result = subprocess.run(
        [
            cli,
            "upload",
            "-p",
            port,
            "--fqbn",
            "arduino:avr:uno",
            str(ino_file.parent)
        ]
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Arduino upload failed."
        )

    print()
    print("SUCCESS:")
    print("UPLOAD COMPLETE!")


def serial_monitor(port, baud=9600):
    cli = find_arduino_cli()

    print()
    print("==============================")
    print(" PyDunio Serial Monitor")
    print("==============================")
    print()
    print(f"Port: {port}")
    print(f"Baud: {baud}")
    print()
    print("Arduino is running.")
    print("Press Ctrl+C to stop the monitor.")
    print()

    try:
        subprocess.run(
            [
                cli,
                "monitor",
                "-p",
                port,
                "--config",
                f"baudrate={baud}"
            ]
        )

    except KeyboardInterrupt:
        print()
        print("Serial monitor stopped.")


def run_arduino(ino_file, port):
    # Compile
    compile_arduino(ino_file)

    # Upload
    upload_arduino(
        ino_file,
        port
    )

    # Start live serial monitor
    serial_monitor(
        port,
        9600
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "PyDunio - "
            "Python-first Arduino programming"
        )
    )

    parser.add_argument(
        "filename",
        help="PyDunio Python file"
    )

    parser.add_argument(
        "--compile",
        action="store_true",
        help="Generate and compile Arduino C++"
    )

    parser.add_argument(
        "--upload",
        metavar="PORT",
        help=(
            "Generate, compile and "
            "upload to Arduino"
        )
    )

    parser.add_argument(
        "--run",
        metavar="PORT",
        help=(
            "Generate, compile, upload "
            "and start serial monitor"
        )
    )

    args = parser.parse_args()

    print()
    print("PyDunio")
    print("=======")
    print(f"Version {VERSION}")

    # -------------------------------
    # Generate
    # -------------------------------

    ino_file = generate(
        args.filename
    )

    # -------------------------------
    # Compile
    # -------------------------------

    if args.compile:
        compile_arduino(
            ino_file
        )

    # -------------------------------
    # Upload
    # -------------------------------

    if args.upload:
        compile_arduino(
            ino_file
        )

        upload_arduino(
            ino_file,
            args.upload
        )

    # -------------------------------
    # Run
    # -------------------------------

    if args.run:
        run_arduino(
            ino_file,
            args.run
        )


if __name__ == "__main__":
    main()