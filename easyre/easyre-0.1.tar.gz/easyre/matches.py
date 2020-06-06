"""
Any Matches
"""
import re

CHINA = 0
INTONATIONAL = 1
phone_patterns = {
    'ar-DZ': r"^(\+?213|0)(5|6|7)\d{8}$",
    'ar-SY': r"^(!?(\+?963)|0)?9\d{8}$",
    'ar-SA': r"^(!?(\+?966)|0)?5\d{8}$",
    'en-US': r"^(\+?1)?[2-9]\d{2}[2-9](?!11)\d{6}$",
    'cs-CZ': r"^(\+?420)? ?[1-9][0-9]{2} ?[0-9]{3} ?[0-9]{3}$",
    'de-DE': r"^(\+?49[ \.\-])?([\(]{1}[0-9]{1,6}[\)])?([0-9 \.\-\/]{3,20})((x|ext|extension)[ ]?[0-9]{1,4})?$",
    'da-DK': r"^(\+?45)?(\d{8})$",
    'el-GR': r"^(\+?30)?(69\d{8})$",
    'en-AU': r"^(\+?61|0)4\d{8}$",
    'en-GB': r"^(\+?44|0)7\d{9}$",
    'en-HK': r"^(\+?852\-?)?[569]\d{3}\-?\d{4}$",
    'en-IN': r"^(\+?91|0)?[789]\d{9}$",
    'en-NZ': r"^(\+?64|0)2\d{7,9}$",
    'en-ZA': r"^(\+?27|0)\d{9}$",
    'en-ZM': r"^(\+?26)?09[567]\d{7}$",
    'es-ES': r"^(\+?34)?(6\d{1}|7[1234])\d{7}$",
    'fi-FI': r"^(\+?358|0)\s?(4(0|1|2|4|5)?|50)\s?(\d\s?){4,8}\d$",
    'fr-FR': r"^(\+?33|0)[67]\d{8}$",
    'he-IL': r"^(\+972|0)([23489]|5[0248]|77)[1-9]\d{6}",
    'hu-HU': r"^(\+?36)(20|30|70)\d{7}$",
    'it-IT': r"^(\+?39)?\s?3\d{2} ?\d{6,7}$",
    'ja-JP': r"^(\+?81|0)\d{1,4}[ \-]?\d{1,4}[ \-]?\d{4}$",
    'ms-MY': r"^(\+?6?01){1}(([145]{1}(\-|\s)?\d{7,8})|([236789]{1}(\s|\-)?\d{7}))$",
    'nb-NO': r"^(\+?47)?[49]\d{7}$",
    'nl-BE': r"^(\+?32|0)4?\d{8}$",
    'nn-NO': r"^(\+?47)?[49]\d{7}$",
    'pl-PL': r"^(\+?48)? ?[5-8]\d ?\d{3} ?\d{2} ?\d{2}$",
    'pt-BR': r"^(\+?55|0)\-?[1-9]{2}\-?[2-9]{1}\d{3,4}\-?\d{4}$",
    'pt-PT': r"^(\+?351)?9[1236]\d{7}$",
    'ru-RU': r"^(\+?7|8)?9\d{9}$",
    'sr-RS': r"^(\+3816|06)[- \d]{5,9}$",
    'tr-TR': r"^(\+?90|0)?5\d{9}$",
    'vi-VN': r"^(\+?84|0)?((1(2([0-9])|6([2-9])|88|99))|(9((?!5)[0-9])))([0-9]{7})$",
    'zh-CN': r"^(\+?0?86\-?)?1[345789]\d{9}$",
    'zh-TW': r"^(\+?886\-?|0)?9\d{8}$"
  }


def is_match(p: str, s: str) -> bool:
    """
    Is Reg **match** str

    Parameters
    ----------
    p:Reg
    s:String

    Returns
    -------
    Boolean
    """

    if re.sub(p, "", s) == "":
        return True

    else:
        return False


def is_email(email: str, is_can_chinese: bool = False):
    """
    Is parm:email a not invalid email address

    Parameters
    ----------
    email:address
    is_can_chinese:Is Can Use Chinese Char(True/False)
    Returns
    -------
    True/False

    References
    ----------
    https://www.cnblogs.com/cuihongyu3503319/p/10244983.html

    Examples
    --------
    >>> is_email("peter@gmail.com")
    >>> is_email("小明@163.com", is_can_chinese=True)

    """
    if not is_can_chinese:
        return is_match(
            r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$",
            email)
    else:
        return is_match(
            r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$",
            email)


def is_name(name: str, country: int = CHINA):
    """
    Is This a Name

    Parameters
    ----------
    name:Name
    country:Country(0:China, 1:INTONATIONAL)

    Returns
    -------
    True/False

    References
    -----------
    https://blog.csdn.net/wwwind213/article/details/80167016
    https://blog.csdn.net/kekekeqi/article/details/80881718

    Raises
    -------
    ValueError("country is invalid")
    """
    if country == CHINA:
        return is_match(r"^[\u4E00-\u9FA5\uf900-\ufa2d·s]{2,20}$", name)

    elif country == INTONATIONAL:
        return is_match(r"^([\\u4e00-\\u9fa5]{1,20}|[a-zA-Z\\.\\s]{1,20})$", name)

    else:
        raise ValueError("country is invalid")


def is_url(url: str):
    """
    Is url a valid url

    Parameters
    ----------
    url:url

    Returns
    -------
    True/False

    Warnings
    ---------
    Only Match http/ftp/https Protocols

    References
    ----------
    https://www.cnblogs.com/zlong123/p/10531680.html


    """
    return is_match(r"((http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?)",
                    url)


def is_chinese_id_card_code(code: str):
    """
    Is code a Valid A Chinese IDCard Code

    Parameters
    ----------
    code:IDCard Code

    Returns
    -------
    True/False

    References
    ----------
    https://blog.csdn.net/qiphon3650/article/details/95541641
    """
    return is_match(r"[1-9]\d{5}(18|19|20|(3\d))\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$",
                    code)


def is_phone_number(phone: str, area: str=""):
    """
    Is a valid phone number



    Parameters
    ----------
    phone:Phone Number

    Returns
    -------
    True/False

    Raises
    ------
    IndexError

    Warnings
    ---------
    Only Support:
    ar-DZ,
    ar-SY,
    ar-SA,
    en-US,
    cs-CZ,
    de-DE,
    da-DK,
    el-GR,
    en-AU,
    en-GB,
    en-HK,
    en-IN,
    en-NZ,
    en-ZA,
    en-ZM,
    es-ES,
    fi-FI,
    fr-FR,
    he-IL,
    hu-HU,
    it-IT,
    ja-JP,
    ms-MY,
    nb-NO,
    nl-BE,
    nn-NO,
    pl-PL,
    pt-BR,
    pt-PT,
    ru-RU,
    sr-RS,
    tr-TR,
    vi-VN,
    zh-CN,
    zh-TW

    References
    ----------
    https://www.pythonheidong.com/blog/article/6118/
    """

    return is_match(phone_patterns[area],
                    phone)


