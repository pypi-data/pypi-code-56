from django.conf import settings

def print_f(*texts, destac=True, remain=False, lenght=50, separator='\n'):
    can_print = True

    if not remain:
        try:
            NOCTON = settings.NOCTON
            can_print = NOCTON.get('alerts') == True
        except AttributeError:
            pass

    if can_print:
        f_text = ""

        for text in texts:
            line = "=" * lenght
            text = str(text).split()
            n = 0
            line_text = ['']
            
            for name in text:
                n += len(name) + 1

                if n < lenght:
                    line_text[-1] += (name + " ")
                else:
                    n = len(name) + 1
                    line_text.append(name + " ")
                    line_text[-2] = line_text[-2].center(lenght)
            line_text[-1] = line_text[-1].center(lenght)

            for index, line_t in enumerate(line_text):
                f_text += (line_t + '\n') if index != len(line_text) - 1 else line_t
            
            f_text += separator

        if destac:
            print(f"""
{line}
{f_text}
{line}
            """)
        else:
            print(f"""
{f_text}
            """)