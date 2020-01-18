import re


def valid_phone(phone):
    phone_rule = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"
    return True if re.match(phone_rule, phone) else False


def valid_password(password):
    password_rule = "(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,16}$"
    return True if re.match(password_rule, password) else False
