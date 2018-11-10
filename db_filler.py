import random
import sys
import re
import subprocess as sb
import glob
import os


def main(*args):
    print('Prompt templates to fill db')

    generic_txt = [files for paths, dirs, files in os.walk('.\\sample_data\\generic')][0]
    generic_notxt = [x.strip('.txt') for x in generic_txt]

    static_txt = [files for paths, dirs, files in os.walk('.\\sample_data\\static')][0]
    static_notxt = [x.strip('.txt') for x in static_txt]

    print(generic_notxt)
    print(generic_txt)
    print(static_notxt)
    print(static_txt)

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
