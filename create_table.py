#!/usr/bin/env python

from db_conn import *
import pymssql

conn = pymssql.connect(SERVER, USER, PASSWORD, "CCZ_BatchMaster")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE rejproinhis (
    id INT NOT NULL,
    dbname VARCHAR(100),
    recdate DATETIME,
    qty DECIMAL(22,6),
    PRIMARY KEY(id)
)
""")

conn.commit()
conn.close()