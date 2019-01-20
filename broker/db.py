import sqlite3
import uuid
import base64
import datetime


def get_a_uuid():
    """

    @return: returns a uuid

    This functions returns a unique uuid that can be used as indexing values.
    """
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return str(r_uuid.decode('utf-8')).replace('=','')


def create_command_line(args):
    """

    @param args:list of arguments
    @return: the field names and values

    This function will take an arbitrary list of field naes and values and properly create a string that is used to
    insert the data into the database.
    """

    numparamsleft = len(args)
    fieldnames = ""
    values = ""

    # For each key, value in the arguments, process each
    for key,value in args.items():
        fieldnames = fieldnames+key
        values = values+"'"+value+"'"
        numparamsleft = numparamsleft-1
        if numparamsleft >= 1:
            fieldnames = fieldnames+","
            values = values+','

    return fieldnames,values


def initialize_database(dbname):
    """

    @param dbname: name of the database
    @return: nothing

    This function will initialize a new database using the name specified in the paramter.   When completed, this
    function will also close the database connection.
    """
    print("Initializing the database: "+dbname)

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
                                        guestpassword text NULL,
                                        teamsroomid text NULL,
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
    return conn


def insert_into_database(dbname,table,**kwargs):
    """

    @param dbname: name of the database
    @param table: table that we want to insert the record into it
    @param kwargs: variable number of arguments that represents the values we want to insert.
    @return: the uuid of the new record that is inserted.
    """
    conn = sqlite3.connect(dbname)

    #generate a unique ID
    id=get_a_uuid()
    #generate the current date for timestamps
    d=datetime.datetime.now()

    fieldnames,values = create_command_line(kwargs)

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
    """

    @param dbname: name of the database
    @param table: table to be used for the search
    @return: the data that was retrieved

    This function just performs a very simple select all from the table and returns the data
    """
    conn = sqlite3.connect(dbname)
    conn.row_factory = sqlite3.Row
    curs = conn.cursor()

    select="SELECT * FROM "+table

    curs.execute(select)

    data=curs.fetchall()

    return data

def update_database(dbname,table,field,condition):
    """

    @param dbname: name of the database
    @param table: table used to update
    @param field: field to update
    @param condition: the condition used to determine which record to update
    @return:

    This function will update a record in a database based upon the field and condition
    """

    conn = sqlite3.connect(dbname)

    update_command = "UPDATE "+table+" SET "+field+" WHERE "+condition

    print(update_command)
    try:
        conn.execute(update_command)
        conn.commit()
    except (sqlite3.Error) as e:
        print(e)
        return(False,str(e))
    conn.close()
    return(True,id)


def delete_database(dbname,table,condition):
    """

    @param dbname: name of the database
    @param table: table to delete
    @param condition: condition to determine which record to delete
    @return:

    Deletes a row from a table which matches the condition
    """

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
    """

    @param dbname: name of the database
    @param table: table to search
    @param field: field that we are using to search
    @param value: value that we want to search for
    @return: True or False if the command was executed correctly and if True, then return the data
    """
    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    select="SELECT * FROM "+table+ " WHERE "+field+"='"+value+"'"
    print(select)
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
            final[i]=data[0][count]

            count = count + 1

        return (True,final)
