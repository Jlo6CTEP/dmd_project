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
        q = """SELECT count(*) from car_charging_station
                WHERE '{given} {hh}:00:00' <= start_time and start_time <= '{given} {hh}:59:59'
                or '{given} {hh}:00:00' <= end_time and end_time <= '{given} {hh}:59:59'
                or start_time <= '{given} {hh}:00:00' and '{given} {hh}:59:59' <= end_time""".format(**data)
        cursor.execute(q)
        count[h] = cursor.fetchall()[0][0]
    res = "\n".join([str(i) + "h-" + str(i + 1) + 'h: ' + str(count[i]) for i in range(24)])

    return res


def count_per_period(data):  # dict with keys period_start, period_end, week_start, week_end
    q = '''SELECT COUNT(*) from car_order0 
        INNER JOIN car_order2 ON car_order0.pickup_location = car_order2.pickup_location and car_order0.destination_location = car_order2.destination_location 
        WHERE 
        (('{week_start}' <= date(initial_time) and date(initial_time) <= '{week_end}') or
         ('{week_start}' <= date(destination_time) and date(destination_time) <= '{week_end}')) and
        (('{period_start}' <= time(initial_time) and time(initial_time) <= '{period_end}') or
         ('{period_start}' <= time(destination_time) and time(destination_time) <= '{period_end}'))
        '''.format(**data)
    cursor.execute(q)
    res = cursor.fetchall()[0][0]
    return res


def query3(input_data):
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


def query4(input_data):
    username = input_data[0]
    cur_date = str(datetime.today()).split(" ")[0]
    month_before = str(datetime.today() - timedelta(days=30)).split(" ")[0]
    customer_id = 12

    data = {"username": username,
            "customer_id": customer_id,
            "cur_date": cur_date,
            "month_before": month_before}

    q = """SELECT * FROM car_order0 
            INNER JOIN car_order1 ON car_order0.initial_location = car_order1.initial_location and car_order0.pickup_location = car_order1.pickup_location and car_order0.initial_time = car_order1.initial_time 
            INNER JOIN customer ON customer.customer_id = car_order0.customer_id
            WHERE username = '{username}' AND '{month_before}' <= date(pickup_time) <= '{cur_date}'
            """.format(**data)
    cursor.execute(q)
    res = "\n".join([str(x) for x in cursor.fetchall()])
    return res


def query5(input_data):
    begin = cursor.execute("SELECT min(date(initial_time)) from car_order1").fetchall()[0][0]
    end = cursor.execute("SELECT max(date(destination_time)) from car_order2").fetchall()[0][0]

    a = datetime.strptime(begin, "%Y-%m-%d")
    b = datetime.strptime(end, "%Y-%m-%d")

    distance = 0
    duration = 0
    start_day = a.date()
    for i in range((b.date() - a.date()).days):
        start_day_str = str(start_day)
        q = """SELECT pickup_distance from car_order3 
        INNER JOIN car_order1 ON car_order3.initial_location = car_order1.initial_location and car_order1.pickup_location = car_order3.pickup_location 
        WHERE date(initial_time)='{}' or date(pickup_time)='{}'""".format(start_day_str, start_day_str)
        cursor.execute(q)
        res = cursor.fetchall()
        s = sum([x[0] for x in res if x is not None])
        distance += s
        start_day += timedelta(days=1)
    distance /= (b.date() - a.date()).days

    cnt_orders = cursor.execute("SELECT count(*) FROM car_order1").fetchall()[0][0]
    cursor.execute("SELECT julianday(pickup_time) - julianday(initial_time) FROM car_order1")
    res = cursor.fetchall()
    duration += sum([x[0] for x in res if x[0] is not None])
    duration /= cnt_orders
    return str((distance, abs(duration) * 24))


