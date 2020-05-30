import random
import re
import unicodedata
from datetime import date
from decimal import Decimal
from random import randint
from typing import Tuple, Optional
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.utils.translation import gettext as _
from jutil.bank_const_iban import IBAN_LENGTH_BY_COUNTRY
# Country-specific bank constants (abc-order):
from jutil.bank_const_be import BE_BIC_BY_ACCOUNT_NUMBER, BE_BANK_NAME_BY_BIC
from jutil.bank_const_dk import DK_BANK_CLEARING_MAP
from jutil.bank_const_fi import FI_BIC_BY_ACCOUNT_NUMBER, FI_BANK_NAME_BY_BIC
from jutil.bank_const_se import SE_BANK_CLEARING_LIST


EMAIL_VALIDATOR = re.compile(r'[a-zA-Z0-9\._-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+')
PHONE_FILTER = re.compile(r'[^+0-9]')
PHONE_VALIDATOR = re.compile(r'\+?\d{6,}')
PASSPORT_FILTER = re.compile(r'[^-A-Z0-9]')
STRIP_NON_NUMBERS = re.compile(r'[^0-9]')
STRIP_NON_ALPHANUMERIC = re.compile(r'[^0-9A-Za-z]')
STRIP_WHITESPACE = re.compile(r'\s+')
IBAN_FILTER = re.compile(r'[^A-Z0-9]')
DIGIT_FILTER = re.compile(r'[^0-9]')


def phone_filter(v: str) -> str:
    return PHONE_FILTER.sub('', str(v)) if v else ''


def phone_validator(v: str):
    v = phone_filter(v)
    if not v or not PHONE_VALIDATOR.fullmatch(v):
        v_str = _('Missing value') if v is None else str(v)
        raise ValidationError(_('Invalid phone number') + ': {}'.format(v_str), code='invalid_phone')


def phone_sanitizer(v: str) -> str:
    v = phone_filter(v)
    if not v or not PHONE_VALIDATOR.fullmatch(v):
        return ''
    return v


def email_filter(v: str) -> str:
    return str(v).lower().strip() if v else ''


def email_validator(v: str):
    v = email_filter(v)
    if not v or not EMAIL_VALIDATOR.fullmatch(v):
        v_str = _('Missing value') if not v else str(v)
        raise ValidationError(_('Invalid email') + ': {}'.format(v_str), code='invalid_email')


def email_sanitizer(v: str) -> str:
    v = email_filter(v)
    if not v or not EMAIL_VALIDATOR.fullmatch(v):
        return ''
    return v


def passport_filter(v: str) -> str:
    return PASSPORT_FILTER.sub('', str(v).upper()) if v else ''


def passport_validator(v: str):
    v = passport_filter(v)
    if not v or len(v) < 5:
        v_str = _('Missing value') if v is None else str(v)
        raise ValidationError(_('Invalid passport number') + ': {}'.format(v_str), code='invalid_passport')


def passport_sanitizer(v: str):
    v = passport_filter(v)
    if not v or len(v) < 5:
        return ''
    return v


def country_code_filter(v: str) -> str:
    return v.strip().upper()


def bic_filter(v: str) -> str:
    return v.strip().upper()


def country_code_validator(v: str):
    """
    Accepts both ISO-2 and ISO-3 formats.
    :param v: str
    :return: None
    """
    v = country_code_filter(v)
    if not (2 <= len(v) <= 3):
        v_str = _('Missing value') if v is None else str(v)
        raise ValidationError(_('Invalid country code') + ': {}'.format(v_str), code='invalid_country_code')


def country_code_sanitizer(v: str) -> str:
    v = country_code_filter(v)
    return v if 2 <= len(v) <= 3 else ''


def bic_sanitizer(v: str) -> str:
    v = bic_filter(v)
    return v if 8 <= len(v) <= 11 else ''


