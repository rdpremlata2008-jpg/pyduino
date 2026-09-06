# PyDunio

**Python-first Arduino programming.**

PyDunio is a Python-first Arduino programming library and compiler. It allows you to write Arduino programs using simple Python-style code and converts them into Arduino C++.

## Version

**0.1.0**

PyDunio is currently in early development.

---

# What is PyDunio?

Arduino normally uses C/C++.

PyDunio lets you write Python-style programs such as:

```python
from pydunio import *

led = Pin(13, OUTPUT)

while True:
    led.on()
    sleep(1000)

    led.off()
    sleep(1000)
```

PyDunio then converts the program into Arduino C++.

---

# Features

PyDunio currently supports:

* Digital pins
* `INPUT`
* `OUTPUT`
* `INPUT_PULLUP`
* `HIGH`
* `LOW`
* `Pin`
* `AnalogPin`
* `PWM`
* `LED`
* `Buzzer`
* `Ultrasonic`
* `Servo`
* `HC05`
* `Button`
* `Potentiometer`
* `LDR`
* `sleep()`
* `blink()`
* `while` loops
* `if` statements
* Comparisons
* Basic mathematics
* Arduino C++ generation
* Arduino CLI compilation
* Arduino uploading

---

# Installation

## Download from GitHub

Go to the PyDunio GitHub repository:

