#!/usr/bin/env python

from db_conn import *
import pymssql
from time import localtime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

conn = pymssql.connect(SERVER, USER, PASSWORD, "CCZ_Batchmaster")
cursor = conn.cursor(as_dict=True)

# Define the date range
year = localtime().tm_year
month = localtime().tm_mon
day = localtime().tm_mday
today = str(year)+'-'+('%02d' % month)+'-'+('%02d' % day)+' 00:00:00.000'
#begindate = str(year)+'-'+('%02d' % (month+1))+'-'+('%02d' % 1)
#enddate = str(year)+'-'+('%02d' % (month+2))+'-'+('%02d' % 1)

# Store the result
a = ''

cursor.execute('SELECT * FROM OEHDR WHERE Statusflg=%s and Canceldate<%s', ('NEW', today))
cursor.fetchall()
print cursor.rowcount