def ascii_filter(v: str) -> str:
    """
    Replaces Unicode accent characters with plain ASCII.
    For example remove_accents('HELÉN') == 'HELEN'.
    :param v: str
    :return: str
    """
    return unicodedata.normalize('NFKD', v).encode('ASCII', 'ignore').decode()


def digit_filter(v: str) -> str:
    return DIGIT_FILTER.sub('', str(v)) if v else ''


def iban_filter(v: str) -> str:
    return IBAN_FILTER.sub('', str(v).upper()) if v else ''


def iban_filter_readable(acct) -> str:
    acct = iban_filter(acct)
    if acct:
        i = 0
        j = 4
        out = ''
        nlen = len(acct)
        while i < nlen:
            if out:
                out += ' '
            out += acct[i:j]
            i = j
            j += 4
        return out
    return acct


def bic_validator(v: str):
    """
    Validates bank BIC/SWIFT code (8-11 characters).
    :param v: str
    :return: None
    """
    v = bic_filter(v)
    if not (8 <= len(v) <= 11):
        v_str = _('Missing value') if v is None else str(v)
        raise ValidationError(_('Invalid bank BIC/SWIFT code') + ': {}'.format(v_str), code='invalid_bic')


def iban_validator(v: str):
    """
    Validates IBAN format bank account number.
    :param v: str
    :return: None
    """
    # validate prefix and length
    v = iban_filter(v)
    if not v:
        raise ValidationError(_('Invalid IBAN account number') + ': {}'.format(_('Missing value')), code='invalid_iban')
    country = v[:2].upper()
    if country not in IBAN_LENGTH_BY_COUNTRY:
        raise ValidationError(_('Invalid IBAN account number') + ': {}'.format(v), code='invalid_iban')
    iban_len = IBAN_LENGTH_BY_COUNTRY[country]
    if iban_len != len(v):
        raise ValidationError(_('Invalid IBAN account number') + ': {}'.format(v), code='invalid_iban')

    # validate IBAN numeric part
    if iban_len <= 26:  # very long IBANs are unsupported by the numeric part validation
        digits = '0123456789'
        num = ''
        for ch in v[4:] + v[0:4]:
            if ch not in digits:
                ch = str(ord(ch) - ord('A') + 10)
            num += ch
        x = Decimal(num) % Decimal(97)
        if x != Decimal(1):
            raise ValidationError(_('Invalid IBAN account number') + ': {}'.format(v), code='invalid_iban')


def iban_generator(country_code: str = '') -> str:
    """
    Generates IBAN format bank account number (for testing).
    :param country_code: 2-character country code (optional)
    :return: str
    """
    # pick random country code if not set (with max IBAN length 27)
    if not country_code:
        country_code = random.choice(  # nosec
            list(filter(lambda cc: IBAN_LENGTH_BY_COUNTRY[cc] <= 26, IBAN_LENGTH_BY_COUNTRY.keys())))
    nlen = IBAN_LENGTH_BY_COUNTRY[country_code]
    if nlen > 26:
        raise ValidationError(_('IBAN checksum generation does not support >26 character IBANs'), code='invalid_iban')

    # generate BBAN part
    if country_code not in IBAN_LENGTH_BY_COUNTRY:
        raise ValidationError(_('Invalid country code') + ': {}'.format(country_code), code='invalid_country_code')
    digits = '0123456789'
    bban = ''.join([random.choice(digits) for n in range(nlen - 4)])  # nosec

    # generate valid IBAN numeric part
    # (probably not the most efficient way to do this but write a better one if you need faster...)
    num0 = ''
    for ch in bban + country_code:
        if ch not in digits:
            ch = str(ord(ch) - ord('A') + 10)
        num0 += ch
    for checksum in range(1, 100):
        num = num0
        checksum_str = '{:02}'.format(checksum)
        for ch in checksum_str:
            if ch not in digits:
                ch = str(ord(ch) - ord('A') + 10)
            num += ch
        # print(num, '/', 97, 'nlen', nlen)
        x = Decimal(num) % Decimal(97)
        if x == Decimal(1):
            return country_code + checksum_str + bban

    raise ValidationError(_('Invalid IBAN account number'), code='invalid_iban')  # should not get here


