import random
import sys
import re
import subprocess as sb
import glob
import os
import random

return_types = {'integer': lambda x: ''.join(list(map(int, x))),
                'string': lambda x: ''.join(list(map(str, x))),
                'chr': lambda x: ''.join(list(map(chr, x)))}

nonterm_txt = [files for paths, dirs, files in os.walk('.\\sample_data\\nonterminal')][0]
nonterm_notxt = [x.replace('.txt', '') for x in nonterm_txt]
nonterm_path = [os.path.join('.\\sample_data\\nonterminal', file) for file in nonterm_txt]

nonterm_files = {name: file for name, file in zip(nonterm_notxt, [open(x, 'r').read() for x in nonterm_path])}

term_txt = [files for paths, dirs, files in os.walk('.\\sample_data\\terminal')][0]
term_notxt = [x.replace('.txt', '') for x in term_txt]
term_path = [os.path.join('.\\sample_data\\terminal', file) for file in term_txt]
term_files = {name: file for name, file in zip(term_notxt, [open(x, 'r').read().split(',') for x in term_path])}


def handle_token(term):
    if term in term_notxt:
        return term_files[term][random.randint(0, len(term_files[term]) - 1)]
    elif re.sub('\(.*\)', '', term) in nonterm_notxt:
        term_no_args = re.sub('\(.*\)', '', term)
        args = re.sub(term_no_args + '\(|\)', '', term).replace(' ', '').split(',')
        return_type = return_types[nonterm_files[term_no_args].split(' ')[0].strip(' ')]
        if re.fullmatch('int\(\d*,\d*\)', term):
            return random.randint(*map(int, args))
        else:
            parsed = []
            literal = ""
            to_parse = ' '.join(nonterm_files[term_no_args].split(' ')[1:])

            regex = re.compile('|'.join(sorted(term_notxt + nonterm_notxt, key=lambda x: 1 / len(x))))
            while len(to_parse) > 0:
                repl = re.match(regex, to_parse)
                if repl:
                    repl = repl.group()
                    if len(literal) > 0:
                        parsed.append(literal)
                        literal = ''
                    if repl in term_notxt:
                        to_parse = to_parse.replace(repl, '', 1)
                        parsed.append(repl)
                    elif repl in nonterm_notxt:
                        parsed.append(to_parse[:to_parse.index(')') + 1])
                        to_parse = to_parse[to_parse.index(')') + 1:]
                else:
                    literal += to_parse[0]
                    to_parse = to_parse[1:]
            return return_type([handle_token(x) for x in parsed if x])
    else:
        return term


def main(*args):
    print('Prompt templates to fill db')

    f = nonterm_files
    k = term_files

    print(''.join(handle_token('license_plate()')))

    # print(args)
    # db_name = args[0][1].replace("\\\\", '\\')

    db_name = '.\\courseDB\\courseDB'
    table_list = re.sub('( |\\r\\n)+', ' ', (sb.check_output("sqlite3 {} .tables".format(db_name)).decode()))

    x = input('>>>')
    commands = []
    while not x.endswith(';'):
        commands.append(x)
        x = input('>>>')

    print(commands)

    print(table_list)


if __name__ == '__main__':
    main(sys.argv)
