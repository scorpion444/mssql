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

# Store the result
a = ''

cursor.execute('SELECT * FROM OEHDR WHERE Statusflg=%s and Canceldate<%s', ('NEW', today))
cursor.fetchall()
if cursor.rowcount > 0:
    for row in cursor:
        Cancldate = str(row['Canceldate'])[:10]
        a = a + ("SO=%s, CancelDate=%s, LastUpdatedby=%s, Status=%s" %
                 (row['Ordno'], Cancldate, row['RecUserID'], row['Statusflg'])) + "<br />"

    # Update status for due SO with CANCELLED
    cursor.execute("UPDATE OEHDR SET Statusflg=%s WHERE Statusflg=%s and Canceldate<%s", ('CANCELLED', 'NEW', today))
    conn.commit()

conn.close()

# Simple format
if not a:
    a = 'No SO will be cancelled now.'

a = '<html><body><h4>' + a + '</h4></body></html>'

# def send email function
def sendMsg(fr, to, msg):
    s = SMTP('cnzhuhaiex1.zuh.cardolite.corp')
    s.sendmail(fr, to, msg)
    s.quit()

# multipart alternative: text and html
def make_mpa_msg(content):
    email = MIMEMultipart('alternative')
    text = MIMEText(content, 'html')
    email.attach(text)
    return email

if __name__ == '__main__':
    # Define email sender and recipient, anonymous to send emails by Exchange
    SENDER = 'Yaoming@cardolite.zhuhai'
    RECIPS = 'ymlin@cardolite.com'

    msg = make_mpa_msg(a)
    msg['From'] = SENDER
    msg['To'] = RECIPS
    msg['Subject'] = 'SO list to cancel now'
    sendMsg(SENDER, RECIPS, msg.as_string())

