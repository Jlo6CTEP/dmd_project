import sqlite3
import os
import task_list
from datetime import datetime, timedelta

DB_PATH = "../courseDB/courseDB"
DP_PATH = os.getcwd()[:-5] + "courseDB/courseDB"


# Each queryN method returns string output without separators and stuff

def query1(input_data):
    color, plate_let = input_data
    plate_let = plate_let + "%" * (3 - len(plate_let))
    plate = "{}%%%{}{}".format(plate_let[0], plate_let[1], plate_let[2])
    cursor.execute("SELECT * FROM car WHERE color = '{}' AND license_plate LIKE '{}'".format(color, plate))
    res = cursor.fetchall()  # getting results
    res = "\n".join([str(x) for x in res])
    return res


def query2(input_data):  # YYYY-MM-DD
    given_date = input_data[0]
    count = [0] * 24
    for h in range(24):
        hh = ["0" + str(h), str(h)][h >= 10]
        data = {"hh": hh, "given": given_date}
        q = "SELECT count(*) from car_charging_station " \
            "WHERE '{given} {hh}:00:00' <= start_time and start_time <= '{given} {hh}:59:59' " \
            "or '{given} {hh}:00:00' <= end_time and end_time <= '{given} {hh}:59:59'" \
            .format(**data)
        cursor.execute(q)
        count[h] = cursor.fetchall()[0][0]
    res = "\n".join([str(i) + "h-" + str(i + 1) + 'h: ' + str(count[i]) for i in range(24)])

    return res

def count_per_period(data): # dict with keys period_start, period_end, week_start, week_end
    q = '''SELECT COUNT(*) from car_order0 NATURAL JOIN car_order2 WHERE 
        (('{week_start}' <= date(initial_time) and date(initial_time) <= '{week_end}') or
         ('{week_start}' <= date(destination_time) and date(destination_time) <= '{week_end}')) and
        (('{period_start}' <= time(initial_time) and time(initial_time) <= '{period_end}') or
         ('{period_start}' <= time(destination_time) and time(destination_time) <= '{period_end}'))
        '''.format(**data)

    cursor.execute(q)
    return cursor.fetchall()[0][0]


def query3():
    cursor.execute("SELECT COUNT(car_id) FROM car")
    total = cursor.fetchall()[0][0]
    cursor.execute("SELECT date(end_time, '-7 day'),date(end_time) from car_charging_station")
    week_start, week_end = cursor.fetchall()[0]

    cnt = [0] * 3

    cnt[0] = count_per_period({"week_start": week_start,
                                "week_end": week_end,
                                "period_start": "07:00:00",
                                "period_end": "10:00:00"})
    cnt[1] = count_per_period({"week_start": week_start,
                                "week_end": week_end,
                                "period_start": "12:00:00",
                                "period_end": "14:00:00"})
    cnt[2] = count_per_period({"week_start": week_start,
                                "week_end": week_end,
                                "period_start": "17:00:00",
                                "period_end": "19:00:00"})
    periods = ["Morning", "Afternoon", "Evening"]
    percentage = [str(x / total * 100) for x in cnt]

    res = '     '.join(periods) + "\n" + \
          '     '.join([percentage[i] + " " * (len(periods[i]) - len(percentage[i])) for i in range(3)])
    return res


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


if __name__ == "__main__":
    do_query("Query 1", ["cobalt", "QB"])
    do_query("Query 2", ["2017-03-03"])
    do_query("Query 3")
