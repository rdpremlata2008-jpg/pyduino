PyDunio

Python-first Arduino programming.

PyDunio is a Python-first Arduino programming library and compiler. It allows you to write Arduino programs using simple Python-style code and converts them into Arduino C++.

Version

0.1.0

PyDunio is currently in early development.

What is PyDunio?

Arduino normally uses C/C++.

PyDunio lets you write Python-style programs such as:

from pydunio import *

led = Pin(13, OUTPUT)

while True:
    led.on()
    sleep(1000)

    led.off()
    sleep(1000)

PyDunio then converts the program into Arduino C++.

Features

PyDunio currently supports:

Digital pins
INPUT
OUTPUT
INPUT_PULLUP
HIGH
LOW
Pin
AnalogPin
PWM
LED
Buzzer
Ultrasonic
Servo
HC05
Button
Potentiometer
LDR
sleep()
blink()
while loops
if statements
Comparisons
Basic mathematics
Arduino C++ generation
Arduino CLI compilation
Arduino uploading
Installation
Download from GitHub

Go to the PyDunio GitHub repository:

https://github.com/rdpremlata2008-jpg/pyduino

Click:

Code → Download ZIP

Extract the ZIP file.

Open a terminal in the extracted project folder.

Install PyDunio:

python -m pip install -e .

Test the installation:

python -c "import pydunio; print('PyDunio installed!')"
Requirements
Python 3.9 or newer
Arduino board
USB cable
Arduino CLI for compiling and uploading
Project Structure
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
Command Line
Generate Arduino Code
python -m pydunio.pydunio blink.py

This converts your Python-style PyDunio program into Arduino C++.

Compile
python -m pydunio.pydunio blink.py --compile

This generates and compiles the Arduino program.

Upload
python -m pydunio.pydunio blink.py --upload COM3

Replace COM3 with your Arduino's actual COM port.

Find the port with:

arduino-cli board list
Digital Pins
Create a Pin
from pydunio import *

led = Pin(13, OUTPUT)
Turn ON
led.on()
Turn OFF
led.off()
Toggle
led.toggle()
Write HIGH
led.write(HIGH)
Write LOW
led.write(LOW)
Read a Pin
button = Pin(7, INPUT)

value = button.read()
Check HIGH
button = Pin(7, INPUT)

if button.high():
    pass
Check LOW
button = Pin(7, INPUT)

if button.low():
    pass
Pin Modes
OUTPUT
led = Pin(13, OUTPUT)
INPUT
button = Pin(7, INPUT)
INPUT_PULLUP
button = Pin(7, INPUT_PULLUP)
Constants
INPUT
OUTPUT
INPUT_PULLUP
HIGH
LOW
LED

Create an LED:

from pydunio import *

led = LED(13)

Turn it on:

led.on()

Turn it off:

led.off()

Toggle it:

led.toggle()
LED Blink
from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(1000)

    led.off()
    sleep(1000)
Fast Blink
from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(100)

    led.off()
    sleep(100)
Slow Blink
from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(2000)

    led.off()
    sleep(2000)
blink()

PyDunio also provides a blink() function:

from pydunio import *

led = LED(13)

blink(led, 500)

The second argument is the delay in milliseconds.

Analog Pins

Create an analog pin:

from pydunio import *

sensor = AnalogPin("A0")

value = sensor.read()
PWM

Create a PWM output:

from pydunio import *

motor = PWM(5)

motor.write(128)
Buzzer

Create a buzzer:

from pydunio import *

buzzer = Buzzer(8)

Beep:

buzzer.beep(1000, 500)

Stop:

buzzer.stop()
Ultrasonic Sensor

Create an ultrasonic sensor:

from pydunio import *

sensor = Ultrasonic(
    trigger=8,
    echo=9
)

Read distance:

distance = sensor.distance()
Servo

Create a servo:

from pydunio import *

servo = Servo(9)

Move it:

servo.angle(90)

or:

servo.write(90)
HC-05 Bluetooth

Create an HC-05:

from pydunio import *

bluetooth = HC05(
    rx=10,
    tx=11,
    baud=9600
)

Send a message:

bluetooth.send("Hello from PyDunio!")

Check if data is available:

if bluetooth.available():
    pass

Read data:

data = bluetooth.read()
Complete HC-05 Example
from pydunio import *

bluetooth = HC05(
    rx=10,
    tx=11,
    baud=9600
)

while True:
    bluetooth.send("Hello from PyDunio!")
    sleep(1000)
