import re

def is_roman_number(num):

    pattern = re.compile(r"""   
                                ^M{0,3}
                                (CM|CD|D?C{0,3})?
                                (XC|XL|L?X{0,3})?
                                (IX|IV|V?I{0,3})?$
            """, re.VERBOSE)

    if re.match(pattern, num):
        return True

    return False


test_string = input("Enter string: ")
if is_roman_number(test_string):
    print('Yessss')
else:
    print('Nope!')