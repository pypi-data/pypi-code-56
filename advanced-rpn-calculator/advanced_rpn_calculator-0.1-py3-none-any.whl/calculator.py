import math
import random

class Calculator:

    def __init__(self):
        self.stack = []
        self.loop_flag = True
        self.operation = {
            "+": self.add,
            "-": self.sub,
            "*": self.mul,
            "/": self.div,
            "cla": self.clear_stack_and_variable,
            "clr": self.clear_stack,
            "clv": self.clear_variable,
            "!": self.bool_not,
            "!=": self.bool_not_equal,
            "%": self.modulo,
            "++": self.increment,
            "--": self.decrement,
            "&": self.bw_and,
            "|": self.bw_or,
            "^": self.bw_xor,
            "~": self.bw_not,
            "<<": self.bw_shift_left,
            ">>": self.bw_shift_right,
            "&&": self.bool_and,
            "||": self.bool_or,
            "^^": self.bool_xor,
            "<": self.smaller_than,
            "<=": self.smaller_than_or_equal_to,
            "==": self.equal_to,
            ">": self.greater_than,
            ">=": self.greater_than_or_equal_to,
            "acos": self.arc_cosine,
            "asin": self.arc_sine,
            "atan": self.arc_tangent,
            "cos": self.cosine,
            "cosh": self.hyperbolic_cosine,
            "sin": self.sine,
            "sinh": self.hyperbolic_sine,
            "tanh": self.hyperbolic_tangent,
            "ceil": self.ceiling,
            "floor": self.floor,
            "round": self.round,
            "ip": self.ip,
            "fp": self.fp,
            "abs": self.absolute,
            "max": self.max_,
            "min": self.min_,
            "hex": self.hex_,
            "bin": self.bin_,
            "dec": self.dec_,
            "e": self.e,
            "pi": self.pi,
            "rand": self.rand_,
            "exp": self.exp,
            "fact": self.fact,
            "sqrt": self.square_root,
            "ln": self.ln,
            "log": self.log,
            "pow": self.pow,
            "pick": self.pick,
            "repeat": self.repeat,
            "drop": self.drop,
            "dropn": self.dropn,
            "dup": self.dup,
            "dupn": self.dupn,
            "roll": self.roll,
            "rolld": self.rolld,
            "stack": self.stack_,
            "swap": self.swap,
            "x=": self.assign_variable,
            "help": self.help,
            "exit": self.quit
        }
        self.output = None
        self.display_mode = 'dec'
        self.repeat_count = 0
        self.x = None
        self.stack_mode = 'horizontal'
        self.macro = {}

    @staticmethod
    def get_letter_or_digit(num):
        """If possible return a number, else return num as a string"""
        for cast in (int, float):
            try:
                num = cast(num)
                return num
            except ValueError:
                pass
        if num[0] == "0":
            for base in (2, 8, 16):
                try:
                    num = int(num, base)
                    return num
                except ValueError:
                    pass
        return num

    def loop(self):
        while self.loop_flag:
            string = ''
            if self.stack:
                
                if self.stack_mode == 'horizontal':
                    stack = ", ".join([str(each) for each in self.stack])
                    print(f"stack = [{stack}]")
                elif self.stack_mode == 'vertical':
                    stack = ",\n".join([str(each) for each in self.stack])
                    print(f"stack = [{stack}]")
                    
            if self.x:
                print(f"x = {self.x}")

            if self.output is None:
                if self.stack:
                    string = self.stack[-1]
            else:
                string = self.output

            if string:
                if self.display_mode == 'hex':
                    if isinstance(string, float):
                        string = f"{float.hex(string)}"
                    else:
                        string = f"{hex(string)}>"
                elif self.display_mode == 'bin':
                    if isinstance(string, float):
                        print("Integer value is required for any notation except decimal!")
                    else:
                        string = f"{bin(string)}>"
                elif self.display_mode == 'oct':
                    if isinstance(string, float):
                        print("Integer value is required for any notation except decimal!")
                    else:
                        string = f"{oct(string)}>"

            data = input(f"{string}>")
            self.evaluate(data)

    def evaluate(self, string):
        l = string.split()
        for i in l:
            i = self.get_letter_or_digit(i)
            if isinstance(i, (int, float)):
                self.stack.append(i)
            elif i == 'x':
                if self.x:
                    self.stack.append(self.x)
                else:
                    print("'x' is not assigned any value!")
            elif i == 'macro':
                i = l.index(i) + 1
                self.macro[l[i]] = l[i+1:]
                break
            elif i in self.macro:
                ind = l.index(i) + 1
                l[ind:ind] = self.macro[i]
            else:
                if i in self.operation.keys():
                    if self.repeat_count:
                        for _ in range(self.repeat_count):
                            self.operation[i]()
                        self.repeat_count = 0
                    else:
                        self.operation[i]()
                else:
                    print("Unknown command: {}".format(i))

    def check_stack(self, num, command):
        """Check if enough number are in the stack"""
        if len(self.stack) < num:
            print("Not enough numbers in the stack for {} command".format(command))
            return False
        return True

    def check_int(self, value, operation):
        if not isinstance(value, int):
            print(f"The operation \"{operation}\" requires int value (found:{value})")
            self.stack.append([value])
            return False
        return True

    def add(self):
        """Take 2 numbers from the stack, add them and put the result in the stack"""
        if self.check_stack(2, "+"):
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            self.output = value1 + value2
            self.stack.append(self.output)

    def sub(self):
        """Take 2 numbers from the stack, substracte them and put the result in the stack"""
        if self.check_stack(2, "-"):
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            self.output = value2 - value1
            self.stack.append(self.output)

    def mul(self):
        """Take 2 numbers from the stack, mul them and put the result in the stack"""
        if self.check_stack(2, "*"):
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            self.output = value1 * value2
            self.stack.append(self.output)

    def div(self):
        """Take 2 numbers from the stack, divise them and put the result in the stack"""
        if self.check_stack(2, "/"):
            value1 = self.stack.pop()
            if value1 == 0:
                print("Impossible to divise by 0")
                self.stack.append(value1)
                return
            value2 = self.stack.pop()
            self.output = value2 / value1
            self.stack.append(self.output)

    def clear_stack_and_variable(self):
        """Clear both stack and variable"""
        self.stack = []
        self.x = None
        self.output = None

    def clear_stack(self):
        """Empty the stack"""
        self.stack = []
        self.output = None

    def clear_variable(self):
        """Clear both stack and variable"""
        self.x = None
        self.output = None

    def bool_not(self):
        if self.check_stack(1, "!"):
            value = self.stack.pop()
            self.output = (not value)

    def bool_not_equal(self):
        """Return True if last two numbers in stack are equal, False otherwise"""
        if self.check_stack(2, "!="):
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            self.output = (value1!=value2)

    def modulo(self):
        """Take 2 integers from the stack, divide them and put the remainder in the stack"""
        if self.check_stack(2, "%"):
            value1 = self.stack.pop()
            if value1 == 0:
                print("Impossible to divide by 0")
                self.stack.append(value1)
                return
            value2 = self.stack.pop()
            if self.check_int(value1, "%") and self.check_int(value2, "%"):
                self.output = value2 % value1
                self.stack.append(self.output)

    def increment(self):
        """Increment an integer"""
        if self.check_stack(1, "++"):
            value = self.stack.pop()
            self.output = value + 1
            self.stack.append(self.output)

    def decrement(self):
        """Decrement an integer"""
        if self.check_stack(1, "--"):
            value = self.stack.pop()
            self.output = value - 1
            self.stack.append(self.output)

    def bw_and(self):
        """Take 2 numbers from the stack, apply a bitwise "and" and put the result in the stack"""
        if self.check_stack(2, "&"):
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            if self.check_int(value1, "&") and self.check_int(value2, "&"):
                self.output = value1 & value2
                self.stack.append(self.output)

    def bw_or(self):
        """Take 2 numbers from the stack, apply a bitwise "or" and put the result in the stack"""
        if self.check_stack(2, "|"):
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            if self.check_int(value1, "|") and self.check_int(value2, "|"):
                self.output = value1 | value2
                self.stack.append(self.output)

    def bw_xor(self):
        """Take 2 numbers from the stack, apply a bitwise "xor" and put the result in the stack"""
        if self.check_stack(2, "^"):
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            if self.check_int(value1, "^") and self.check_int(value2, "^"):
                self.output = value1 ^ value2
                self.stack.append(self.output)

    def bw_not(self):
        """Take 2 numbers from the stack, apply a bitwise "xor" and put the result in the stack"""
        if self.check_stack(2, "~"):
            value1 = self.stack.pop()
            if self.check_int(value1, "~"):
                self.output = ~value1
                self.stack.append(self.output)

    def bw_shift_left(self):
        """Take 2 numbers from the stack, apply a left shift and put the result in the stack"""
        if self.check_stack(2, "<<"):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            if self.check_int(value1, "<<") and self.check_int(value2, "<<"):
                self.output = value1 << value2
                self.stack.append(self.output)

    def bw_shift_right(self):
        """Take 2 numbers from the stack, apply a right shift and put the result in the stack"""
        if self.check_stack(2, ">>"):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            if self.check_int(value1, ">>") and self.check_int(value2, ">>"):
                self.output = value1 >> value2
                self.stack.append(self.output)

    def bool_and(self):
        """Perform boollean AND operation on two values and output the result (not added to the stack)"""
        if self.check_stack(2, "&&"):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            self.output = ((value1) and (value2))


    def bool_or(self):
        """Perform boollean OR operation on two values and output the result (not added to the stack)"""
        if self.check_stack(2, "||"):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            self.output = ((value1) and (value2))

    def bool_xor(self):
        """Perform boolean XOR operation on two values and output the result (not added to the stack)"""
        if self.check_stack(2, "||"):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            self.output = (bool(value1))^(bool(value2))

    def smaller_than(self):
        """Smaller than operation on two values and output the result (not added to the stack)"""
        if self.check_stack(2, "<"):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            self.output = value1<value2

    def smaller_than_or_equal_to(self):
        """Smaller than or equal to operation on two values and output the result (not added to the stack)"""
        if self.check_stack(2, "<="):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            self.output = value1<=value2

    def greater_than(self):
        """Greater than operation on two values and output the result (not added to the stack)"""
        if self.check_stack(2, ">"):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            self.output = value1>value2

    def greater_than_or_equal_to(self):
        """Greater than operation on two values and output the result (not added to the stack)"""
        if self.check_stack(2, ">="):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            self.output = value1 >= value2

    def equal_to(self):
        """Equal to operation on two values and output the result (not added to the stack)"""
        if self.check_stack(2, "=="):
            value2 = self.stack.pop()
            value1 = self.stack.pop()
            self.output = (value1 == value2)

    def arc_cosine(self):
        """Take arc cosine on a value and output the result (also added to the stack)"""
        if self.check_stack(1, "acos"):
            value = self.stack.pop()
            self.output = math.acos(value)
            self.stack.append(self.output)

    def arc_sine(self):
        """Take arc sine on a value and output the result (also added to the stack)"""
        if self.check_stack(1, "asin"):
            value = self.stack.pop()
            self.output = math.asin(value)
            self.stack.append(self.output)

    def arc_tangent(self):
        """Take arc tangent on a value and output the result (also added to the stack)"""
        if self.check_stack(1, "atan"):
            value = self.stack.pop()
            self.output = math.atan(value)
            self.stack.append(self.output)

    def cosine(self):
        """Take cosine on a value and output the result (also added to the stack)"""
        if self.check_stack(1, "cos"):
            value = self.stack.pop()
            self.output = math.cos(value)
            self.stack.append(self.output)

    def hyperbolic_cosine(self):
        """Take arc hyperbolic cosine on a value and output the result (also added to the stack)"""
        if self.check_stack(1, "cosh"):
            value = self.stack.pop()
            self.output = math.cosh(value)
            self.stack.append(self.output)

    def sine(self):
        """Take sine on a value and output the result (also added to the stack)"""
        if self.check_stack(1, "sin"):
            value = self.stack.pop()
            self.output = math.sin(value)
            self.stack.append(self.output)

    def hyperbolic_sine(self):
        """Take hyperbolic sine on a value and output the result (also added to the stack)"""
        if self.check_stack(1, "sinh"):
            value = self.stack.pop()
            self.output = math.sinh(value)
            self.stack.append(self.output)

    def hyperbolic_tangent(self):
        """Take hyperbolic tangent on a value and output the result (also added to the stack)"""
        if self.check_stack(1, "tanh"):
            value = self.stack.pop()
            self.output = math.tanh(value)
            self.stack.append(self.output)

    def ceiling(self):
        """Take ceil of an integer and output the result (also added to the stack)"""
        if self.check_stack(1, "ceil"):
            value = self.stack.pop()
            self.output = math.ceil(value)
            self.stack.append(self.output)


    def floor(self):
        """Take floor of an integer and output the result (also added to the stack)"""
        if self.check_stack(1, "floor"):
            value = self.stack.pop()
            self.output = math.floor(value)
            self.stack.append(self.output)


    def round(self):
        """Take round of an integer and output the result (also added to the stack)"""
        if self.check_stack(1, "round"):
            value = self.stack.pop()
            self.output = round(value)
            self.stack.append(self.output)


    def ip(self):
        """Separates int from floating part of a decimal number and output the result (also added to the stack)"""
        if self.check_stack(1, "ip"):
            value = self.stack.pop()
            self.output, _ = math.modf(value)
            self.stack.append(self.output)

    def fp(self):
        """separates floating part of a decimal number and output the result (also added to the stack)"""
        if self.check_stack(1, "float"):
            value = self.stack.pop()
            _, self.output = math.modf(value)
            self.stack.append(self.output)
    # Todo: A little ambiguity in readme.md file about working of "sign"
    def absolute(self):
        """Take ceil of an integer and output the result (also added to the stack)"""
        if self.check_stack(1, "abs"):
            value = self.stack.pop()
            self.output = abs(value)
            self.stack.append(self.output)
    # Todo: Ambiguity about whether to push the max value to stack or not
    def max_(self):
        """Take maximum value of the stack and output the result (also removed from the stack)"""
        if self.check_stack(1, "max"):
            self.output = max(self.stack)
            self.stack.remove(self.output)
    # Todo: Ambiguity about whether to push the min value to stack or not
    def min_(self):
        """Take minimum value of the stack and output the result (also removed from the stack)"""
        if self.check_stack(1, "min"):
            self.output = min(self.stack)
            self.stack.remove(self.output)

    def hex_(self):
        """Change display mode to hex"""
        self.display_mode = 'hex'

    def dec_(self):
        """Change display mode to decimal"""
        self.display_mode = 'dec'

    def bin_(self):
        """Change display mode to binary"""
        self.display_mode = 'bin'

    def oct_(self):
        """Change display mode to octal"""
        self.display_mode = 'oct'

    def e(self):
        self.output = math.e
        self.stack.append(self.output)

    def pi(self):
        self.output = math.pi
        self.stack.append(self.output)

    def rand_(self):
        self.output = random.randint()
        self.stack.append(self.output)

    def exp(self):
        """Apply e**x to the last number of the stack"""
        if self.check_stack(1, "exp"):
            value = self.stack.pop()
            self.output = math.exp(value)
            self.stack.append(self.output)

    def fact(self):
        """Push factorial of the last number to the stack"""
        if self.check_stack(1, "fact"):
            value = self.stack.pop()
            if self.check_int(value, "fact"):
                self.output = 1
                while value>0:
                    self.output *= value
                    value -= 1
                self.stack.append(self.output)

    def square_root(self):
        """Push factorial of the last number to the stack"""
        if self.check_stack(1, "fact"):
            value = self.stack.pop()
            self.output = math.sqrt(value)
            self.stack.append(self.output)

    def ln(self):
        """Apply log10 to the last number of the stack"""
        if self.check_stack(1, "ln"):
            value = self.stack.pop()
            if value > 0:
                self.output = math.log(value)
                self.stack.append(self.output)
            else:
                print("Number out of domain for logarithm")
                self.stack.append(value)

    def log(self):
        """Apply log10 to the last number of the stack"""
        if self.check_stack(1, "log10"):
            value = self.stack.pop()
            if value > 0:
                self.output = math.log(value)
                self.stack.append(self.output)
            else:
                print("Number out of domain for logarithm")
                self.stack.append(value)

    def pow(self):
        """Take 2 numbers from the stack, apply power and put the result in the stack"""
        if self.check_stack(2, "**"):
            value1 = self.stack.pop()
            value2 = self.stack.pop()
            self.output = value2 ** value1
            self.stack.append(self.output)
    # Todo: Add support for network operations

    def pick(self):
        """Pick the nth item form stack"""
        if self.check_stack(1, "pick"):
            value = self.stack.pop()
            if 0<=value<len(self.stack):
                self.output = self.stack[value]
            else:
                self.output = None
                print("Index out of range for 'pick'!")

    def repeat(self):
        """Repeat an operation n times"""
        if self.check_stack(1, "repeat"):
            self.repeat_count = self.stack.pop()

    # Todo: depth implementation
    def drop(self):
        """Drop the top most item from the stack"""
        if self.check_stack(1, "drop"):
            self.stack.pop()

    def dropn(self):
        """Drop the n top most items from the stack"""
        if self.check_stack(1, "dropn"):
            value = self.stack.pop()
            if self.check_stack(value, "dropn"):
                self.stack = self.stack[:-value]

    def dup(self):
        """Duplicates the top item from the stack"""
        if self.check_stack(1, "dup"):
            self.stack.append(self.stack[-1])

    def dupn(self):
        """Duplicates n top items of thew stack"""
        if self.check_stack(1, "dupn"):
            value = self.stack.pop()
            if self.check_stack(value, "dupn"):
                self.stack.extend(self.stack[-value:])

    def roll(self):
        """Roll the stack upwards by n"""
        if self.check_stack(1, 'roll'):
            value = self.stack.pop()
            if self.check_stack(value, 'roll'):
                self.stack = self.stack[-value:] + self.stack[:-value]

    def rolld(self):
        """Roll the stack downwards by n"""
        if self.check_stack(1, 'rolld'):
            value = self.stack.pop()
            if self.check_stack(value, 'rolld'):
                self.stack = self.stack[value:] + self.stack[:value]


    def stack_(self):
        """Toggles stack display from horizontal to vertical"""
        self.stack_mode = "vertical"

    def swap(self):
        """Swap the top 2 stack items"""
        temp = self.stack[-1]
        self.stack[-1] = self.stack[-2]
        self.stack[-2] = temp

    # Todo: define a macro
    def assign_variable(self):
        """Assigns a variable, e.g. '1024 x='"""
        self.x = self.stack.pop()

    def help(self):
        """Print help; Same as pol --list"""
        doc = ""
        for command, method in self.operation.items():
            doc += "`{}` : {}\n".format(command, method.__doc__)

        print(doc)

    def quit(self):
        """Quit the program"""
        self.loop_flag = False
