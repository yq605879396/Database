import pymysql

# login_check
def check_user_pwd(username, password):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()

    if len(username) == 11:
        sql = "SELECT `password` FROM `patient` WHERE `SSN`=%s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result:
            print(result['password'], password)
            return result['password'] == password, 'patient'
    else:
        sql = "SELECT `ppassword`, `pvphone` FROM `provider` WHERE `pvphone`=%s"
        cursor.execute(sql, (username,))
        result = cursor.fetchone()
        if result:
            print(result['ppassword'], password)
            return result['ppassword'] == password, 'provider'

    return False, ""


# add patient 
def add_patient(email, password, pname, SSN, birthdt, pphone, px, py, priority, maxdix = '100', paddress = ''):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            try:
                sql = "INSERT INTO `patient` (`pname`,`SSN`, `birthdt`,`paddress`, `pphone`, `madix`,`px`,`py`,`pemail`, `password`, `priority`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, (pname, SSN, birthdt, paddress, pphone, maxdix, px, py, email, password, str(priority)))
                connection.commit()
                return True
            except Exception as e:
                print("please change")
                print(e)
                connection.rollback()
    return False


# add provider
def add_provider(pvname, ppassword, pvtype, pvaddress, pvphone, pvx, pvy):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record
            try:
                sql = "INSERT INTO `provider` (`pvname`, `ppassword`, `pvtype`, `pvaddress`, `pvphone`, `pvx`, `pvy`) VALUES (%s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql, (pvname, ppassword, pvtype, pvaddress, pvphone, pvx, pvy))
                connection.commit()
                print("Successfully add a new provider")
                return True
            except:
                print("Failed to add a new provider. This phone has already by registered, please change")
                connection.rollback()
    return False


