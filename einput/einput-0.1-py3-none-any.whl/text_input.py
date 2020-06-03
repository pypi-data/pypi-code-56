import sys

print("""
    input_module.text_input Copyright (C) 2020  Lucifer Monao
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions.
    """)



def delete_line(amount=1):
    for _ in range(amount):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")

def get_input(text="Please enter a valid [type]...",up=False,str_type="String", max_length=False, min_length=False, remove=False, layout="Space", contain_numbers=True, contain_special_symbols=True):
    
    addons = []
    start_of_addon = text.find("[")
    end_of_addon = text.find("]")
    while not start_of_addon == -1 and not end_of_addon == -1:
        addons.append([(text[start_of_addon:end_of_addon]).strip("[").strip("]"), start_of_addon])
        text = text[:start_of_addon] +  text[end_of_addon + 1:] 
        start_of_addon = text.find("[")
        end_of_addon = text.find("]")
        
    for addon in addons[::-1]:
        if addon[0].upper() == "TYPE":
            text_as_list = list(text)
            text_as_list.insert(addon[1], "" + str(str_type).lower())
            text = "".join(text_as_list)
        if addon[0].upper() == "MAX_LENGTH":
            text_as_list = list(text)
            text_as_list.insert(addon[1], "" + str(max_length).lower())
            text = "".join(text_as_list)
        if addon[0].upper() == "MIN_LENGTH":
            text_as_list = list(text)
            text_as_list.insert(addon[1], "" + str(min_length).lower())
            text = "".join(text_as_list)
        if addon[0].upper() == "CONTAIN_NUMBERS":
            text_as_list = list(text)
            text_as_list.insert(addon[1], "" + str(contain_numbers).lower())
            text = "".join(text_as_list)
        if addon[0].upper() == "CONTAIN_SPECIAL_SYMBOLS":
            text_as_list = list(text)
            text_as_list.insert(addon[1], "" + str(contain_special_symbols).lower())
            text = "".join(text_as_list)


    if layout.upper() == "SPACE":
        text = text + " "
    elif layout.upper() == "TABULATOR" or layout == "TAB":
        text = text + "    "
    elif layout.upper() == "ENTER":
        text = text + "\n"


    while True:
        input_text = input(text)
        if remove: delete_line()
        success = True

        # CONVERTING TO STRING 
        if str_type.upper() == "STRING":
            for number in "1234567890":
                if number in input_text and not contain_numbers:
                    print("Please enter a valid string without any numbers...")
                    success = False
            for special_symbol in """!§$%&/()=?'_:;'°><,.-#+"´^|²³′¸`}[]{~’}""":
                if special_symbol in input_text and not contain_special_symbols:
                    print("Please enter a valid string without any special symbols...")
                    success = False
            if up:
                input_text = input_text.upper()

        #COVERTING TO INTEGER
        if str_type.upper() == "INTEGER":
            try:
                input_text = int(input_text)
            except ValueError:
                print("Please enter a valid integer...")
                success = False
            except TypeError:
                print("Please enter a valid integer...")
                success = False

        #CONVERTING TO FLOAT
        if str_type.upper() == "FLOAT":
            try:
                input_text = float(input_text)
            except ValueError:
                print("Please enter a valid float...")
                success = False
            except TypeError:
                print("Please enter a valid float...")
                success = False

        #CONVERTING TO LIST
        if str_type.upper() == "LIST":
            for number in "1234567890":
                if number in input_text and not contain_numbers:
                    print("Please enter a valid string without any numbers...")
                    success = False
            for special_symbol in """!§$%&/()=?'_:;'°><,.-#+"´^|²³′¸`}[]{~’}""":
                if special_symbol in input_text and not contain_special_symbols:
                    print("Please enter a valid string without any special symbols...")
                    success = False
            try:
                input_text = list(input_text)
            except ValueError:
                print("Please enter a valid array of character...")
                success = False
            except TypeError:
                print("Please enter a valid array of character...")
                success = False

        #CHECKING LENGTH
        if type(input_text) == list:
            if len(input_text) < min_length and not type(min_length) == bool:
                print(f"Your entered text is too short, it has to have at least {min_length} numbers...")
                success = False
            if len(input_text) > max_length and not type(max_length) == bool:
                print(f"Your entered text is too long, it has to have at most {max_length} numbers...")
                success = False
        elif type(input_text) == int or type(input_text) == float:
            if input_text < 10 ** min_length and not type(min_length) == bool:
                print(f"Your entered text is too smal, it has to have at least {10 ** min_length} numbers...")
                success = False
            if input_text > 10 ** max_length and not type(max_length) == bool:
                print(f"Your entered text is too big, it has to have at most {10 ** max_length} numbers...")
                success = False
        else:
            if len(str(input_text)) < min_length and not type(min_length) == bool:
                print(f"Your entered text is too short, it has to have at least {min_length} numbers...")
                success = False
            if len(str(input_text)) > max_length and not type(max_length) == bool:
                print(f"Your entered text is too long, it has to have at most {max_length} numbers...")
                success = False
        if success: return(input_text)

def number_input(*argv, text="Please enter a valid [type] with the minumum length of [min_length] and the maximum length of [max_length].", max_number=False, min_number=False, type_of_number="INTEGER"):
    return(get_input(text, min_length=min_number, max_length=max_number, str_type=type_of_number))

def yes_or_no(text="Please enter yes or no."):
    while True:
        entered = input(text)
        if entered == "yes": return(True)
        elif entered == "no": return(False)
        

if __name__ == "__main__Now you can use *args or **kwargs to pass arguments ":
    print(get_input(contain_numbers=False, remove=True,text="Please enter a valid [type] with the minumum length of [min_length] and the maximum length of [max_length].",contain_special_symbols=False, up=True, layout="Enter", max_length=200, min_length=2, str_type="STRING"))