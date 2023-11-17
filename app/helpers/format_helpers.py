import re


def license_plate_validator(string):
    new_arg_format = r'^[A-Za-z]{2}\d{3}[A-Za-z]{2}$'
    old_arg_format = r'^[A-Za-z]{3}\d{3}$'

    if re.match(new_arg_format, string):
        return re.findall(new_arg_format, string)
    elif re.match(old_arg_format, string):
        return re.findall(old_arg_format, string)
    else:
        return None