# get patient information 
def get_patient(pid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record\
            try:
                sql = "select `pname`,`pemail`, `SSN`, date(`birthdt`),`paddress`, `pphone`, `madix`,`px`,`py` FROM `patient` WHERE `pid`=%s"
                cursor.execute(sql, (pid, ))
                connection.commit()
                return cursor.fetchone()
            except Exception as e:
                print("Fail to fetch patient information")
                print(e)
                connection.rollback()
    return None


# get provider information 
def get_provider(pvid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record\
            try:
                sql = "select `pvname`, `ppassword`, `pvtype`, `pvaddress`, `pvphone`, `pvx`, `pvy` FROM `provider` WHERE `pvid`=%s"
                cursor.execute(sql, (pvid, ))
                connection.commit()
                print("Successfully fectch provider's basic information")
                return cursor.fetchone()
            except Exception as e:
                print("Fail to fectch provider's basic information")
                print(e)
                connection.rollback()
    return None


# get availability for patient
def get_patient_ava(pid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record\
            try:
                sql = "SELECT `avad`, `avatime` FROM `patientava` WHERE `pid`=%s"
                cursor.execute(sql, (pid, ))
                connection.commit()
                return cursor.fetchall()
            except Exception as e:
                print("Failed to get patient availability")
                print(e)
                connection.rollback()
    return None


# get availability for provider - return past, future
def get_provider_ava(pvid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Create a new record\
            try:
                sql = "SELECT `apid`, date(`date`), date(`offerdt`), `time`, IFNULL(`status`, 'expired') as `status` FROM `appointment` natural left join `book`  WHERE `pvid`=%s and concat(date(`date`),' ', time(`time`))< NOW() ORDER BY `date` DESC"
                cursor.execute(sql, (pvid, ))
                connection.commit()
                past_ava =cursor.fetchall()

                sql = "SELECT `apid`, date(`date`), `time`, `status`, `SSN`, `pname`, date(`offerdt`), date(`replydt`) FROM `appointment` natural left join `book` natural left join `patient` WHERE `pvid`=%s and concat(date(`date`),' ', time(`time`))> NOW() ORDER BY `date`"
                cursor.execute(sql, (pvid, ))
                connection.commit()
                fut_ava =cursor.fetchall()

                print("Successfully fectch provider's appointment list")
                return past_ava, fut_ava

            except Exception as e:
                print("Fail to fectch provider appointment list")
                print(e)
                connection.rollback()
    return None


# get match for patient
def get_patient_app(pid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                sql = "SELECT `pvname`, ROUND(SQRT(power((`px`-`pvx`),2) + power((`py`-`pvy`),2))) as `dist`,`apid`, date(`date`), `time`, `pvphone`, `pvtype`, `pvaddress`, date(`offerdt`), date(`deadlinedt`), `status` FROM `book` natural join `patient` natural join `appointment` natural join `provider` WHERE `pid`=%s ORDER BY `date` DESC"
                cursor.execute(sql, (pid, ))
                connection.commit()
                print("get appoitments successfully")
                return cursor.fetchall()
            except Exception as e:
                print("Failed to get patient appointments")
                print(e)
                connection.rollback()
    return None


# get ava info of provider   
def get_provider_ava_info(pvid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                sql = "SELECT count(*) as ava_num FROM `appointment` WHERE `pvid`=%s"
                cursor.execute(sql, (pvid, ))
                connection.commit()
                ava_num = cursor.fetchone()['ava_num']
                
                sql = "SELECT count(*) as ava_fin FROM `appointment` WHERE `pvid`=%s and concat(date(`date`),' ', time(`time`))< NOW() "
                cursor.execute(sql, (pvid, ))
                connection.commit()
                ava_fin = cursor.fetchone()['ava_fin']
                
                sql = "SELECT count(*) as ava_fin_yes FROM `appointment` natural join `book` WHERE `pvid`=%s and concat(date(`date`),' ', time(`time`))< NOW() and `status` = 'vaccinated' "
                cursor.execute(sql, (pvid, ))
                connection.commit()
                ava_fin_yes = cursor.fetchone()['ava_fin_yes']

                sql = "SELECT count(*) as ava_up FROM `appointment` WHERE `pvid`=%s and  concat(date(`date`),' ', time(`time`)) > NOW() "
                cursor.execute(sql, (pvid, ))
                connection.commit()
                ava_up = cursor.fetchone()['ava_up']
                
                sql = "SELECT count(*) as ava_up_acc FROM `appointment` natural join `book` WHERE `pvid`=%s and concat(date(`date`),' ', time(`time`))> NOW() and `status` = 'accept' "
                cursor.execute(sql, (pvid, ))
                connection.commit()
                ava_up_acc = cursor.fetchone()['ava_up_acc']

                sql = "SELECT count(*) as ava_up_dec FROM `appointment` natural join `book` WHERE `pvid`=%s and  concat(date(`date`),' ', time(`time`))< NOW() > NOW() and `status` = 'decline' "
                cursor.execute(sql, (pvid, ))
                connection.commit()
                ava_up_dec = cursor.fetchone()['ava_up_dec']
                ava_up_pend = str(int(ava_up) - int(ava_up_acc))
                ava_fin_no = str(int(ava_fin) - int(ava_fin_yes))

                print("Successfully fectch provider's summay about appointments.") 
                return ava_num, ava_fin, ava_fin_yes, ava_fin_no, ava_up, ava_up_acc, ava_up_dec, ava_up_pend
            
            except Exception as e:
                print("Failed to fectch provider's summay about appointments.") 
                print(e)
                connection.rollback()
    return None    

# update availability of patient
def update_ava(pid, new_ava):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor = connection.cursor()
                sql = "DELETE FROM `patientava` WHERE `pid`=%s"
                cursor.execute(sql, (pid, ))
                if len(new_ava) > 2:
                    new_ava = new_ava[1:-1]
                    new_ijs = new_ava.split(',')
                    for new_ij in new_ijs:
                        i = new_ij[1]
                        j = new_ij[2]
                        i = str(int(i) + 1)
                        j = str(int(j) + 1)
                        sql = "INSERT INTO `patientava` (`pid`,`avad`, `avatime`) VALUES (%s, %s, %s);"
                        cursor.execute(sql, (pid, j, i))
                connection.commit()
                print("Successfully update availability for patient.")
                return True
            except Exception as e:
                print("Failed to update availability for patient.")
                print(e)
                connection.rollback()
                return False

# update patient basic information
def update_patient_basic(pid, maxdis, paddress, px, py):      
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor = connection.cursor()
                if maxdis:
                    print(maxdis)
                    sql = "UPDATE `patient` SET `madix`= %s WHERE `pid`=%s"
                    cursor.execute(sql, (maxdis, pid))
                    connection.commit()
                if paddress:
                    sql = "UPDATE `patient` SET `paddress`= %s WHERE `pid`=%s"
                    cursor.execute(sql, (paddress, pid))
                    connection.commit()
                
                if px:
                    sql = "UPDATE `patient` SET `px`= %s WHERE `pid`=%s"
                    cursor.execute(sql, (px, pid))
                    connection.commit()
                if py:
                    print("hihi")
                    sql = "UPDATE `patient` SET `py`= %s WHERE `pid`=%s"
                    cursor.execute(sql, (py, pid))
                    connection.commit()
                print("Successfully update appointment status for patient.")
                return True
            except Exception as e:
                print("Failed to update appointment status for patient.")
                print(e)
                connection.rollback()
                return False


# add appointment from provider
def add_provider_ava(pvid, date, time):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor = connection.cursor()
                sql =  "INSERT INTO `appointment` (`pvid`,`date`, `time`) VALUES (%s, %s, %s);"
                cursor.execute(sql, (pvid, date, time ))
                connection.commit()
                print("Successfully add an appointment for provider.")
                return True
            except Exception as e:
                print("Fail to add an appointment for provider.")
                print(e)
                connection.rollback()
                return False


# patient - changing matching status
def dec_or_acc_match(pid, apid, action):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                cursor = connection.cursor()
                sql1 = "UPDATE `book` SET `status`= %s WHERE `pid`=%s and `apid` = %s;"
                if action == 'cancel':
                    action = 'decline'
                cursor.execute(sql1, (action, pid, apid ))
                connection.commit()
                print("Successfully update appointment status for patient.")
                return True
            except Exception as e:
                print("Failed to update appointment status for patient.")
                print(e)
                connection.rollback()
                return False
            

def SSN_2_pid(SSN):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                sql = "SELECT `pid` FROM `patient` WHERE `SSN`=%s;"
                cursor.execute(sql, (SSN, ))
                connection.commit()
                pid = cursor.fetchone()['pid']
                return pid
            except Exception as e:
                print("Invaid SSN - not such record")
                print(e)
                connection.rollback()
                return False


def phone_2_pvid(pvphone):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='774109yq',
                                 database='vaccine',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            try:
                sql = "SELECT `pvid` FROM `provider` WHERE `pvphone`=%s;"
                cursor.execute(sql, (pvphone, ))
                connection.commit()
                pvid = cursor.fetchone()['pvid']
                return pvid
            except Exception as e:
                print("Invaid provider phone - not such record")
                print(e)
                connection.rollback()
                return False
