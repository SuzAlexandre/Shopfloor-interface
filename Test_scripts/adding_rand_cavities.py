import sys
import pyodbc
import numpy



def get_SO_list(conn):
    cursor = conn.cursor()

    cursor.execute('select SO_number from SO_numbers_list')
    SO_list=[]

    for row in cursor:
        SO_list.append(row[0])
    
    for row in SO_list:
        # generate a few cavity number per row and execute
       cav_start=numpy.random.randint(1,50)
       cav_number=numpy.random.randint(2,6)

       for cav in range(cav_start,cav_number+cav_start,1):   
            cursor.execute('insert into casting_cavities_list (SO_number, cavity_number) values(?,?)',row, cav)
    conn.commit()


conn = pyodbc.connect(
"Driver={SQL Server Native Client 11.0};"
"Server=10.41.32.4;"
"Database=SZ_001;"
"Trusted_Connection=yes;")


get_SO_list(conn)