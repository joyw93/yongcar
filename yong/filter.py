import locale
locale.setlocale(locale.LC_ALL, '')

def format_datetime(value, fmt='%Y-%m-%d %H:%M'):
    return value.strftime(fmt)