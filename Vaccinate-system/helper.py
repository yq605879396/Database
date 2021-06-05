import re
import time
import datetime
def check_email(input_str):
    p=re.compile('[^\._-][\w\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$|^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    if p.match(input_str) != None:
        return True
    else:
        return False

def check_SSN(input_str):
    chunks = input_str.split('-')
    p=re.compile('^[0-9]*$')
    if len(chunks) ==3 and len(chunks[0])==3 and len(chunks[1])==2 and len(chunks[2])==4 and p.match(chunks[0]) != None and p.match(chunks[1]) != None and p.match(chunks[2]) != None:
        return True
    else:
        return False

# should be all number
def check_phone(input_str):
    chunks = input_str.split('-')
    p=re.compile('^[0-9]*$')
    if len(chunks) ==3 and len(chunks[0])==3 and len(chunks[1])==3 and len(chunks[2])==4 and p.match(chunks[0]) != None and p.match(chunks[1]) != None and p.match(chunks[2]) != None:
        return True
    else:
        return False


# should YYYY-MM-DD 1900- 2022, 1-12, 1-31 
def check_date(input_str):
    chunks = input_str.split('-')
    p=re.compile('^[0-9]*$')
    if len(chunks) == 3 and len(chunks[0]) == 4 and 1 <= len(chunks[1]) <= 2 and 1<= len(chunks[2]) <= 2 and p.match(chunks[0]) != None and p.match(chunks[1]) != None and p.match(chunks[2]) != None \
        and 1900 < int(chunks[0]) < 2023 and 0 < int(chunks[1]) < 13 and -1 < int(chunks[2]) < 32: 
        return True
    else:
        return False

# should HH:MM AM/PM
def check_time(input_str):
    chunks = input_str.split(' ')
    p=re.compile('^[0-9]*$')
    if len(chunks) !=2 or ":" not in chunks[0]:
        return False
    else:
        hh, mm = chunks[0].split(':')
        if len(hh) > 2 or len(mm) > 2 or len(hh) < 1 or len(mm) < 1 or (chunks[1]!="AM" and chunks[1]!= "PM"):
            return False
        if 0 < int(hh) < 13 and -1 < int(mm) < 61:
            return True
        return False

def later_then_current(date, time):
    cur_date = datetime.date.today()
    date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if date > cur_date:
        return True
    elif date < cur_date:
        return False
    else:
        cur_time = datetime.datetime.now().__format__('%I:%M %p')
        time = datetime.datetime.strptime(time, "%I:%M %p").strftime("%I:%M %p")
        return time > cur_time

def get_group(birthday):
    birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d").date()
    age = datetime.date.today() - birthday
    age = int(age.days)//365.25
    if age >= 80:
        return 1
    elif age >= 60:
        return 2
    elif age >= 40:
        return 3
    elif age >= 30:
        return 4
    elif age >= 20:
        return 5
    elif age >= 10:
        return 6
    else:
        return 7

def check_expire(date):
    #date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if date < datetime.date.today():
        return True
    return False