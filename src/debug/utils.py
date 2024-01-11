def iban_to_int(iban: str) -> int:
    # Convert letters to numbers (A=10, B=11, ..., Z=35)
    converted = ""
    for char in iban:
        if char.isdigit():
            converted += char
        else:
            converted += str(ord(char) - 55)
    return int(converted)


def is_iban_valid(iban: str) -> bool:
    # Remove spaces and convert to uppercase
    iban = iban.replace(" ", "").upper()

    # Country specific IBAN lengths (only DE added for simplicity)
    iban_lengths = {
        "DE": 22,
    }

    country_code = iban[:2]
    if country_code in iban_lengths and len(iban) == iban_lengths[country_code]:
        rearranged_iban = iban[4:] + iban[:4]
        integer_iban = iban_to_int(rearranged_iban)

        remainder = integer_iban % 97

        return remainder == 1
    else:
        return False