def validate_country_iban(v: str, country: str):
    v = iban_filter(v)
    if v[0:2] != country:
        raise ValidationError(_('Invalid IBAN account number') + ' ({}.2): {}'.format(country, v), code='invalid_iban')
    iban_validator(v)


def iban_bank_info(v: str) -> Tuple[str, str]:
    """
    Returns BIC code and bank name from IBAN number.
    :param v: IBAN account number
    :return: (BIC code, bank name) or ('', '') if not found / unsupported country
    """
    v = iban_filter(v)
    prefix = v[:2]
    func_name = prefix.lower() + '_iban_bank_info'  # e.g. fi_iban_bank_info, be_iban_bank_info
    func = globals().get(func_name)
    if func is not None:
        return func(v)
    return '', ''


def iban_bic(v: str) -> str:
    """
    Returns BIC code from IBAN number.
    :param v: IBAN account number
    :return: BIC code or '' if not found
    """
    info = iban_bank_info(v)
    return info[0] if info else ''


def calculate_age(born: date, today: Optional[date] = None) -> int:
    if not today:
        today = now().date()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def filter_country_company_org_id(country_code: str, v: str):
    if country_code == 'FI':
        return fi_company_org_id_filter(v)
    return PASSPORT_FILTER.sub('', v)


def validate_country_company_org_id(country_code: str, v: str):
    if country_code == 'FI':
        fi_company_org_id_validator(v)


# ============================================================================
# Country specific functions (countries in alphabetical order)
# ============================================================================


# ----------------------------------------------------------------------------
# Belgium
# ----------------------------------------------------------------------------

def be_iban_validator(v: str):
    validate_country_iban(v, 'BE')


def be_iban_bank_info(v: str) -> Tuple[str, str]:
    """
    Returns BIC code and bank name from BE IBAN number.
    :param v: IBAN account number
    :return: (BIC code, bank name) or ('', '') if not found
    """
    v = iban_filter(v)
    bic = BE_BIC_BY_ACCOUNT_NUMBER.get(v[4:7], None)
    return (bic, BE_BANK_NAME_BY_BIC[bic]) if bic is not None else ('', '')


# ----------------------------------------------------------------------------
# Denmark
# ----------------------------------------------------------------------------

def dk_iban_validator(v: str):
    validate_country_iban(v, 'DK')


def dk_clearing_code_bank_name(v: str) -> str:
    v = iban_filter(v)
    if v.startswith('DK'):
        v = v[4:]
    return DK_BANK_CLEARING_MAP.get(v[:4], '')


def dk_iban_bank_info(v: str) -> Tuple[str, str]:
    """
    Returns empty string (BIC not available) and bank name from DK IBAN number.
    DK5000400440116243
    :param v: IBAN account number
    :return: ('', bank name) or ('', '') if not found
    """
    return '', dk_clearing_code_bank_name(v)


# ----------------------------------------------------------------------------
# Estonia
# ----------------------------------------------------------------------------

def ee_iban_validator(v: str):
    validate_country_iban(v, 'EE')


# ----------------------------------------------------------------------------
# Finland
# ----------------------------------------------------------------------------

FI_SSN_FILTER = re.compile(r'[^-A-Z0-9]')
FI_SSN_VALIDATOR = re.compile(r'^\d{6}[+-A]\d{3}[\d\w]$')
FI_COMPANY_ORG_ID_FILTER = re.compile(r'[^0-9]')


def fi_payment_reference_number(num: str):
    """
    Appends Finland reference number checksum to existing number.
    :param num: At least 3 digits
    :return: Number plus checksum
    """
    assert isinstance(num, str)
    num = STRIP_WHITESPACE.sub('', num)
    num = re.sub(r'^0+', '', num)
    assert len(num) >= 3
    weights = [7, 3, 1]
    weighed_sum = 0
    numlen = len(num)
    for j in range(numlen):
        weighed_sum += int(num[numlen - 1 - j]) * weights[j % 3]
    return num + str((10 - (weighed_sum % 10)) % 10)


