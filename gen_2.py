"""Endless gen with arguments string lenght, number and number of digits"""
import random
import string
import re


def endless_random_gen():
    """Generate the string of alphanumeric symbols"""
    choice_list = string.ascii_letters + string.digits
    while True:
        yield ''.join([random.choice(choice_list) for _ in xrange(1, random.randint(1, 80))])


def gen_validator(str_count, str_len=None, dig_numb=1):
    """Validator for endless_random_gen"""
    if str_len < dig_numb and str_len is not None:
        print "asd"
        return
    for cur_string in endless_random_gen():
        if str_count != 0:
            if len(re.findall(r'\d', cur_string)) == dig_numb:
                if str_len is not None:
                    if len(cur_string) == str_len:
                        yield cur_string
                        str_count -= 1
                else:
                    yield cur_string
                    str_count -= 1
        else:
            break


def gen_validator_decor():
    """Checking for arguments in gen_validator"""
    try:
        for _ in gen_validator(7):
            print _
    except TypeError:
        print 'Try with at least one argument!'


if __name__ == "__main__":
    gen_validator_decor()
