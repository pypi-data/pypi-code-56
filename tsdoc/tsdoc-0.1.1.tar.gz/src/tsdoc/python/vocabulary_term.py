from tsdoc.python.segment import Segment
from typing import Final
from typing import Optional
from typing import TYPE_CHECKING

# Conditional import used because there would be a circular dependency
# https://mypy.readthedocs.io/en/latest/common_issues.html#import-cycles
if TYPE_CHECKING:
    from tsdoc.python.vocabulary import Vocabulary  # noqa: F401

import attr


@attr.s(auto_attribs=True, kw_only=True)
class VocabularyTerm(Segment):
    # Forward reference used because there would be a circular dependency
    # https://mypy.readthedocs.io/en/latest/kinds_of_types.html#class-name-forward-references
    parent: Optional["Vocabulary"] = attr.ib(eq=False)
    text: Final[str]  # type: ignore[misc]

    @property
    def name(self) -> str:
        names = {
            "Equal to": "Equal to (==)",
            "Greater than": "Greater than (>)",
            "Less than": "Less than (<)",
            "Not equal to": "Not equal to (!=)",
        }

        return names.get(self.text, self.text)

    @property
    def definition(self) -> str:
        definitions = {
            "and": "True if all parts are True",
            "Argument": "Information that a function needs to know in order to run",
            "Assignment": "Storing information in a variable",
            "Attribute": "A piece of information an object knows about itself",
            "Boolean": "A True or False value",
            "Boolean zen": "Using a boolean as a complete condition",
            "break": "Immediately end a loop",
            "Chained comparison": "An expression with more than one comparison operator",  # noqa: E501
            "Class": "A blueprint for creating something specific",
            "Comment": "A note that the computer ignores",
            "Comparison operator": "Compares two values and gives a yes or no answer",
            "Compound expression": "A boolean expression made of up of other boolean expressions",  # noqa: E501
            "Concatenate": "Join two strings together using the + symbol",
            "Condition": "Asks a yes or no question",
            "Conditional": "Runs the first section of code where the condition is true",
            "continue": "Immediately end an iteration",
            "Data type": "The category a piece of information belongs to",
            "Decrement": "Decrease a variable by an amount",
            "Documentation": "A written explanation of how to use code",
            "elif statement": "When all prior conditions are false, runs a section code when the condition is true",  # noqa: E501
            "else statement": "When all prior conditions are false, runs a section of code as a last alternative",  # noqa: E501
            "Equal to": "Are the two values the same?",
            "Error": "When the computer encounters something unexpected in your code",  # noqa: E501
            "Expression": "A piece of code that produces a value",
            "Float": "A number with a decimal point",
            "Floor division": "Rounds the quotient down to a whole number after division",  # noqa: E501
            "Function": "A named code action that can be used in a program",
            "Greater than": "Is the left value bigger than the right value?",
            "Header comment": 'A multi-line comment at the top of a program surrounded by `"""` marks',  # noqa: E501
            "if statement": "Runs a section code when the condition is true",
            "Increment": "Increase a variable by an amount",
            "Infinite loop": "A loop with a condition that will always be True",
            "Input": "Information the program receives from the user",
            "Instance": "A specific copy created from a class",
            "Integer": "A whole number",
            "Iteration": "One repetition of a loop",
            "Less than": "Is the left value smaller than the right value?",
            "Library": "A collection of code from outside the program",
            "Literal": "A value that is not in a variable",
            "Logical operator": "Combines or modifies a boolean",
            "Method": "A function that belongs to an instance",
            "Modulus": "Gets the remainder after division",
            "Nested conditional": "A conditional inside another conditional",
            "None": 'A special keyword that means "no value"',
            "not": "Gives the opposite boolean value",
            "Not equal to": "Are the two values different?",
            "or": "True if one or more parts are True",
            "Output": "Information a program gives to the user, such as text",
            "Power": "Multiplies a number by itself some number of times",
            "Random": "A library with code to create unpredictable values",
            "Return value": "Information given back by a function",
            "Shortcut operator": "Changes a variable based on the current value",
            "Statement": "A single line of code that perform an action",
            "String": "A group of letters, symbols and/or numbers inside double quotation marks",  # noqa: E501
            "String multiplication": "Repeat one or more characters a certain number of times",  # noqa: E501
            "Syntax": "Exact spelling, symbols and order of the code",
            "Then block": "A section of code that might get run",
            "Typecast": "Treat one data type like another",
            "Variable": "A storage container for information",
            "while - else": "A clause following a while loop that runs unless the loop ends with break",  # noqa: E501
            "while loop": "Repeats a section of code until a condition is no longer True",  # noqa: E501
        }

        return definitions[self.text]

    @property
    def instruction(self) -> str:
        instructions = {
            "and": "2.4.1",
            "Argument": "1.2.1",
            "Assignment": "1.1.3",
            "Attribute": "3.1.3",
            "Boolean": "2.4.1",
            "Boolean zen": "2.4.2",
            "break": "3.1.2",
            "Chained comparison": "2.2.2",
            "Class": "3.1.3",
            "Comment": "1.1.2",
            "Comparison operator": "2.1.2",
            "Compound expression": "2.4.2",
            "Concatenate": "1.3.2",
            "Condition": "2.1.1",
            "Conditional": "2.2.1",
            "continue": "3.1.2",
            "Data type": "1.3.1",
            "Decrement": "1.4.1",
            "Documentation": "1.2.2",
            "elif statement": "2.2.1",
            "else statement": "2.2.1",
            "Equal to": "2.1.1",
            "Error": "1.1.2",
            "Expression": "1.4.1",
            "Float": "1.3.1",
            "Floor division": "2.3.2",
            "Function": "1.2.1",
            "Greater than": "2.1.2",
            "Header comment": "1.1.2",
            "if statement": "2.1.1",
            "Increment": "1.4.1",
            "Infinite loop": "3.1.1",
            "Input": "1.1.3",
            "Instance": "3.1.3",
            "Integer": "1.3.1",
            "Iteration": "3.1.1",
            "Less than": "2.1.2",
            "Library": "1.2.1",
            "Literal": "1.3.1",
            "Logical operator": "2.4.1",
            "Method": "3.1.3",
            "Modulus": "2.3.2",
            "Nested conditional": "2.2.2",
            "None": "1.4.2",
            "not": "2.4.1",
            "Not equal to": "2.1.1",
            "or": "2.4.1",
            "Output": "1.1.1",
            "Power": "2.3.2",
            "Random": "2.3.1",
            "Return value": "1.4.2",
            "Shortcut operator": "1.4.1",
            "Statement": "1.1.1",
            "String": "1.1.1",
            "String multiplication": "1.3.2",
            "Syntax": "1.1.1",
            "Then block": "2.2.1",
            "Typecast": "1.3.2",
            "Variable": "1.1.3",
            "while - else": "3.1.2",
            "while loop": "3.1.1",
        }

        return instructions[self.text]
