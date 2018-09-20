#!/usr/bin/env python

from db_conn import *
import pymssql

conn = pymssql.connect(SERVER, USER, PASSWORD, "tempdb")
cursor = conn.cursor()
cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')

for row in cursor:
    print('row = %r' % (row,))

conn.close()