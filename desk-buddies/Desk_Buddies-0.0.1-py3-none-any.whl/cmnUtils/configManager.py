from prettytable import PrettyTable

# These can methods can be static, because they are stateless
from cmnSys.simpleConfig import SimpleConfig


def user_config_interface(settings: SimpleConfig):
    print("Here are a list of properties you can alter, type 'q' at any time when you are done!")
    table = PrettyTable()
    table.field_names = ["Item", "Type", "Value"]
    for key, val in settings.items():
        table.add_row([key, type(val).__name__, val])

    print(table)
    while True:
        prop = input("Enter a property you would like set: ")
        if prop == 'q':
            break
        if prop not in settings.keys():
            print("Property does not exist. Try again.")
            continue
        val = input("Enter the value you would like to set: ")
        if prop == 'q':
            break
        try:
            val = type(settings[prop])(val)
            settings[prop] = val
        except ValueError:
            print("Value could not be converted to the expected datatype")


