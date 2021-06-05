# 1. check book status - update
# 2. add new match to book list
#   get patient
#   get appointment
#   get edge - weight is the distance
import collections
import heapq
import pymysql
from datetime import datetime
from threading import Timer
import time

def db_check_status():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                # check those no reply after deadline
                sql = "UPDATE `book` set `status` = 'vaccinated' where `deadlinedt` < now() and status = 'accept';"
                cursor.execute(sql)
                connection.commit()
                # check those appointments that already happened
                sql = "UPDATE `book` set `status` = 'vaccinated' where `status` = 'accept' and `apid` in (select apid from appointment where date < now());"
                cursor.execute(sql)
                connection.commit()
                return True
            except Exception as e:
                print("Fail to update status")
                print(e)
                connection.rollback()
    return False
    
def get_app_patient():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                # check those no reply after deadline
                sql = "select `px`, `py`, `madix`, `priority`,`pid` from `patient` natural join `waiting_patients`" 
                cursor.execute(sql)
                connection.commit()
                patients = cursor.fetchall()
                # check those appointments that already happened
                sql = "select `pvx`, `pvy`, `apid` from `provider` natural join `appointment` natural join `available_app`;"
                cursor.execute(sql)
                connection.commit()
                appointments = cursor.fetchall()
                return appointments, patients
            except Exception as e:
                print("Failed to get need patient or appointments")
                print(e)
                connection.rollback()
    return False

def matching(providers, patients):
    A_node = set()
    B_node = set()
    heap = []
    for provider in providers:
        apid, pvx, pvy = provider['apid'], provider['pvx'], provider['pvy']
        A_node.add(apid)
        for patient in patients:
            pid, px, py, maxd, priority = patient['pid'], patient['px'], patient['py'], patient['madix'], patient['priority']
            if pid not in B_node:
                B_node.add(pid)
                dist = pow(px-pvx,2) + pow(py-pvy, 2)
                if dist < maxd**2:
                    heapq.heappush(heap,(priority, -dist, apid, pid))
    result = []
    seen_A = set()
    seen_B = set()
    while heap and len(seen_A) < len(A_node) and len(seen_B) < len(B_node):
        _, _, sel_apid, sel_pid = heapq.heappop(heap)
        if sel_apid not in seen_A and sel_pid not in seen_B:
            result.append([sel_apid, sel_pid])
            seen_A.add(sel_apid)
            seen_B.add(sel_pid)
    return result

def db_add_match(result):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                for apid, pid in result:
                    sql = "INSERT INTO `book` ( `apid`, `pid`, `offerdt`, `deadlinedt`) VALUES (%s, %s, curdate(), curdate() + interval 3 day)" 
                    cursor.execute(sql, (apid, pid))
                    connection.commit()
                return True
            except Exception as e:
                print("Something wrong while adding matches")
                print(e)
                connection.rollback()
    return False


def task():
    print("working.....")
    db_check_status()
    providers, patients = get_app_patient()
    print(providers, patients)
    res = matching(providers, patients)
    print(res)
    db_add_match(res)

if __name__ == '__main__':
    while True:
        time.sleep(10)
        task()
