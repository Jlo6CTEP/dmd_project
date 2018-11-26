import sqlite3
import os

DB_PATH = "../courseDB/courseDB"
DP_PATH = os.getcwd()[:-5] + "courseDB/courseDB"


# Each queryN method returns string output without separators and stuff


def query1():
    cursor.execute("SELECT * FROM car WHERE color = 'red' AND license_plate LIKE 'A%%%N%'")
    res = cursor.fetchall()  # getting results
    res = "\n".join([str(x) for x in res])
    return res


def query2(given_date):  # YYYY-MM-DD hh:mm:ss
    cursor.execute("SELECT start_time>end_time from car_charging_station")
    for rec in cursor.fetchall():
        print(rec[0])

    cursor.execute(
        "SELECT station_id, start_time, end_time FROM car_charging_station WHERE date(start_time) = {} or date(end_time) = {}".format(
            given_date, given_date))
    used = [set() for h in range(24)]
    for rec in cursor.fetchall():
        print(rec)

    return "test2"


def query3():
    return "test3"


def query4():
    return "test4"


def query5():
    return "test5"


def query6():
    return "test6"


def query7():
    return "test7"


def query8():
    return "test8"


def query9():
    return "test9"


def query10():
    return "test10"



def do_query(query_name, input_data=None):
    global cursor

    print(query_name, "|", task_list.task[query_name])  # Prints query in human language

    conn = sqlite3.connect(DB_PATH)  # connection to DB
    cursor = conn.cursor()  # object that does queries and return their result

    query_num = query_name.split()[-1]  # Gets numerical identifier of query (from 1 to 10)
    args = ["input_data", ""][input_data is None]  # Prepares argument
    funct = "query" + query_num + "(" + args + ")"  # Prepares function
    res = eval(funct)  # Evaluates function

    # Mb dict of functions ll be better? I mean, eval is not good

    print(res)
    print()

    conn.close()  # closing connection with DB
    return res


do_query("Query 1 ")
do_query("Query 2 ", "2018-11-01")
# do_query("Query 3 ")
