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
begindate = str(year)+'-'+('%02d' % (month+1))+'-'+('%02d' % 1)
enddate = str(year)+'-'+('%02d' % (month+2))+'-'+('%02d' % 1)

#Store the result
a = ''

cursor.execute('SELECT * FROM POHDR WHERE statusflg=%s or statusflg=%s', ('NEW', 'OPEN'))
for row in cursor:
    Cancldate = str(row['Cancldate'])[:10]
    if Cancldate >= begindate and Cancldate < enddate:
        a = a + ("PO=%s, CancelDate=%s, LastUpdatedby=%s, Status=%s" %
                       (row['Pono'], Cancldate, row['RecUserID'], row['Statusflg'])) + '<br />'

conn.close()

# Simple format
if not a:
    a = 'No PO will be cancelled next month.'

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
    RECIPS = 'PurchaseZhuhai@cardolite.com'

    msg = make_mpa_msg(a)
    msg['From'] = SENDER
    msg['To'] = RECIPS
    msg['Subject'] = 'PO to cancel next month'
    sendMsg(SENDER, RECIPS, msg.as_string())

