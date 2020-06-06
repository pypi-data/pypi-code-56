"""
Mask Code Like PyQt5.QWidget.QLineEdit
It is **simpler** and **easier to understand** than **regular expressions**.

References
-----------
https://www.cnblogs.com/HE-helloword/articles/12349285.html
"""
all_alphas = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
all_upper_alphas = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z']
all_numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
print(all_numbers, all_alphas, all_upper_alphas)


def mask_char2char_set(mask_char: str):
    """
    Mask Char like 'a' to char set like [1]
    Parameters
    ----------
    mask_char:mask str

    Returns
    -------
    char set(list type)

    Raises
    ------
    ValueError(Mask Char Can't to be empty):Can't be Mask  Char To Empty String('')

    Warnings
    --------
    Don't Support like 'a' or '!'
    Only Support 'A' 'N' '9' 'D' 'F' 'B'

    """

    if mask_char == "":
        raise ValueError("Mask Char Can't to be empty")

    if mask_char == "A":
        alphas = all_alphas[:]
        alphas.extend(all_upper_alphas)
        return alphas

    if mask_char == "N":
        l = all_alphas[:]
        l.extend(all_upper_alphas)
        l.extend(all_numbers)
        return l

    if mask_char == "9":
        return all_numbers

    if mask_char == "D":
        return all_numbers[1:]

    if mask_char == "H":
        return \
            ['a', 'b', 'c', 'd', 'e', 'f',
             'A', 'B', 'C', 'D', 'E', 'F',
             0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    if mask_char == "B":
        return ["0", "1"]
    return mask_char


def is_match(mask: str, string: str) -> bool:
    """
    Is The Mask Match String
    
    Parameters
    ----------
    mask:Maskcode
    string:Will match string

    Returns
    -------
    Boolean:True/False

    Examples
    --------
    >>>is_match("9", "0")
    >>>is_match("A", "0")

    
    Warnings
    --------
    Don't Support like 'a' or '!'
    Only Support 'A' 'N' '9' 'D' 'F' 'B'
    """
    if len(mask) != len(string):
        return False

    for i in range(len(mask)):
        # print(mask_char2char_set(mask[i]), string[i])
        # print(string[i] not in mask_char2char_set(mask[i]))
        if string[i] not in mask_char2char_set(mask[i]):
            return False

    return True
