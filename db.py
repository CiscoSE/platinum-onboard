import sqlite3
import uuid
import base64
import datetime

def get_a_uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    print(r_uuid)
    return str(r_uuid.decode('utf-8')).replace('=','')


def create_command_line (args):

    numparamsleft=len(args)
    fieldnames=""
    values=""

    for key,value in args.items():
        fieldnames=fieldnames+key
        values=values+"'"+value+"'"
        numparamsleft=numparamsleft-1
        if numparamsleft>=1:
            fieldnames=fieldnames+","
            values=values+','

    return fieldnames,values


def initialize_database(dbname):
    print ("Initializing the database: "+dbname)

    try:
        conn = sqlite3.connect(dbname)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print("Error: "+e)
        return(False)

    sql_create_domains_table = """ CREATE TABLE IF NOT EXISTS domain (
                                        id text PRIMARY KEY,
                                        name text NOT NULL UNIQUE,
                                        date text NOT NULL
                                    ); """

    sql_create_device_table = """CREATE TABLE IF NOT EXISTS device (
                                    id text PRIMARY KEY,
                                    name text NOT NULL UNIQUE,
                                    date text NOT NULL
                                );"""

    sql_create_guest_table = """CREATE TABLE IF NOT EXISTS guest (
                                        id text PRIMARY KEY,
                                        name text NOT NULL,
                                        device text NOT NULL,
                                        date text NOT NULL,
                                        status text NOT NULL
                                    );"""

    try:
        conn.execute(sql_create_domains_table)
        conn.execute(sql_create_device_table)
        conn.execute(sql_create_guest_table)
    except sqlite3.Error as e:
        print("Error: "+e)
        return(False)
    conn.commit()
    conn.close()
    return (conn)

def insert_into_database(dbname,table,**kwargs):
    conn = sqlite3.connect(dbname)

    #generate a unique ID
    id=get_a_uuid()
    #generate the current date for timestamps
    d=datetime.datetime.now()

    print(kwargs)

    fieldnames,values = create_command_line(kwargs)

    print (fieldnames)
    print (values)

    insert="INSERT INTO "+table+" (ID,DATE,"+fieldnames+") VALUES ('"+id+"','"+str(d)+"',"+values+")"

    print(insert)

    try:
        conn.execute(insert)
        conn.commit()
    except (sqlite3.Error) as e:
        print(e)
        return(False,str(e))
    conn.close()
    return(True,id)

def search_db(dbname,table):
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()

    select="SELECT * FROM "+table

    curs.execute(select)

    data=curs.fetchall()

    return data

def update_database(dbname,table,field,condition):

    conn = sqlite3.connect(dbname)

    update_command = "UPDATE "+table+" SET "+field+" WHERE "+condition

    try:
        conn.execute(update_command)
        conn.commit()
    except (sqlite3.Error) as e:
        print(e)
        return(False,str(e))
    conn.close()
    return(True,id)


def delete_database(dbname,table,condition):

    delete_command = "DELETE FROM "+table
    if condition != "":
        delete_command += " WHERE "+condition

    delete_command +=";"

    print(delete_command)

    conn = sqlite3.connect(dbname)

    try:
        conn.execute(delete_command)
        conn.commit()
    except (sqlite3.Error) as e:
        print(e)
        return(False,str(e))
    conn.close()
    return(True,id)

def search_database(dbname,table,field,value):
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    select="SELECT * FROM "+table+ " WHERE "+field+"='"+value+"'"

    curs.execute(select)
    names = list(map(lambda x: x[0], curs.description))

    data=curs.fetchall()

    final={}
    num_rows_fetched = len(data)

    if num_rows_fetched<1:
        return(False,final)
    else:
        count=0
        for i in names:
            print(i+" "+data[0][count])
            final[i]=data[0][count]

            count = count + 1

        return (True,final)