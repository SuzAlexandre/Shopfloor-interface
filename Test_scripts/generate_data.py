import sys
from numpy import random
from numpy.core import arrayprint
from numpy.lib.function_base import _update_dim_sizes, append
import pyodbc
import numpy
import datetime

# Setup some time boudaries
start_date = datetime.datetime(year=2020, month=1, day=16)
end_date = datetime.datetime(year=2021, month=1, day=20)
crucible_stations_list=['A1','A2','A3','B1','B2','B3','C1','C2']
delta_time=(end_date-start_date).total_seconds()

# generate some crucible ID
def genCrucibles():
    cursor = conn.cursor()
    
    # generate crucible ids
    crucibleIds=numpy.arange(1,100)

    for val in crucibleIds:
      cursor.execute('insert into crucible_list (crucible_ID) values(?)',int(val))   
    conn.commit()


# step 1 generate metal batch
def genBatchIDs():
    cursor = conn.cursor()
    
    res=[]

    # Count 1 year production, so about 10 000 crucibles
    for cnt in range(1,10000):
        crucibleId=random.choice(numpy.arange(1,100))
        station = random.choice(crucible_stations_list)
        
        # generate test and used times
        test_time=start_date+datetime.timedelta(seconds=numpy.random.choice(numpy.arange(1,delta_time)))
        used_time=test_time+datetime.timedelta(minutes=int(numpy.random.choice(numpy.arange(1,60*4))))
        # let's say batch ID is made of  line ,station, julian date, and a counter, but to make it super simple, let's just put a counter
        batch_name = str(station) + '{:03d}'.format(crucibleId) + '{:05d}'.format(cnt)
        res.append([batch_name,int(crucibleId),test_time,used_time])
    
    cursor.executemany('insert into metal_batch (metal_batch_ID, crucible_ID, insert_time, used_time) values (?,?,?,?)',res)
    conn.commit()
    
    # for val in crucibleId:
    #   cursor.execute('insert into crucible_list (crucible_ID) values(?)',int(val))   
    # conn.commit()

def genShotList():
    cursor = conn.cursor()

    caster_list=[]
    metal_batch_list=[]

    # get list of caster
    cursor.execute('select caster_ID from caster_list')

    # save that in cursor list
    for row in cursor:
        caster_list.append(row[0])
    
    cursor.commit()

    # get list of batch
    cursor.execute('select metal_batch_ID from metal_batch')

    # save that in cursor list
    for row in cursor:
        metal_batch_list.append(row[0])
    
    cursor.commit()

    #create a total of:
        # 16 casters
        # 10 shots per hours per caster, non stop for 350 days

    nb_shot = int(16*10*24)
    cursor.fast_executemany=True

    metal_batch_range=range(1,len(metal_batch_list))

    nb_days = 10
    for days in range(1,nb_days):
        res=[]
        print("Starting day " + str(days) + " of " + str(nb_days) + " with " + str(nb_shot) + " shots planned")
        for i in range(nb_shot):
            shot_time = start_date+datetime.timedelta(seconds=numpy.random.choice(numpy.arange(1,delta_time)))
            caster_ID = random.choice(caster_list)
            metal_batch = metal_batch_list[int(random.choice(metal_batch_range))]
            
            res.append([shot_time,int(caster_ID),metal_batch])
        
        print("Writing in database...")
        cursor.executemany('insert into shot_list (shot_time, caster_ID, metal_batch_ID) values (?,?,?)',res)
        conn.commit()

        print('Completed day' + str(days))

def reviewCounts():
    cursor = conn.cursor()
    
    table_list = ['part_serial_numbers', 'parts_serial_number_shot_list', 'xray_scan', 'HT_batch_parts_list','machining_scan','assembly_scan']
    table_list_name = ['Serial numbers', 'Shot list', 'X ray', 'HT batch', 'Machining scan', 'Assembly scan']

    for table in table_list:
        query = 'select count(serial_number) from ' + table 
        cursor.execute(query)

        row = cursor.fetchone()
        print(row[0])
        conn.commit()

def testFunc():
    for i in range(1,120,10):
        print('{:03d}'.format(i))
# generate HT batch ID

conn = pyodbc.connect(
"Driver={SQL Server Native Client 11.0};"
"Server=10.41.32.4;"
"Database=SZ_001;"
"Trusted_Connection=yes;")

# genCrucibles()
genShotList()

# sudo apt-get install update
# sudo apt-get install openvpn
# wget https://git.io/vpn -O openvpn-install.sh

# sudo bash openvpn-install.sh
# pswd  = '6ATT8hAu5mWc9l30lS'