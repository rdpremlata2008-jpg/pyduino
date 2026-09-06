# =========================
# PyDunio Core
# =========================

INPUT = "INPUT"
OUTPUT = "OUTPUT"
INPUT_PULLUP = "INPUT_PULLUP"

HIGH = 1
LOW = 0


class Pin:
    def __init__(self, number, mode):
        self.number = number
        self.mode = mode

    def on(self):
        pass

    def off(self):
        pass

    def toggle(self):
        pass

    def write(self, value):
        pass

    def read(self):
        pass

    def high(self):
        pass

    def low(self):
        pass


class AnalogPin:
    def __init__(self, pin):
        self.pin = pin

    def read(self):
        pass


class PWM:
    def __init__(self, pin):
        self.pin = pin

    def write(self, value):
        pass


def sleep(milliseconds):
    pass


def blink(pin, milliseconds=500):
    pass


class Buzzer:
    def __init__(self, pin):
        self.pin = pin

    def beep(self, frequency=1000, duration=0):
        pass

    def stop(self):
        pass