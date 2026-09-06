# =========================
# PyDunio Sensors
# =========================

class Ultrasonic:

    def __init__(self, trigger, echo):
        self.trigger = trigger
        self.echo = echo

    def distance(self):
        pass


class Servo:

    def __init__(self, pin):
        self.pin = pin

    def angle(self, degrees):
        pass

    def write(self, degrees):
        pass


class HC05:

    def __init__(self, rx, tx, baud=9600):
        self.rx = rx
        self.tx = tx
        self.baud = baud

    def send(self, message):
        pass

    def available(self):
        pass

    def read(self):
        pass


class Button:

    def __init__(self, pin):
        self.pin = pin

    def pressed(self):
        pass


class LED:

    def __init__(self, pin):
        self.pin = pin

    def on(self):
        pass

    def off(self):
        pass

    def toggle(self):
        pass


class Potentiometer:

    def __init__(self, pin):
        self.pin = pin

    def read(self):
        pass


class LDR:

    def __init__(self, pin):
        self.pin = pin

    def read(self):
        pass