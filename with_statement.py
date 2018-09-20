#!/usr/bin/env python

from db_conn import *
import pymssql

with pymssql.connect(SERVER, USER, PASSWORD, "tempdb") as conn:
    with conn.cursor(as_dict=True) as cursor:
        cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
        for row in cursor:
            print("ID=%d, Name=%s" % (row['id'], row['name']))