[https://github.com/rdpremlata2008-jpg/pyduino](https://github.com/rdpremlata2008-jpg/pyduino)

Click:

**Code → Download ZIP**

Extract the ZIP file.

Open a terminal in the extracted project folder.

Install PyDunio:

```powershell
python -m pip install -e .
```

Test the installation:

```powershell
python -c "import pydunio; print('PyDunio installed!')"
```

---

# Requirements

* Python 3.9 or newer
* Arduino board
* USB cable
* Arduino CLI for compiling and uploading

---

# Project Structure

```text
pyduino/
│
├── pydunio/
│   ├── __init__.py
│   ├── pydunio.py
│   ├── compiler.py
│   ├── core.py
│   └── sensors.py
│
├── examples/
│   └── blink.py
│
├── README.md
├── LICENSE
├── .gitignore
└── pyproject.toml
```

---

# Command Line

## Generate Arduino Code

```powershell
python -m pydunio.pydunio blink.py
```

This converts your Python-style PyDunio program into Arduino C++.

---

## Compile

```powershell
python -m pydunio.pydunio blink.py --compile
```

This generates and compiles the Arduino program.

---

## Upload

```powershell
python -m pydunio.pydunio blink.py --upload COM3
```

Replace `COM3` with your Arduino's actual COM port.

Find the port with:

```powershell
arduino-cli board list
```

---

# Digital Pins

## Create a Pin

```python
from pydunio import *

led = Pin(13, OUTPUT)
```

---

## Turn ON

```python
led.on()
```

---

## Turn OFF

```python
led.off()
```

---

## Toggle

```python
led.toggle()
```

---

## Write HIGH

```python
led.write(HIGH)
```

---

## Write LOW

```python
led.write(LOW)
```

---

## Read a Pin

```python
button = Pin(7, INPUT)

value = button.read()
```

---

## Check HIGH

```python
button = Pin(7, INPUT)

if button.high():
    pass
```

---

## Check LOW

```python
button = Pin(7, INPUT)

if button.low():
    pass
```

---

# Pin Modes

## OUTPUT

```python
led = Pin(13, OUTPUT)
```

## INPUT

```python
button = Pin(7, INPUT)
```

## INPUT_PULLUP

```python
button = Pin(7, INPUT_PULLUP)
```

---

# Constants

```python
INPUT
OUTPUT
INPUT_PULLUP
HIGH
LOW
```

---

# LED

Create an LED:

```python
from pydunio import *

led = LED(13)
```

Turn it on:

```python
led.on()
```

Turn it off:

```python
led.off()
```

Toggle it:

```python
led.toggle()
```

---

# LED Blink

```python
from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(1000)

    led.off()
    sleep(1000)
```

---

# Fast Blink

```python
from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(100)

    led.off()
    sleep(100)
```

---

# Slow Blink

```python
from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(2000)

    led.off()
    sleep(2000)
```

---

# blink()

PyDunio also provides a `blink()` function:

```python
from pydunio import *

led = LED(13)

blink(led, 500)
```

The second argument is the delay in milliseconds.

---

# Analog Pins

Create an analog pin:

```python
from pydunio import *

sensor = AnalogPin("A0")

value = sensor.read()
```

---

# PWM

Create a PWM output:

```python
from pydunio import *

motor = PWM(5)

motor.write(128)
```

---

# Buzzer

Create a buzzer:

```python
from pydunio import *

buzzer = Buzzer(8)
```

Beep:

```python
buzzer.beep(1000, 500)
```

Stop:

```python
buzzer.stop()
```

---

# Ultrasonic Sensor

Create an ultrasonic sensor:

```python
from pydunio import *

sensor = Ultrasonic(
    trigger=8,
    echo=9
)
```

Read distance:

```python
distance = sensor.distance()
```

---

# Servo

Create a servo:

```python
from pydunio import *

servo = Servo(9)
```

Move it:

```python
servo.angle(90)
```

or:

```python
servo.write(90)
```

---

# HC-05 Bluetooth

Create an HC-05:

```python
from pydunio import *

bluetooth = HC05(
    rx=10,
    tx=11,
    baud=9600
)
```

Send a message:

```python
bluetooth.send("Hello from PyDunio!")
```

Check if data is available:

```python
if bluetooth.available():
    pass
```

Read data:

```python
data = bluetooth.read()
```

## Complete HC-05 Example

```python
from pydunio import *

bluetooth = HC05(
    rx=10,
    tx=11,
    baud=9600
)

while True:
    bluetooth.send("Hello from PyDunio!")
    sleep(1000)
```

### HC-05 Wiring

```text
HC-05 VCC  → Arduino 5V
HC-05 GND  → Arduino GND
HC-05 TXD  → Arduino pin 10
HC-05 RXD  → Arduino pin 11
```

A voltage divider or suitable level shifter may be needed for the HC-05 RX input.

---

# Button

Create a button:

```python
from pydunio import *

button = Button(7)
```

Check if pressed:

```python
if button.pressed():
    pass
```

---

# Potentiometer

Create a potentiometer:

```python
from pydunio import *

pot = Potentiometer("A0")
```

Read it:

```python
value = pot.read()
```

---

# LDR

Create an LDR:

```python
from pydunio import *

ldr = LDR("A0")
```

Read it:

```python
value = ldr.read()
```

---

# Sleep

`sleep()` uses milliseconds.

```python
sleep(1000)
```

1000 milliseconds = 1 second.

Example:

```python
from pydunio import *

sleep(500)
```

500 milliseconds = 0.5 seconds.

---

# While Loops

PyDunio supports `while` loops.

```python
from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(500)

    led.off()
    sleep(500)
```

---

# If Statements

PyDunio supports `if` statements.

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

---

# Comparisons

PyDunio supports:

```text
==
!=
<
<=
>
>=
```

Example:

```python
if distance < 20:
    buzzer.beep(1000, 200)
```

---

# Mathematics

PyDunio supports:

```text
+
-
*
/
%
```

Example:

```python
value = 10 + 5
```

Another example:

```python
value = 100 / 2
```

---

# Multiple LEDs

```python
from pydunio import *

led1 = LED(10)
led2 = LED(11)
led3 = LED(12)

while True:
    led1.on()
    led2.off()
    led3.off()

    sleep(500)

    led1.off()
    led2.on()
    led3.off()

    sleep(500)

    led1.off()
    led2.off()
    led3.on()

    sleep(500)
```

---

# Traffic Light Example

```python
from pydunio import *

red = LED(11)
yellow = LED(12)
green = LED(13)

while True:
    red.on()
    yellow.off()
    green.off()
    sleep(2000)

    red.off()
    yellow.on()
    green.off()
    sleep(1000)

    red.off()
    yellow.off()
    green.on()
    sleep(2000)
```

---

# Button + LED

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

---

# Button + Buzzer

```python
from pydunio import *

button = Pin(7, INPUT_PULLUP)
buzzer = Buzzer(8)

while True:
    if button.low():
        buzzer.beep(1000, 100)
    else:
        buzzer.stop()
```

---

# Ultrasonic + Buzzer

```python
from pydunio import *

sensor = Ultrasonic(
    trigger=8,
    echo=9
)

buzzer = Buzzer(10)

while True:
    distance = sensor.distance()

    if distance < 20:
        buzzer.beep(1000, 100)
    else:
        buzzer.stop()

    sleep(100)
```

---

# Supported Classes

```text
Pin
AnalogPin
PWM
Buzzer
Ultrasonic
Servo
HC05
Button
LED
Potentiometer
LDR
```

---

# Pin API

## Pin

```python
Pin(pin, mode)
```

Methods:

```python
.on()
.off()
.toggle()
.write(value)
.read()
.high()
.low()
```

---

# LED API

```python
LED(pin)
```

Methods:

```python
.on()
.off()
.toggle()
```

---

# Buzzer API

```python
Buzzer(pin)
```

Methods:

```python
.beep(frequency, duration)
.stop()
```

---

# Ultrasonic API

```python
Ultrasonic(trigger, echo)
```

Method:

```python
.distance()
```

---

# Servo API

```python
Servo(pin)
```

Methods:

```python
.angle(degrees)
.write(degrees)
```

---

# HC-05 API

```python
HC05(rx, tx, baud=9600)
```

Methods:

```python
.send(message)
.available()
.read()
```

---

# Button API

```python
Button(pin)
```

Method:

```python
.pressed()
```

---

# AnalogPin API

```python
AnalogPin(pin)
```

Method:

```python
.read()
```

---

# PWM API

```python
PWM(pin)
```

Method:

```python
.write(value)
```

---

# Potentiometer API

```python
Potentiometer(pin)
```

Method:

```python
.read()
```

---

# LDR API

```python
LDR(pin)
```

Method:

```python
.read()
```

---

# Arduino Code Generation

PyDunio converts Python-style code into Arduino C++.

For example:

```python
from pydunio import *

led = LED(13)

led.on()
sleep(1000)
led.off()
```

can generate Arduino code like:

```cpp
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
}
```

---

# Arduino CLI

PyDunio can use Arduino CLI to compile and upload generated Arduino programs.

Check Arduino CLI:

```powershell
arduino-cli version
```

Find connected boards:

```powershell
arduino-cli board list
```

Compile a PyDunio program:

```powershell
python -m pydunio.pydunio blink.py --compile
```

Upload:

```powershell
python -m pydunio.pydunio blink.py --upload COM3
```

---

# Examples

Example programs can be stored in:

```text
examples/
```

Recommended examples:

```text
examples/
├── blink.py
├── button.py
├── buzzer.py
├── ultrasonic.py
├── servo.py
└── hc05.py
```

---

# Development Status

PyDunio is currently **Version 0.1.0**.

It is an early-stage project.

Some Python features are not supported yet.

Future versions may add:

* More Arduino boards
* More sensors
* More actuators
* Better compiler errors
* Functions
* `for` loops
* More Python expressions
* Serial communication
* More Bluetooth features
* Easier command-line usage
* PyPI releases
* Automatic Arduino CLI setup

---

# Contributing

PyDunio is open source.

You can help by:

* Reporting bugs
* Suggesting features
* Improving documentation
* Adding examples
* Adding hardware support
* Improving the compiler

---

# License

PyDunio is released under the **MIT License**.

See the `LICENSE` file for details.

---

# GitHub

PyDunio:

[https://github.com/rdpremlata2008-jpg/pyduino](https://github.com/rdpremlata2008-jpg/pyduino)

---

# Author

PyDunio

**Python-first Arduino programming.**

Made to make Arduino programming easier for Python users.
