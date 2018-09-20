#!/usr/bin/env python

from db_conn import *
import pymssql

with pymssql.connect(SERVER, USER, PASSWORD, "tempdb") as conn:
    with conn.cursor(as_dict=True) as cursor:
        cursor.execute("""
        CREATE PROCEDURE FindPerson
            @name VARCHAR(100)
        AS BEGIN
            SELECT * FROM persons WHERE name = @name
        END
        """)
        cursor.callproc('FindPerson', ('Jane Doe',))
        for row in cursor:
            print("ID=%d, Name=%s" % (row['id'], row['name']))