def fi_payment_reference_validator(v: str):
    v = STRIP_WHITESPACE.sub('', v)
    if fi_payment_reference_number(v[:-1]) != v:
        raise ValidationError(_('Invalid payment reference: {}').format(v))


def iso_payment_reference_validator(v: str):
    """
    Validates ISO reference number checksum.
    :param v: Reference number
    """
    num = ''
    v = STRIP_WHITESPACE.sub('', v)
    for ch in v[4:] + v[0:4]:
        x = ord(ch)
        if ord('0') <= x <= ord('9'):
            num += ch
        else:
            x -= 55
            if x < 10 or x > 35:
                raise ValidationError(_('Invalid payment reference: {}').format(v))
            num += str(x)
    res = Decimal(num) % Decimal('97')
    if res != Decimal('1'):
        raise ValidationError(_('Invalid payment reference: {}').format(v))


def fi_iban_validator(v: str):
    validate_country_iban(v, 'FI')


def fi_iban_bank_info(v: str) -> Tuple[str, str]:
    """
    Returns BIC code and bank name from FI IBAN number.
    :param v: IBAN account number
    :return: (BIC code, bank name) or ('', '') if not found
    """
    v = iban_filter(v)
    bic = FI_BIC_BY_ACCOUNT_NUMBER.get(v[4:7], None)
    return (bic, FI_BANK_NAME_BY_BIC[bic]) if bic is not None else ('', '')


def fi_ssn_filter(v: str) -> str:
    return FI_SSN_FILTER.sub('', v.upper())


def fi_company_org_id_filter(v: str) -> str:
    v = FI_COMPANY_ORG_ID_FILTER.sub('', v)
    return v[:-1] + '-' + v[-1:] if len(v) >= 2 else ''


def fi_company_org_id_validator(v0: str):
    v = fi_company_org_id_filter(v0)
    prefix = v[:2]
    if v[-2:-1] != '-' and prefix != 'FI':
        raise ValidationError(_('Invalid company organization ID')+' (FI.1): {}'.format(v0), code='invalid_company_org_id')
    v = v.replace('-', '', 1)
    if len(v) != 8:
        raise ValidationError(_('Invalid company organization ID')+' (FI.2): {}'.format(v0), code='invalid_company_org_id')
    multipliers = (7, 9, 10, 5, 8, 4, 2)
    x = 0
    for i, m in enumerate(multipliers):
        x += int(v[i]) * m
    remainder = divmod(x, 11)[1]
    if remainder == 1:
        raise ValidationError(_('Invalid company organization ID')+' (FI.3): {}'.format(v0), code='invalid_company_org_id')
    if remainder >= 2:
        check_digit = str(11 - remainder)
        if check_digit != v[-1:]:
            raise ValidationError(_('Invalid company organization ID')+' (FI.4): {}'.format(v0), code='invalid_company_org_id')


def fi_company_org_id_generator() -> str:
    remainder = 1
    v = ''
    while remainder < 2:
        v = str(randint(11111111, 99999999))  # nosec
        multipliers = (7, 9, 10, 5, 8, 4, 2)
        x = 0
        for i, m in enumerate(multipliers):
            x += int(v[i]) * m
        remainder = divmod(x, 11)[1]
    check_digit = str(11 - remainder)
    return v[:-1] + '-' + check_digit


