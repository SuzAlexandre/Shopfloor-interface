import sys
import pyodbc
import numpy


def generate_scrap_codes(conn):
    cursor = conn.cursor()

    for row in range(2,50):
       scrap_code=str(row)
       scrap_description_EN = "EN description of scrap - " + scrap_code
       scrap_description_CN = "CN description of scrap - " + scrap_code
       cursor.execute('insert into scrap_code_list (scrap_code, scrap_description_EN, scrap_description_CN) values (?,?,?)', scrap_code, scrap_description_EN, scrap_description_CN)
       
    conn.commit()

conn = pyodbc.connect(
"Driver={SQL Server Native Client 11.0};"
"Server=10.41.32.4;"
"Database=SZ_001;"
"Trusted_Connection=yes;")

generate_scrap_codes(conn)