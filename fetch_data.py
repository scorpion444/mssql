#!/usr/bin/env python

from db_conn import *
import pymssql
from time import localtime

conn = pymssql.connect(SERVER, USER, PASSWORD, "CCZ_BatchMaster")
cursor = conn.cursor()

# Define the date range and database name
year = localtime().tm_year
month = localtime().tm_mon
day = localtime().tm_mday
date = str(year)+'-'+('%02d' % month)+'-'+('%02d' % day)
dbname = 'CCZ_BatchMaster'

cursor.execute('select sum(qtyonhand) from INLOC where Location=%s and Qtyonhand<>0' % 'WKOFF')
row = cursor.fetchone()

qty = row[0]

conn.commit()
conn.close()