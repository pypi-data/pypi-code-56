class EmptyStringGiven(Exception):
	"""A error raised when given string is empty"""
	pass

class MissingRequiredParameter(Exception):
	"""A error raised a required parameter is missing"""
	pass

def morsify(text:str=None):
	"""Encode text to morse code"""
	if text is None:
		raise MissingRequiredParameter("'text' is a required parameter.")
	
	if text == "":
		raise EmptyStringGiven("'text' must have length greater than 0")

	code = {
			"a" : ".-",
			"b" : "-...",
			"c" : "-.-.",
			"d" : "-..",
			"e" : ".",
			"f" : "..-.",
			"g" : "--.",
			"h" : "....",
			"i"  : "..",
			"j"  : ".---",
			"k" : "-.-",
			"l"  : ".-..",
			"m" : "--",
			"n" : "-.",
			"o" : "---",
			"p" : ".--.",
			"q" : "--.-",
			"r"  : ".-.",
			"s" : "...",
			"t" : "-",
			"u": "..-",
			"v" : "...-",
			"w" : ".--",
			"x"  : "-..-",
			"y"  : "-.--",
			"z" : "--..",
			"1" : ".----",
			"2" : "..---",
			"3" : "...--",
			"4" : "....-",
			"5" : ".....",
			"6" : "-....",
			"7" : "--...",
			"8" : "---..",
			"9" : "----.",
			"0" : "-----",
		}
		
	text = str(text).lower().replace(".", "").replace("-", "")
		
	chars = list(text)
	msg = ""
	for w in chars:
		try:
			msg += code[w] + " "
		except:
			msg += " "
		
	return msg


def demorse(code:str=None):
	"""Decode morse code to text."""
	if code is None:
		raise MissingRequiredParameter("'code' is required.")
	
	if len(code) == 0:
		raise EmptyStringGiven("'code' must have length greater than 1")

	morse_codes = {
			".-" : "a",
			"-..." : "b",
			"-.-." : "c",
			"-.." : "d",
			"." : "e",
			"..-." : "f",
			"--.": "g",
			"...." : "h",
			".." : "i",
			".---" : "j",
			"-.-" : "k",
			".-.." : "l",
			"--" : "m",
			"-." : "n",
			"---" : "o",
			".--." : "p",
			"--.-" : "q",
			".-." : "r",
			"..." : "s",
			"-" : "t",
			"..-" : "u",
			"...-" : "v",
			".--" : "w",
			"-..-" : "x",
			"-.--" : "y",
			"--.." : "z",
			".----" : "1",
			"..---" : "2",
			"...--" : "3",
			"....-" : "4",
			"....." : "5",
			"-...." : "6",
			"--..." : "7",
			"---.." : "8",
			"----." : "9",
			"-----" : "0",
		}
	code = str(code).lower()
	
	chars = code.split(" ")
	msg = ""
		
	for w in chars:
		try:
			msg += morse_codes[w]
		except:
			msg += " "

	return msg	
	