HC-05 Wiring
HC-05 VCC  → Arduino 5V
HC-05 GND  → Arduino GND
HC-05 TXD  → Arduino pin 10
HC-05 RXD  → Arduino pin 11

A voltage divider or suitable level shifter may be needed for the HC-05 RX input.

Button

Create a button:

from pydunio import *

button = Button(7)

Check if pressed:

if button.pressed():
    pass
Potentiometer

Create a potentiometer:

from pydunio import *

pot = Potentiometer("A0")

Read it:

value = pot.read()
LDR

Create an LDR:

from pydunio import *

ldr = LDR("A0")

Read it:

value = ldr.read()
Sleep

sleep() uses milliseconds.

sleep(1000)

1000 milliseconds = 1 second.

Example:

from pydunio import *

sleep(500)

500 milliseconds = 0.5 seconds.

While Loops

PyDunio supports while loops.

from pydunio import *

led = LED(13)

while True:
    led.on()
    sleep(500)

    led.off()
    sleep(500)
If Statements

PyDunio supports if statements.

from pydunio import *

button = Pin(7, INPUT_PULLUP)
led = LED(13)

while True:
    if button.low():
        led.on()
    else:
        led.off()
Comparisons

PyDunio supports:

==
!=
<
<=
>
>=

Example:

if distance < 20:
    buzzer.beep(1000, 200)
Mathematics

PyDunio supports:

+
-
*
/
%

Example:

value = 10 + 5

Another example:

value = 100 / 2
Multiple LEDs
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
Traffic Light Example
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
Button + LED
from pydunio import *

button = Pin(7, INPUT_PULLUP)
led = LED(13)

while True:
    if button.low():
        led.on()
    else:
        led.off()
Button + Buzzer
from pydunio import *

button = Pin(7, INPUT_PULLUP)
buzzer = Buzzer(8)

while True:
    if button.low():
        buzzer.beep(1000, 100)
    else:
        buzzer.stop()
Ultrasonic + Buzzer
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
Supported Classes
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
Pin API
Pin
Pin(pin, mode)

Methods:

.on()
.off()
.toggle()
.write(value)
.read()
.high()
.low()
LED API
LED(pin)

Methods:

.on()
.off()
.toggle()
Buzzer API
Buzzer(pin)

Methods:

.beep(frequency, duration)
.stop()
Ultrasonic API
Ultrasonic(trigger, echo)

Method:

.distance()
Servo API
Servo(pin)

Methods:

.angle(degrees)
.write(degrees)
HC-05 API
HC05(rx, tx, baud=9600)

Methods:

.send(message)
.available()
.read()
Button API
Button(pin)

Method:

.pressed()
AnalogPin API
AnalogPin(pin)

Method:

.read()
PWM API
PWM(pin)

Method:

.write(value)
Potentiometer API
Potentiometer(pin)

Method:

.read()
LDR API
LDR(pin)

Method:

.read()
Arduino Code Generation

PyDunio converts Python-style code into Arduino C++.

For example:

from pydunio import *

led = LED(13)

led.on()
sleep(1000)
led.off()

can generate Arduino code like:

void setup() {
  pinMode(13, OUTPUT);
}

void loop() {
  digitalWrite(13, HIGH);
  delay(1000);
  digitalWrite(13, LOW);
}
Arduino CLI

PyDunio can use Arduino CLI to compile and upload generated Arduino programs.

Check Arduino CLI:

arduino-cli version

Find connected boards:

arduino-cli board list

Compile a PyDunio program:

python -m pydunio.pydunio blink.py --compile

Upload:

python -m pydunio.pydunio blink.py --upload COM3
Examples

Example programs can be stored in:

examples/

Recommended examples:

examples/
├── blink.py
├── button.py
├── buzzer.py
├── ultrasonic.py
├── servo.py
└── hc05.py
Development Status

PyDunio is currently Version 0.1.0.

It is an early-stage project.

Some Python features are not supported yet.

Future versions may add:

More Arduino boards
More sensors
More actuators
Better compiler errors
Functions
for loops
More Python expressions
Serial communication
More Bluetooth features
Easier command-line usage
PyPI releases
Automatic Arduino CLI setup
Contributing

PyDunio is open source.

You can help by:

Reporting bugs
Suggesting features
Improving documentation
Adding examples
Adding hardware support
Improving the compiler
License

PyDunio is released under the MIT License.

See the LICENSE file for details.

GitHub

PyDunio:

https://github.com/rdpremlata2008-jpg/pyduino

Author

PyDunio

Python-first Arduino programming.

Made to make Arduino programming easier for Python users.