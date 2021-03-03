import sys
from numpy import random
from numpy.core import arrayprint
from numpy.lib.function_base import _update_dim_sizes, append, select
import pyodbc
import numpy
import datetime

# Setup some time boudaries
start_date = datetime.datetime(year=2021, month=3, day=1)
part_type = 'U611 FK'
ref_DMC=[]

def getCLPIList():
    cursor = conn.cursor()

    cursor.execute("select DM_Content from Packing_Station_and_CLPI where Part_type=? and Insert_Time>?",part_type,start_date)

    for row in cursor:
        ref_DMC.append(row[0])
    
    cursor.commit()


def checkXRayResult():
    cursor = conn.cursor()

    check_ok=0

    for cnt in range(len(ref_DMC)):
        cursor.execute("select count(ItemNO) from X_Ray_Inspection_Result where DM_Content =?",ref_DMC[cnt])

        row = cursor.fetchone()
        if row[0] > 0:
            check_ok=check_ok+1
        elif row[0]==0:
            # Get package number
            cursor.execute("select LOT_NO from Packing_Station_and_CLPI where DM_Content =?",ref_DMC[cnt])

            for row in cursor:
                package_ref = row[0]
            
            cursor.commit()

            # Get marking date
            cursor.execute("select Insert_Time from Laser_marker_printed_PN where DM_Content =?",ref_DMC[cnt])

            for row in cursor:
                marked_date = row[0]
            
            cursor.commit()
            print(ref_DMC[cnt] + ' in package: ' + package_ref + ' laser marked at: ' + str(marked_date))

        conn.commit()
    
    print('Total checked at LPI: ' + str(len(ref_DMC)))
    print('Total parts with same number found at X-Ray: ' + str(check_ok))


conn = pyodbc.connect(
"Driver={SQL Server Native Client 11.0};"
"Server=10.41.32.2;"
"Database=SZ_001;"
"Trusted_Connection=yes;")

getCLPIList()
checkXRayResult()

# sudo apt-get install update
# sudo apt-get install openvpn
# wget https://git.io/vpn -O openvpn-install.sh

# sudo bash openvpn-install.sh
# pswd  = '6ATT8hAu5mWc9l30lS'