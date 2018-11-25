import task_list
import sqlite3
import os

DB_PATH =  os.getcwd()[:-5] + "courseDB/courseDB"

# Each queryN method returns string output without separators and stuff

def query1():
    cursor.execute("SELECT * FROM Customer")
    res = cursor.fetchall() # getting results
    res = "\n".join([str(x) for x in res])
    
    return res

def query2():
    return "test2"

def do_query(query_name, input_data=None):
    global cursor
    
    print(query_name, "|", task_list.task[query_name]) # Prints query in human language
    
    conn = sqlite3.connect(DB_PATH) # connection to DB
    cursor = conn.cursor() # object that does queries and return their result
    
    query_num = query_name.split()[-1] # Gets numerical identifier of query (from 1 to 10)
    args = ["input_data", ""][input_data is None] # Prepares argument
    funct = "query" + query_num + "(" + args + ")" # Prepares function
    res = eval(funct) # Evaluates function    
    
    print(res)
    print()
    
    conn.close() # closing connection with DB
    return res

<<<<<<< HEAD

def do_query(query_name):
    print(task_list.task[query_name])
||||||| merged common ancestors
def do_query(query_name):
    print(task_list.task[query_name])
=======
>>>>>>> 781f4fff8b9110499c8a6c2bbfdbda5cef55b1f1

<<<<<<< HEAD
# return string output without separators and stuff
||||||| merged common ancestors
# return string output without separators and stuff
=======
do_query("Query 1 ")
>>>>>>> 781f4fff8b9110499c8a6c2bbfdbda5cef55b1f1
