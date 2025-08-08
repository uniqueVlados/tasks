import re


def normalize_phone(phone: str) -> str:
    digits = re.sub(r'\D', '', phone)

    if len(digits) == 11:
        if digits[0] == '8':
            digits = '7' + digits[1:]
    elif len(digits) == 10:
        digits = '7' + digits
    else:
        raise ValueError(f"Invalid phone number length: {phone}")

    return f"+{digits}"


def normalize_fullname(fullname: str) -> str:
    parts = re.split(r'\s+', fullname.strip())
    cleaned_parts = []
    for part in parts:
        if not part:
            continue
        capitalized_subparts = [sub.capitalize()
                                for sub in re.split(r'(-)', part) if sub]
        cleaned_part = ''.join(capitalized_subparts)
        cleaned_parts.append(cleaned_part)
    return ' '.join(cleaned_parts)


def normalize_amount(amount: str) -> float:
    cleaned = amount.strip().replace(' ', '').replace(',', '.')
    return float(cleaned)
