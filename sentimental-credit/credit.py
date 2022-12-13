from cs50 import get_int

# Luhn's algorithm


def checkvalid(cardnum, len):
    sum_even = 0
    sum_odd = 0
    for i in range(1, len+1):
        # extract digits
        current_digit = int((cardnum / pow(10, i-1)) % 10)
        # for even numbers
        if i % 2 == 0:
            product_even = current_digit * 2
            if (product_even < 10):
                # add digit
                sum_even += product_even
            else:
                # if digit * 2 > 10, add individual digits
                sum_even += (product_even - 9)
        # for odd numbers
        else:
            sum_odd += current_digit
        sum = sum_even + sum_odd
    # if sum ends with 0, valid
    if sum % 10 == 0:
        return True
    # if sum doesn't end with 0, invalid
    else:
        return False


def checkdigit(cardnum, digits):
    checkdigits = cardnum // pow(10, len(str(card_number))-digits)
    return checkdigits


# get card number
card_number = get_int("Number: ")
# check if length is valid: 16, 15 or 13 digits only
card_len = len(str(card_number))

if card_len != 16 and card_len != 15 and card_len != 13:
    print("INVALID\n")

# if length = 15, check first two digits for AMEX (34 or 37)
if card_len == 15:
    first_digits = checkdigit(card_number, 2)
    if first_digits != 34 and first_digits != 37:
        print("INVALID\n")
    else:
        valid = checkvalid(card_number, 15)
        if valid:
            print("AMEX\n")
        else:
            print("INVALID\n")


# if 13, check first digit for visa
    # then check valid
if card_len == 13:
    first_digits = checkdigit(card_number, 1)
    print(f"first digit: {first_digits}")
    if first_digits != 4:
        print("INVALID\n")
    else:
        valid = checkvalid(card_number, 13)
        if valid:
            print("VISA\n")
        else:
            print("INVALID\n")

if card_len == 16:
    # check digit for visa
    first_digits = checkdigit(card_number, 1)
    if checkdigit(card_number, 1) == 4:
        valid = checkvalid(card_number, 16)
        if valid:
            print("VISA\n")
        else:
            print("INVALID\n")
    elif checkdigit(card_number, 2) > 50 and checkdigit(card_number, 2) < 56:
        valid = checkvalid(card_number, 16)
        if valid:
            print("MASTERCARD\n")
        else:
            print("INVALID\n")
    else:
        print("INVALID\n")