def query6(input_data):
    """In order to accommodate traveling demand, the company decided to distribute cars according
to demand locations. Your task is to compute top-3 most popular pick-up locations and travel
destination for each time of day: morning (7am-10am), afternoon (12am-2pm) and evening
(5pm-7pm)"""
    morning = {"start": "07:00:00", "end": "10:00:00"}
    afternoon = {"start": "12:00:00", "end": "14:00:00"}
    evening = {"start": "17:00:00", "end": "19:00:00"}
    res = [["Morning", [], []],
    ["Afternoon", [], []],
    ["Evening", [], []]]

    res[0][1] = get_3_most_popular_loc("pickup_location", morning)
    res[0][2] = get_3_most_popular_loc("destination_location", morning)

    res[0][1] = get_3_most_popular_loc("pickup_location", afternoon)
    res[0][2] = get_3_most_popular_loc("destination_location", afternoon)

    res[0][1] = get_3_most_popular_loc("pickup_location", evening)
    res[0][2] = get_3_most_popular_loc("destination_location", evening)
    ans = ""
    for i in range(3):
        ans += res[i][0] + "\n" + str(res[i][1]) + "\n" + str(res[i][2]) + "\n\n"

    return ans


def query7(input_data):
    """Despite the wise management, the company is going through hard times and can’t afford
anymore to maintain the current amount of self-driving cars. The management decided to stop
using 10% of all self-driving cars, which take least amount of orders for the last 3 months."""

    end_date = str(datetime.today()).split(" ")[0]
    start_date = str(datetime.today() - timedelta(days=90)).split(" ")[0]
    data = {"start_date": start_date,
            "end_date": end_date}

    q = """SELECT car_id, count(order_id) FROM car_order0
          WHERE '{start_date}' <= date(initial_time) <= '{end_date}'
          GROUP BY car_id ORDER BY count(order_id)
          """.format(**data)

    cursor.execute(q)
    all = cursor.fetchall()
    stop = all[:int(len(all) / 10)]
    res = "Id, \tCount of orders\n" + "\n".join("{}     {}".format(x[0], x[1]) for x in stop)
    return res


def query8(input_data):
    return "test8"


def query9(input_data):
    cursor.execute("SELECT workshop_id,type FROM car_part_instance INNER JOIN car_part_class on car_part_instance.vendor_code=car_part_class.vendor_code")
    result = []
    curs_in = cursor.fetchall()
    for x in set([x[0] for x in curs_in]):
        result.append([f for f in curs_in if f[0] == x])
    part_count = []
    for x in result:
        part_count.append([x[0][0]] + [f[1] for f in x])
    counter = []
    for x in part_count:
        counter.append([x[0]]+[{x[1:].count(f): f for f in set(x[1:])}])
    final_solution = []
    for x in counter:
        final_solution.append([x[0]] + [max(x[1].items(), key=lambda x: x[0])])
    print("test")
    return str(final_solution)


def query10(input_data):
    cursor.execute('''SELECT car.car_id,model,cost,date from car_workshop 
    INNER JOIN car on car_workshop.car_id = car.car_id
''')
    result = []
    curs_in = cursor.fetchall()
    for x in set([x[0] for x in curs_in]):
        result.append([f for f in curs_in if f[0] == x])
    for x in result:
        x.sort(key=lambda x: x[3])

    current_date = datetime.now()
    total_sum = [sum([f[2] for f in x]) for x in result]
    fst_repair = [(current_date.date() - datetime.strptime(x[0][3], "%Y-%m-%d").date()).days for x in result]
    car_type = [x[0][1] for x in result]

    return str(sorted([(x / y, z) for x, y, z in zip(total_sum, fst_repair, car_type)], key=lambda x: x[0], reverse=True)[0])


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

    conn.close()  # closing connection with DB
    return res


if __name__ == "__main__":
    # do_query("Query 1", ["cobalt", "QB"])
    # do_query("Query 2", ["2017-03-03"])
    # do_query("Query 3")
    # do_query("Query 5")
    pass