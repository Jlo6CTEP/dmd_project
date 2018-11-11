import sys
import re
import subprocess as sb
import sqlite3
import os
import random

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
            if len(literal) > 0:
                parsed.append(literal)
            return return_type([handle_token(x) for x in parsed if x])
    else:
        return term


def main(*args):
    print('First provide table name and number of elements to be filled as "table your_table_name your_int"')
    print('Finally provide templates to fill DB in form "your_column_name entry" ')
    print('where Entry is name of terminal or nonterminal from corresponding folders')
    print('When done with one table, prompt "table your_table_name" again, to start work with another')
    print('When done, prompt ";" symbol')
    # db_name = args[0][1].replace("\\\\", '\\')

    db_name = '.\\courseDB\\courseDB'
    connection = sqlite3.connect(db_name)
    db = connection.cursor()

    table_list = [name[0] for name in db.execute("SELECT name FROM sqlite_master WHERE type='table';")]
    table_contents = [list(x[1] for x in db.execute("PRAGMA table_info({})".format(x)).fetchall()) for x in table_list]

    table_info = {name: field for name, field in zip(table_list, table_contents)}

    x = ""
    commands = {}
    one_table = []
    while not x.endswith(';'):
        x = input('>>>')
        if x != ';':
            if x.startswith('table') and len(one_table) != 0:
                commands.update({one_table[0].split(' ')[1]: one_table})
                one_table = []
            one_table.append(x)
    if len(one_table) != 0:
        commands.update({one_table[0].split(' ')[1]: one_table})

    for k, v in commands.items():
        commands.update({k: [[v[0].split(' ')[2]]] + [x.split() for x in v[1:]]})
    kek = {f: k for f, k in enumerate(table_contents[1])}

    data = {table: [commands[table][0]] + sorted(commands[table][1:], key=lambda x: {cont: enum for enum, cont
                            in enumerate(table_info[table])}[x[0]]) for table in commands.keys()}

    for k,v in data.items():
        for x in range(1, len(data[k])):
            data[k][x][1] = handle_token(data[k][x][1])


    for table_record in commands:
        for count in table_record[2]:
            db.execute('INSERT INTO ? (?) VALUES (?)', [table_record[0]])


if __name__ == '__main__':
    main(sys.argv)

# table bank_card 1000
# Security_code int(10,10000)
# Expire date()
# Number int(10,100000)
# table car_order 1000
# Order_ID int(0,1000)
# Cost int(0,1000)
# Destination location()
# ;
# for table in commands if table[0][0]
