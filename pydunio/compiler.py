"""
PyDunio Compiler

Converts Python-style PyDunio programs
into Arduino C++.
"""

import ast


class PyDunioCompiler:

    def __init__(self):

        self.setup = []
        self.loop = []

        self.variables = {}

        self.includes = set()

        self.indent = 0

    # ==========================================================
    # MAIN COMPILER
    # ==========================================================

    def compile(self, source: str):

        tree = ast.parse(source)

        self.setup = []
        self.loop = []
        self.variables = {}
        self.includes = set()

        for node in tree.body:
            self.compile_statement(
                node,
                self.loop
            )

        return self.generate_cpp()

    # ==========================================================
    # STATEMENTS
    # ==========================================================

    def compile_statement(self, node, output):

        # --------------------------------------
        # import
        # --------------------------------------

        if isinstance(node, ast.ImportFrom):

            if node.module == "pydunio":

                return

            return

        # --------------------------------------
        # assignment
        # --------------------------------------

        if isinstance(node, ast.Assign):

            self.compile_assignment(
                node,
                output
            )

            return

        # --------------------------------------
        # expression
        # --------------------------------------

        if isinstance(node, ast.Expr):

            result = self.expression(
                node.value
            )

            if result:
                output.append(
                    result
                )

            return

        # --------------------------------------
        # while
        # --------------------------------------

        if isinstance(node, ast.While):

            self.compile_while(
                node,
                output
            )

            return

        # --------------------------------------
        # if
        # --------------------------------------

        if isinstance(node, ast.If):

            self.compile_if(
                node,
                output
            )

            return

        # --------------------------------------
        # pass
        # --------------------------------------

        if isinstance(node, ast.Pass):

            return

        raise SyntaxError(
            f"PyDunio does not support "
            f"{type(node).__name__} yet."
        )

    # ==========================================================
    # ASSIGNMENT
    # ==========================================================

    def compile_assignment(self, node, output):

        if not node.targets:
            return

        target = node.targets[0]

        if not isinstance(
            target,
            ast.Name
        ):
            raise SyntaxError(
                "Only simple variables are supported."
            )

        name = target.id

        value = node.value

        # --------------------------------------
        # Pin(...)
        # --------------------------------------

        if self.is_constructor(
            value,
            "Pin"
        ):

            pin = self.expression(
                value.args[0]
            )

            mode = self.expression(
                value.args[1]
            )

            self.variables[name] = {
                "type": "Pin",
                "pin": pin
            }

            self.setup.append(
                f"pinMode({pin}, {mode});"
            )

            return

        # --------------------------------------
        # LED(...)
        # --------------------------------------

        if self.is_constructor(
            value,
            "LED"
        ):

            pin = self.expression(
                value.args[0]
            )

            self.variables[name] = {
                "type": "LED",
                "pin": pin
            }

            self.setup.append(
                f"pinMode({pin}, OUTPUT);"
            )

            return

        # --------------------------------------
        # Buzzer(...)
        # --------------------------------------

        if self.is_constructor(
            value,
            "Buzzer"
        ):

            pin = self.expression(
                value.args[0]
            )

            self.variables[name] = {
                "type": "Buzzer",
                "pin": pin
            }

            self.setup.append(
                f"pinMode({pin}, OUTPUT);"
            )

            return

        # --------------------------------------
        # Ultrasonic(...)
        # --------------------------------------

        if self.is_constructor(
            value,
            "Ultrasonic"
        ):

            trigger = self.keyword_or_arg(
                value,
                "trigger",
                0
            )

            echo = self.keyword_or_arg(
                value,
                "echo",
                1
            )

            self.variables[name] = {
                "type": "Ultrasonic",
                "trigger": self.expression(trigger),
                "echo": self.expression(echo)
            }

            self.setup.append(
                f"pinMode({self.expression(trigger)}, OUTPUT);"
            )

            self.setup.append(
                f"pinMode({self.expression(echo)}, INPUT);"
            )

            return

        # --------------------------------------
        # Servo(...)
        # --------------------------------------

        if self.is_constructor(
            value,
            "Servo"
        ):

            pin = self.expression(
                value.args[0]
            )

            self.includes.add(
                "#include <Servo.h>"
            )

            self.variables[name] = {
                "type": "Servo",
                "pin": pin
            }

            self.setup.append(
                f"{name}.attach({pin});"
            )

            return

        # --------------------------------------
        # HC05(...)
        # --------------------------------------

        if self.is_constructor(
            value,
            "HC05"
        ):

            rx = self.keyword_or_arg(
                value,
                "rx",
                0
            )

            tx = self.keyword_or_arg(
                value,
                "tx",
                1
            )

            baud = self.keyword_or_arg(
                value,
                "baud",
                2,
                default=9600
            )

            self.includes.add(
                "#include <SoftwareSerial.h>"
            )

            self.variables[name] = {
                "type": "HC05",
                "rx": self.expression(rx),
                "tx": self.expression(tx)
            }

            self.setup.append(
                f"{name}.begin({self.expression(baud)});"
            )

            return

        # --------------------------------------
        # Normal variable
        # --------------------------------------

        expression = self.expression(
            value
        )

        self.variables[name] = {
            "type": "variable"
        }

        output.append(
            f"auto {name} = {expression};"
        )

    # ==========================================================
    # WHILE
    # ==========================================================

    def compile_while(self, node, output):

        condition = self.expression(
            node.test
        )

        output.append(
            f"while ({condition}) {{"
        )

        body = []

        for statement in node.body:

            self.compile_statement(
                statement,
                body
            )

        for line in body:

            output.append(
                "  " + line
            )

        output.append(
            "}"
        )

    # ==========================================================
    # IF
    # ==========================================================

    def compile_if(self, node, output):

        condition = self.expression(
            node.test
        )

        output.append(
            f"if ({condition}) {{"
        )

        body = []

        for statement in node.body:

            self.compile_statement(
                statement,
                body
            )

        for line in body:

            output.append(
                "  " + line
            )

        output.append(
            "}"
        )

        if node.orelse:

            output.append(
                "else {"
            )

            else_body = []

            for statement in node.orelse:

                self.compile_statement(
                    statement,
                    else_body
                )

            for line in else_body:

                output.append(
                    "  " + line
                )

            output.append(
                "}"
            )

    # ==========================================================
    # EXPRESSIONS
    # ==========================================================

    def expression(self, node):

        # --------------------------------------
        # Constants
        # --------------------------------------

        if isinstance(
            node,
            ast.Constant
        ):

            if node.value is True:
                return "true"

            if node.value is False:
                return "false"

            if node.value is None:
                return "nullptr"

            if isinstance(
                node.value,
                str
            ):
                escaped = (
                    node.value
                    .replace("\\", "\\\\")
                    .replace('"', '\\"')
                )

                return f'"{escaped}"'

            return str(
                node.value
            )

        # --------------------------------------
        # Name
        # --------------------------------------

        if isinstance(
            node,
            ast.Name
        ):

            constants = {
                "HIGH": "HIGH",
                "LOW": "LOW",
                "INPUT": "INPUT",
                "OUTPUT": "OUTPUT",
                "INPUT_PULLUP":
                    "INPUT_PULLUP"
            }

            return constants.get(
                node.id,
                node.id
            )

        # --------------------------------------
        # Comparison
        # --------------------------------------

        if isinstance(
            node,
            ast.Compare
        ):

            left = self.expression(
                node.left
            )

            operators = {
                ast.Eq: "==",
                ast.NotEq: "!=",
                ast.Lt: "<",
                ast.LtE: "<=",
                ast.Gt: ">",
                ast.GtE: ">="
            }

            parts = []

            for operator, comparator in zip(
                node.ops,
                node.comparators
            ):

                op = operators.get(
                    type(operator)
                )

                if op is None:
                    raise SyntaxError(
                        "Unsupported comparison."
                    )

                right = self.expression(
                    comparator
                )

                parts.append(
                    f"{left} {op} {right}"
                )

                left = right

            return " && ".join(parts)

        # --------------------------------------
        # Binary operations
        # --------------------------------------

        if isinstance(
            node,
            ast.BinOp
        ):

            operators = {
                ast.Add: "+",
                ast.Sub: "-",
                ast.Mult: "*",
                ast.Div: "/",
                ast.Mod: "%"
            }

            operator = operators.get(
                type(node.op)
            )

            if operator is None:
                raise SyntaxError(
                    "Unsupported math operator."
                )

            left = self.expression(
                node.left
            )

            right = self.expression(
                node.right
            )

            return (
                f"({left} "
                f"{operator} "
                f"{right})"
            )

        # --------------------------------------
        # Unary operations
        # --------------------------------------

        if isinstance(
            node,
            ast.UnaryOp
        ):

            operand = self.expression(
                node.operand
            )

            if isinstance(
                node.op,
                ast.USub
            ):
                return f"-{operand}"

            if isinstance(
                node.op,
                ast.Not
            ):
                return f"!({operand})"

        # --------------------------------------
        # Function calls
        # --------------------------------------

        if isinstance(
            node,
            ast.Call
        ):

            return self.compile_call(
                node
            )

        return ""

    # ==========================================================
    # FUNCTION / METHOD CALLS
    # ==========================================================

    def compile_call(self, node):

        # --------------------------------------
        # sleep(...)
        # --------------------------------------

        if (
            isinstance(
                node.func,
                ast.Name
            )
            and node.func.id == "sleep"
        ):

            value = self.expression(
                node.args[0]
            )

            return f"delay({value});"

        # --------------------------------------
        # blink(...)
        # --------------------------------------

        if (
            isinstance(
                node.func,
                ast.Name
            )
            and node.func.id == "blink"
        ):

            pin = self.expression(
                node.args[0]
            )

            duration = (
                self.expression(
                    node.args[1]
                )
                if len(node.args) > 1
                else "500"
            )

            if isinstance(
                node.args[0],
                ast.Name
            ):

                variable = node.args[0].id

                if variable in self.variables:

                    info = self.variables[
                        variable
                    ]

                    if info["type"] in (
                        "Pin",
                        "LED"
                    ):

                        pin = info["pin"]

            return (
                f"digitalWrite({pin}, HIGH); "
                f"delay({duration}); "
                f"digitalWrite({pin}, LOW); "
                f"delay({duration});"
            )

        # --------------------------------------
        # Object.method(...)
        # --------------------------------------

        if isinstance(
            node.func,
            ast.Attribute
        ):

            obj = node.func.value

            if not isinstance(
                obj,
                ast.Name
            ):
                return ""

            object_name = obj.id
            method = node.func.attr

            if object_name not in self.variables:
                return ""

            info = self.variables[
                object_name
            ]

            # ==========================
            # Pin / LED
            # ==========================

            if info["type"] in (
                "Pin",
                "LED"
            ):

                pin = info["pin"]

                if method == "on":

                    return (
                        f"digitalWrite("
                        f"{pin}, HIGH);"
                    )

                if method == "off":

                    return (
                        f"digitalWrite("
                        f"{pin}, LOW);"
                    )

                if method == "toggle":

                    return (
                        f"digitalWrite("
                        f"{pin}, "
                        f"!digitalRead({pin}));"
                    )

                if method == "write":

                    value = self.expression(
                        node.args[0]
                    )

                    return (
                        f"digitalWrite("
                        f"{pin}, {value});"
                    )

                if method == "read":

                    return (
                        f"digitalRead({pin})"
                    )

                if method == "high":

                    return (
                        f"digitalRead({pin}) == HIGH"
                    )

                if method == "low":

                    return (
                        f"digitalRead({pin}) == LOW"
                    )

            # ==========================
            # Buzzer
            # ==========================

            if info["type"] == "Buzzer":

                pin = info["pin"]

                if method == "beep":

                    frequency = self.expression(
                        node.args[0]
                    )

                    if len(node.args) > 1:

                        duration = self.expression(
                            node.args[1]
                        )

                        return (
                            f"tone({pin}, "
                            f"{frequency}, "
                            f"{duration});"
                        )

                    return (
                        f"tone({pin}, "
                        f"{frequency});"
                    )

                if method == "stop":

                    return (
                        f"noTone({pin});"
                    )

            # ==========================
            # Servo
            # ==========================

            if info["type"] == "Servo":

                if method in (
                    "angle",
                    "write"
                ):

                    angle = self.expression(
                        node.args[0]
                    )

                    return (
                        f"{object_name}.write("
                        f"{angle});"
                    )

            # ==========================
            # Ultrasonic
            # ==========================

            if info["type"] == "Ultrasonic":

                if method == "distance":

                    trigger = info[
                        "trigger"
                    ]

                    echo = info[
                        "echo"
                    ]

                    return (
                        f"ultrasonicDistance("
                        f"{trigger}, {echo})"
                    )

            # ==========================
            # HC-05
            # ==========================

            if info["type"] == "HC05":

                if method == "send":

                    message = self.expression(
                        node.args[0]
                    )

                    return (
                        f"{object_name}.println("
                        f"{message});"
                    )

                if method == "available":

                    return (
                        f"{object_name}.available()"
                    )

                if method == "read":

                    return (
                        f"{object_name}.read()"
                    )

        return ""

    # ==========================================================
    # HELPERS
    # ==========================================================

    def is_constructor(
        self,
        node,
        name
    ):

        return (
            isinstance(
                node,
                ast.Call
            )
            and isinstance(
                node.func,
                ast.Name
            )
            and node.func.id == name
        )

    def keyword_or_arg(
        self,
        call,
        name,
        index,
        default=None
    ):

        for keyword in call.keywords:

            if keyword.arg == name:
                return keyword.value

        if len(call.args) > index:
            return call.args[index]

        if default is not None:

            return ast.Constant(
                value=default
            )

        raise SyntaxError(
            f"Missing argument: {name}"
        )

    # ==========================================================
    # GENERATE C++
    # ==========================================================

    def generate_cpp(self):

        lines = []

        lines.append(
            "// =================================="
        )

        lines.append(
            "// Generated by PyDunio"
        )

        lines.append(
            "// =================================="
        )

        lines.append("")

        # Libraries
        for include in sorted(
            self.includes
        ):

            lines.append(
                include
            )

        if self.includes:
            lines.append("")

        # Ultrasonic helper
        ultrasonic_used = any(
            info["type"] == "Ultrasonic"
            for info in self.variables.values()
        )

        if ultrasonic_used:

            lines.append(
                "long ultrasonicDistance("
                "int trigger, int echo) {"
            )

            lines.append(
                "  digitalWrite(trigger, LOW);"
            )

            lines.append(
                "  delayMicroseconds(2);"
            )

            lines.append(
                "  digitalWrite(trigger, HIGH);"
            )

            lines.append(
                "  delayMicroseconds(10);"
            )

            lines.append(
                "  digitalWrite(trigger, LOW);"
            )

            lines.append(
                "  long duration = "
                "pulseIn(echo, HIGH);"
            )

            lines.append(
                "  return duration / 58;"
            )

            lines.append(
                "}"
            )

            lines.append("")

        # Servo objects
        for name, info in self.variables.items():

            if info["type"] == "Servo":

                lines.append(
                    f"Servo {name};"
                )

        # HC05 objects
        for name, info in self.variables.items():

            if info["type"] == "HC05":

                lines.append(
                    f"SoftwareSerial "
                    f"{name}("
                    f"{info['rx']}, "
                    f"{info['tx']});"
                )

        if any(
            info["type"] in (
                "Servo",
                "HC05"
            )
            for info in self.variables.values()
        ):

            lines.append("")

        # setup
        lines.append(
            "void setup() {"
        )

        for line in self.setup:

            lines.append(
                "  " + line
            )

        lines.append(
            "}"
        )

        lines.append("")

        # loop
        lines.append(
            "void loop() {"
        )

        for line in self.loop:

            lines.append(
                "  " + line
            )

        lines.append(
            "}"
        )

        return "\n".join(lines)


### Test program


from pydunio import *

bluetooth = HC05(
    rx=10,
    tx=11,
    baud=9600
)

while True:

    if bluetooth.available():
        message = bluetooth.read()
        bluetooth.send(message)

    sleep(10)
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="PyDunio - Python-first Arduino programming"
    )

    parser.add_argument(
        "filename",
        help="PyDunio Python file to compile"
    )

    parser.add_argument(
        "--compile",
        action="store_true",
        help="Generate and compile Arduino C++"
    )

    parser.add_argument(
        "--upload",
        metavar="PORT",
        help="Generate, compile and upload to Arduino"
    )

    args = parser.parse_args()

    ino_file = generate(args.filename)

    if args.compile:
        compile_arduino(ino_file)

    if args.upload:
        compile_arduino(ino_file)
        upload_arduino(
            ino_file,
            args.upload
        )


if __name__ == "__main__":
    main()