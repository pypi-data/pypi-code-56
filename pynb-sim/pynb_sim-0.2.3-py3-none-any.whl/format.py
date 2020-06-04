def format(str, **kwargs):
    # Replace single {} to double {{}} and {{||}} to {}
    try:
        return str.replace("{{|", chr(219)).replace("|}}", chr(220))\
            .replace("{", "{{").replace("}", "}}")\
            .replace(chr(219), "{").replace(chr(220), "}")\
            .format(
                powered_by=_powered_by(),
                powered_by_header="""
                    $("<div style='display: none;' class='powered-by-header pynbsim-injected-block'></div>")
                        .append(""" + _powered_by() + ")",
                **kwargs
            )
    except KeyError as e:
        raise KeyError("Can't format, missing the '{}' argument".format(e.args[0]))

def _powered_by():
    return """$("<div class='powered-by'><i class='fas fa-rocket'></i> Powered by <a href='https://github.com/Helveg/pynb-sim' target='_blank'>pynbsim</a></div>")"""