def fi_ssn_validator(v: str):
    v = fi_ssn_filter(v)
    if not FI_SSN_VALIDATOR.fullmatch(v):
        raise ValidationError(_('Invalid personal identification number')+' (FI.1): {}'.format(v), code='invalid_ssn')
    d = int(Decimal(v[0:6] + v[7:10]) % Decimal(31))
    digits = {
        10: 'A', 	11: 'B', 	12: 'C', 	13: 'D', 	14: 'E', 	15: 'F', 	16: 'H',
        17: 'J', 	18: 'K', 	19: 'L', 	20: 'M', 	21: 'N', 	22: 'P', 	23: 'R',
        24: 'S', 	25: 'T', 	26: 'U', 	27: 'V', 	28: 'W', 	29: 'X', 	30: 'Y',
    }
    ch = digits.get(d, str(d))
    if ch != v[-1:]:
        raise ValidationError(_('Invalid personal identification number')+' (FI.2): {}'.format(v), code='invalid_ssn')


def fi_ssn_generator():
    day = randint(1, 28)  # nosec
    month = randint(1, 12)  # nosec
    year = randint(1920, 1999)  # nosec
    suffix = randint(100, 999)  # nosec
    v = '{:02}{:02}{:02}-{}'.format(day, month, year-1900, suffix)
    d = int(Decimal(v[0:6] + v[7:10]) % Decimal(31))
    digits = {
        10: 'A', 	11: 'B', 	12: 'C', 	13: 'D', 	14: 'E', 	15: 'F', 	16: 'H',
        17: 'J', 	18: 'K', 	19: 'L', 	20: 'M', 	21: 'N', 	22: 'P', 	23: 'R',
        24: 'S', 	25: 'T', 	26: 'U', 	27: 'V', 	28: 'W', 	29: 'X', 	30: 'Y',
    }
    ch = digits.get(d, str(d))
    return v + ch


def fi_ssn_birthday(v: str) -> date:
    v = fi_ssn_filter(v)
    fi_ssn_validator(v)
    sep = v[6]  # 231298-965X
    year = int(v[4:6])
    month = int(v[2:4])
    day = int(v[0:2])
    if sep == '+':  # 1800
        year += 1800
    elif sep == '-':
        year += 1900
    elif sep == 'A':
        year += 2000
    return date(year, month, day)


def fi_ssn_age(ssn: str, today: Optional[date] = None) -> int:
    return calculate_age(fi_ssn_birthday(ssn), today)


# ----------------------------------------------------------------------------
# Sweden
# ----------------------------------------------------------------------------

SE_SSN_FILTER = re.compile(r'[^-0-9]')
SE_SSN_VALIDATOR = re.compile(r'^\d{6}[-]\d{3}[\d]$')


def se_iban_validator(v: str):
    validate_country_iban(v, 'SE')


def se_ssn_filter(v: str) -> str:
    return SE_SSN_FILTER.sub('', v.upper())


def se_ssn_validator(v: str):
    v = se_ssn_filter(v)
    if not SE_SSN_VALIDATOR.fullmatch(v):
        raise ValidationError(_('Invalid personal identification number')+' (SE.1): {}'.format(v), code='invalid_ssn')
    v = STRIP_NON_NUMBERS.sub('', v)
    dsum = 0
    for i in range(9):
        x = int(v[i])
        if i & 1 == 0:
            x += x
        # print('summing', v[i], 'as', x)
        xsum = x % 10 + int(x/10) % 10
        # print(v[i], 'xsum', xsum)
        dsum += xsum
    # print('sum', dsum)
    rem = dsum % 10
    # print('rem', rem)
    checksum = 10 - rem
    if checksum == 10:
        checksum = 0
    # print('checksum', checksum)
    if int(v[-1:]) != checksum:
        raise ValidationError(_('Invalid personal identification number')+' (SE.2): {}'.format(v), code='invalid_ssn')


def se_clearing_code_bank_info(account_number: str) -> Tuple[str, Optional[int]]:
    """
    Returns Sweden bank info by clearning code.
    :param account_number: Swedish account number with clearing code as prefix
    :return: (Bank name, account digit count) or ('', None) if not found
    """
    v = digit_filter(account_number)
    clearing = v[:4]
    for name, begin, end, acc_digits in SE_BANK_CLEARING_LIST:
        if begin <= clearing <= end:
            return name, acc_digits
    return '', None
