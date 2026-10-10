# PyDunio

Python-first Arduino programming.

PyDunio is a lightweight Python-style library and compiler for Arduino projects. It lets you write simple Python code for pins, sensors, LEDs, buzzers, and more, and it generates Arduino C++ code you can compile and upload.

## Version

0.2.1

## What is PyDunio?

Arduino development is usually done in C/C++. PyDunio makes it easier to prototype with Python-like syntax for simple hardware tasks.

Example:

```python
from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(1000)
    led.off()
    sleep(1000)
```

This can be converted into Arduino C++ and compiled for upload.

## Features

PyDunio currently supports:

- Digital pins and pin modes
- INPUT / OUTPUT / INPUT_PULLUP
- HIGH / LOW constants
- Pin, AnalogPin, PWM
- LED, Buzzer, Ultrasonic, Servo, HC05
- Button, Potentiometer, LDR
- sleep(), blink()
- while loops and if statements
- basic comparisons and arithmetic
- Arduino C++ generation
- Arduino CLI compilation and upload

## Installation

From a terminal in the project folder:

```bash
python -m pip install -e .
```

Verify installation:

```bash
python -c "import pydunio; print('PyDunio installed!')"
```

## Requirements

- Python 3.9+
- Arduino board
- USB cable
- Arduino CLI

## Project Structure

```text
pyduino/
├── pydunio/
│   ├── __init__.py
│   ├── __main__.py
│   ├── compiler.py
│   ├── core.py
│   ├── pyduino.py
│   └── sensors.py
├── README.md
├── LICENSE
├── .gitignore
├── pyproject.toml
└── .github/
    └── workflows/
        └── python-publish.yml
```

## Usage

Generate Arduino code:

```bash
python -m pydunio.pyduino blink.py
```

Compile:

```bash
python -m pydunio.pyduino blink.py --compile
```

Upload to Arduino:

```bash
python -m pydunio.pyduino blink.py --upload COM3
```

Replace `COM3` with your actual Arduino port.

## Example: LED Blink

```python
from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(1000)
    led.off()
    sleep(1000)
```

## Example: Button + LED

```python
from pydunio import *

button = Pin(7, INPUT_PULLUP)
led = LED(13)

while True:
    if button.low():
        led.on()
    else:
        led.off()
```

## Arduino CLI

Check the CLI version:

```bash
arduino-cli version
```

List connected boards:

```bash
arduino-cli board list
```

## Publishing

This project is configured for PyPI publishing with GitHub Actions using OIDC / trusted publisher authentication.

## Development Status

PyDunio is an early-stage project. It is intended for learning, prototyping, and simple Arduino workflows. Future work may include:

- more board support
- richer compiler features
- better error handling
- more hardware abstractions
- more examples and documentation

## Contributing

Contributions are welcome. You can help by:

- reporting bugs
- suggesting features
- improving examples
- improving compiler support
- improving docs

## License

PyDunio is released under the MIT License.

See `LICENSE` for details.

## GitHub

- Repository: https://github.com/rdpremlata2008-jpg/pyduino
