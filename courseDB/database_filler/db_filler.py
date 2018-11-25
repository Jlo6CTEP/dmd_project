import itertools
import math
import sys
import re
import sqlite3
import os
import random
from copy import deepcopy
from sqlite3 import IntegrityError

return_types = {'integer': lambda x: int(''.join(list(map(str, x)))),
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


def handle_token(term, create_list, x, unique_randint):
    if term in term_notxt:
        return term_files[term][random.randint(0, len(term_files[term]) - 1)]
    elif re.sub('\(.*\)', '', term) in nonterm_notxt:
        term_no_args = re.sub('\(.*\)', '', term)
        args = re.sub(term_no_args + '\(|\)', '', term).replace(' ', '').split(',')
        return_type = return_types[nonterm_files[term_no_args].split(' ')[0].strip(' ')]

        if re.fullmatch('int\(\d*,\d*\)', term):
            return random.randint(*map(int, args))
        if re.fullmatch('unique_int\(\d*,\d*\)', term):
            x[0] += 1
            rand_range = list(map(int, args))
            if create_list:
                unique_randint.append(random.sample(range(*rand_range), rand_range[1] - rand_range[0]))
            return unique_randint[x[0]].pop(0)
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
            if len(literal) > 0:
                parsed.append(literal)
            return return_type([handle_token(x, create_list, x, unique_randint) for x in parsed if x])
    else:
        return term


def main(*args):
    print('First provide table name and number of elements to be filled as "table your_table_name your_int"')
    print('Finally provide templates to fill DB in form "your_column_name entry" ')
    print('where Entry is name of terminal or nonterminal from corresponding folders')
    print('When done with one table, prompt "table your_table_name" again, to start work with another')
    print('Input one statement per line, when done, prompt ";" symbol')
    # db_name = args[0][1].replace("\\\\", '\\')

    db_name = '..\\courseDB'
    connection = sqlite3.connect(db_name)
    db = connection.cursor()

    table_list = [name[0] for name in db.execute("SELECT name FROM sqlite_master WHERE type='table';")]
    table_contents = [list(x[1] for x in db.execute("PRAGMA table_info({})".format(x)).fetchall()) for x in table_list]

    table_info = {name: field for name, field in zip(table_list, table_contents)}

    x = ""
    raw_input = ""
    while not x.endswith(';'):
        x = (input('>>>'))
        raw_input += '\n' + x

    raw_input = ['table' + x for x in re.sub('\n\n+', '', raw_input.replace(';', '')).split('table')]
    commands = [[x.strip().split(' ') for x in record.split('\n')] for record in raw_input]
    # commands = [dict([('kek', 'kek') for line in record]) for record in raw_input]
    print('*')

    flag = False
    unique_sequence = []
    data_full = []
    for record in commands[1:]:
        flag = False
        create_unique_list = True
        header = record[0]
        create_list = []
        alt = [-1]
        for f in range(int(header[2])):
            data_full = []
            for x in record[1:]:
                if x[0] == 'record':
                    data_full += [[x[1]]]
                    data_full += [[handle_token(x[2], create_unique_list, alt, create_list)]]
                if x[0] == 'foreign':
                    table1 = list(db.execute("SELECT {} FROM {}".format(x[2], x[3])))
                    data_full += [[x[1]]]
                    data_full += [[random.sample(table1, 1)]]
            create_unique_list = False
            alt = [-1]

            for relation in [x for x in record[1:] if x[0] == 'relation']:
                table1 = list(db.execute("SELECT {} FROM {}".format(relation[2], relation[1])))
                table2 = list(db.execute("SELECT {} FROM {}".format(relation[4], relation[3])))

                if relation[5] == 'N-N':
                    data_full[0] += [relation[2]]
                    data_full[1] += random.sample(table1, 1)
                    data_full[0] += [relation[4]]
                    data_full[1] += random.sample(table2, 1)
                elif relation[5] == '1-N':
                    if not flag:
                        unique_sequence = random.sample(table1, len(table1))
                    flag = True
                    data_full[0] += [relation[2]]
                    data_full[1] += unique_sequence.pop(0)
                    data_full[0] += [relation[4]]
                    data_full[1] += random.sample(table1, 1)
                else:
                    data_full[0] += [relation[2]]
                    data_full[1] += table1.pop(random.randint(0, len(table1)-1))
                    data_full[0] += [relation[4]]
                    data_full[1] += table2.pop(random.randint(0, len(table2)-1))
            db.execute('INSERT INTO {} ({}) VALUES ({})'.format(header[1], ','.join(data_full[0]),
                                                                ','.join(map(str, data_full[1]))))
        print()
    connection.commit()
    connection.close()

    print()


if __name__ == '__main__':
    main(sys.argv)
