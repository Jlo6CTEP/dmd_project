import random
import sys
import re
import subprocess as sb
import glob
import os


def main(*args):

    os.chdir('.\\sample_data')
    files_txt = list(glob.glob('*.txt'))
    files_notxt = [x.strip('.txt') for x in glob.glob('*.txt')]

    os.chdir('..')

    #print(args)
    #db_name = args[0][1].replace("\\\\", '\\')
    db_name = '.\\courseDB\\courseDB'
    table_list = re.sub('( |\\r\\n)+', ' ', (sb.check_output("sqlite3 {} .tables".format(db_name)).decode()))

    print(table_list)

if __name__ == '__main__':
    main(sys.argv)
