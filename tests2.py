import re
import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

start_parse = False
tracking = False
data_dict = {}
paragraph_count = 0
footnote_count = 0
append_line = {
    'append': False,
    'spaced': False,
    'index': None
}
start_new_line = False


footnote_pattern = re.compile(r'^(\d)+[\s][a-zA-Z]+')

def convert_to_integer(integer):
    try:
        integer = int(integer)      
    except ValueError:
        return False
    return True

def reset_append():
    return {
    'append': False,
    'spaced': False,
    'index': None
}


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

def crawl_spaces(line, pos='end'):

    if pos!='end':
        forward_index = 0
        if line[forward_index] == ' ':
            while line[forward_index] == ' ':
                forward_index += 1
        return line[forward_index], forward_index
    else:
        reverse_index = -1
        if line[reverse_index] == ' ':
            while line[reverse_index] == ' ':
                reverse_index -= 1
        return line[reverse_index], reverse_index


def clean_up(line):

    global data_dict
    global append_line
    global start_new_line

    append = False

    if append_line['append'] and paragraph_count > 0:

        last_entry = list(data_dict.keys())[-1]

        if 'footnote' in last_entry:
            last_entry = list(data_dict.keys())[-2]

        if append_line['spaced']:
            data_dict[last_entry] += ' ' + line
        else:
            hyphen_index = append_line['index']
            data_dict[last_entry] = data_dict[last_entry][:hyphen_index]
            data_dict[last_entry] += line
        append = True   

    last_character, index = crawl_spaces(line)

    if last_character == '-' or last_character != '.':

        if last_character == '-':
            append_line['spaced'] = False
            append_line['index'] = index
        elif last_character.islower():
            append_line['spaced'] = True
            append_line['index'] = None

        append_line['append'] = True

    else:
        append_line = {
        'append': False,
        'spaced':False,
        'index': None
        }

    if start_new_line:
        start_new_line = False
        return start_new_line

    return append


def handle_footnotes(line):

    global footnote_count
    global tracking
    global start_new_line
    footnote_markers = ['•', '*']

    first_character, _ = crawl_spaces(line, pos='start')
    footnote_match = footnote_pattern.search(line)

    if tracking:
        last_character, index = crawl_spaces(line)
        if last_character == '-':
            line = line[:index]
            data_dict[f'footnote{footnote_count}'] += line
        else:
            data_dict[f'footnote{footnote_count}'] += ' ' + line
        return True

    elif first_character in footnote_markers or footnote_match:

        if footnote_match and start_new_line:
            start_new_line = False
            return False

        if not tracking:
            footnote_count += 1
            data_dict[f'footnote{footnote_count}'] = line
            tracking = True

        return True

    return False

def parse_text(infile):

    global append_line, tracking, start_new_line, start_parse, data_dict, paragraph_count

    with open(infile, 'r', errors='ignore', encoding='utf-8') as source:

        for line in source.readlines():

            line = line.strip('\n')

            if line.strip(' ') == "LXVI":
                start_parse = True

            # if convert_to_integer(line.stri)

            if start_parse:
                if line == '':
                    paragraph_count += 1
                    start_new_line = True
                    tracking = False
                    append_line = reset_append()

                elif not handle_footnotes(line) and not clean_up(line):
                    paragraph_count += 1
                    data_dict[str(paragraph_count)] = line

        for key, value in data_dict.items():
            print(key + ': ' + value)


if __name__ == '__main__':
    infile = './tr-texts/Kritzman Die heroische Periode der grossen russischen Revolution TXT 1.txt'
    parse_text(infile)