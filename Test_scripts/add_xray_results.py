import sys
from PyQt5.QtWidgets import QMessageBox
from numpy import random
import pyodbc
import numpy
import datetime
from PyQt5.QtGui import *

def genXRayResults(conn):
    cursor = conn.cursor()
    cursor.execute('select xray_ID from xray_list')
    
    # initialize XRay list
    XRayList=[]

    for row in cursor:
        XRayList.append(row[0])
    conn.commit()

    # read all serial numbers fom  part serial numbers
    SN_list=[]
    XRayTime=[]
    XRayResults=[]
    XRayIDs=[]
    res=[]

    cursor.execute('select serial_number, register_time from part_serial_numbers')

    for row in cursor:
        SN_list.append(row[0])
        timeref = row[1]
        scanTime = timeref + datetime.timedelta(seconds= float(numpy.random.choice(numpy.arange(1,60))), minutes= float(numpy.random.choice(numpy.arange(1,5))))
        XRayTime.append(scanTime)
        XRayResults.append(numpy.random.choice([0,1],p=[0.1, 0.9]))
        XRayIDs.append(random.choice(XRayList))
        new_row = [row[0],random.choice(XRayList),scanTime,int(numpy.random.choice([0,1],p=[0.1, 0.9]))]
        res.append(new_row)
        

    conn.commit()
    print('Done reading, start writing...')
    total = len(SN_list)
    cnt_ref=0
    ref=42690

    # cursor.executemany('insert into xray_scan (serial_number, xray_ID, scan_time, xray_result) values (?,?,?,?)',SN_list[cnt_ref:total],XRayIDs[cnt_ref:total],XRayTime[cnt_ref:total],XRayResults[cnt_ref:total])
    
    cursor.executemany('insert into xray_scan (serial_number, xray_ID, scan_time, xray_result) values (?,?,?,?)',res[ref:total])
    conn.commit()

    # for cnt in range(33811,len(SN_list)):
    #     XRayID = random.choice(XRayList)
    #     XRayResult = int(numpy.random.choice([0,1],p=[0.1, 0.9]))
    #     cursor.execute('insert into xray_scan (serial_number, xray_ID, scan_time, xray_result) values (?,?,?,?)',SN_list[cnt],XRayID,XRayTime[cnt],XRayResult)
    #     conn.commit()

    #     if cnt > cnt_ref+5000:
    #         cnt_ref=cnt
    #         progress=cnt/total*100
    #         progress=int(progress)
    #         print(str(progress) + '%')


conn = pyodbc.connect(
"Driver={SQL Server Native Client 11.0};"
"Server=10.41.32.4;"
"Database=SZ_001;"
"Trusted_Connection=yes;")

genXRayResults(conn)