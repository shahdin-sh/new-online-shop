import re


def persian_to_western_digits(text):
    digits_mapping = {
        '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
        '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'
    }
    return re.sub('[۰-۹]', lambda x: digits_mapping[x.group()], text)