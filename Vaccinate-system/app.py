from flask import Flask,render_template, flash
from flask import redirect
from flask import url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
import database_func as db_f
from encrypt import *
from helper import *
from datetime import timedelta

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SECRET_KEY'] = "123asdQi0231-829!)!'["

@app.route('/')
def index():
    return redirect( url_for('user_login') )

@app.route('/user_login', methods=['GET','POST'])
def user_login():
    if request.method=='POST':  # 
        username = request.form['usn']
        password = request.form['pwd']
        if not check_phone(username) and not check_SSN(username):
            flash('Please input valid username')
        else:
            correct, acc_type = db_f.check_user_pwd(username, password)
            if correct:
                if acc_type == 'patient':
                    return redirect(url_for('patient_main', username = des_encrypt(secret_key, username)))
                else:
                    return redirect(url_for('provider_main', username = des_encrypt(secret_key, username)))
            else:
                login_massage = "Login Failed"
                flash('Wrong username or password')
                return render_template('login.html', message=login_massage)
    return render_template('login.html')


@app.route('/patient_main/<username>', methods=['GET','POST'])
def patient_main(username):
    url = username
    SSN = des_decrypt(secret_key, username)
    pid = db_f.SSN_2_pid(SSN)
    if request.method == 'GET':
        if request.args:
            if request.args.get('mode') == 'availability':
                new_ava = request.args.get('new_ava')
                if db_f.update_ava(pid, new_ava):
                    print("YAY!! update availability for patient successfully!")
                else:
                    print("Whooops! fail to update availability for patient")

            elif request.args.get('mode') == 'match':
                if db_f.dec_or_acc_match(pid, request.args.get('apid'), request.args.get('action')):
                    print("YAY!!! update match status successfully")
                else:
                    print("Whooops! failed to update appointment status for patient")

    elif request.method == 'POST':
        new_dis = request.form['new_maxdict']
        new_address = request.form['new_address']
        new_px = request.form['new_px']
        new_py = request.form['new_py']
        print(pid, new_dis, new_address, new_px, new_py)
        db_f.update_patient_basic(pid, new_dis, new_address, new_px, new_py)
  
    patient_data = db_f.get_patient(pid)
    patient_ava = db_f.get_patient_ava(pid)
    patient_app = db_f.get_patient_app(pid)
    ava = [[0]*7 for _ in range(6)]
    if patient_ava:
        for record in patient_ava:
            ava[record['avatime']-1][record['avad']-1] = 1
    patient_data['ava'] = ava
    patient_data['app'] = patient_app
    patient_data['url'] = url
    for match in patient_app:
        if check_expire(match['date(`deadlinedt`)']):
            match['show'] = 'No'
        else:
            match['show'] = 'Yes'
    return render_template('patient_main.html', patient_data = patient_data)


@app.route('/provider_main/<username>', methods=['GET','POST'])
def provider_main(username):
    url = username
    pvphone = des_decrypt(secret_key, username)
    pvid = db_f.phone_2_pvid(pvphone)
    print("Current pvid is:", pvid)

    if request.method == 'POST':
        date = request.form['new_date']
        time = request.form['new_time']
        print("Parames from front end(form): ", date, time)
        if not check_date(date): 
            flash('Invalid input - please make sure date format is correct.')
        elif not later_then_current(date, time):
            flash("Invalid input - time shouldn't in the past.")
        elif not check_time(time):
            flash('Invalid input - please make sure time format is correct.')
        else:
            if db_f.add_provider_ava(pvid, date, time):
                flash('Yay, added successfully') 
            else:
                flash('Whoops, something wrong when dealing with database')

    provider_data = db_f.get_provider(pvid)
    ava_info = db_f.get_provider_ava_info(pvid)
    provider_data['url'] = url
    # ava_num, ava_fin, ava_fin_yes,ava_fin_dec, ava_fin_no,ava_fin_outdate, ava_up, ava_up_acc, ava_up_dec, ava_up_pend
    if ava_info:
        provider_data['ava_num'] =  ava_info[0]
        provider_data['ava_fin'] =  ava_info[1]
        provider_data['ava_fin_yes'] =  ava_info[2]
        provider_data['ava_fin_no'] =  ava_info[3]
        provider_data['ava_up'] = ava_info[4]
        provider_data['ava_up_acc'] =  ava_info[5]
        provider_data['ava_up_dec'] =  ava_info[6]
        provider_data['ava_up_pend'] =  ava_info[7]
    provider_ava= db_f.get_provider_ava(pvid)
    if provider_ava:
        provider_data['past_ava'], provider_data['fut_ava'] = provider_ava[0], provider_ava[1]
      
    return render_template('provider_main.html', provider_data = provider_data)


@app.route('/reg_patient', methods=['GET','POST'])
def reg_patient():
    if request.method == 'POST':
        pemail = request.form['pemail']
        password = request.form['password']
        pname = request.form['pname']
        SSN = request.form['SSN']
        birthdt = request.form['birthdt']
        paddress = request.form['paddress']
        pphone = request.form['pphone']     
        madix = request.form['madix']
        px = request.form['px']
        py = request.form['py']

        # check input
        if not pname or not pemail or not password or not SSN or not birthdt or not px  or not py or not paddress or not madix:
            flash('Invalid input - please make sure filled in all fields')
        elif not check_phone(pphone):
            flash('Invalid input - please make sure input phone is valid')
        elif not check_email(pemail):
            flash('Invalid input - please make sure input email is valid')
        elif not check_SSN(SSN):
            flash('Invalid input - please make sure input SSN is valid')
        elif db_f.add_patient(pemail, password, pname, SSN, birthdt, pphone, px, py, get_group(birthdt), madix, paddress):
            flash('registered Successfully!')
            return redirect( url_for('user_login'))
        else:
            flash('Invalid input - This SSN has already registered.')

    return render_template('new_patient.html')


@app.route('/reg_provider', methods=['GET','POST'])
def reg_provider():
    if request.method == 'POST':
        pvname = request.form['pvname']
        ppassword = request.form['ppassword']
        pvaddress = request.form['pvaddress']
        pvtype = request.form['type']
        pvphone = request.form['pvphone']
        pvx = request.form['pvx']
        pvy = request.form['pvy']

        # check input 
        if not pvname or not ppassword or not pvx  or not pvy or not pvaddress or not pvphone or not pvaddress:
            flash('Invalid input - please make sure filled in all fields')
        elif not check_phone(pvphone):
            flash('Invalid input - please make sure your phone number is valid')
        elif db_f.add_provider(pvname, ppassword, pvtype, pvaddress, pvphone, pvx, pvy):
            flash('registered Successfully!')
            return redirect( url_for('user_login'))
        else:
            flash('Invalid input - please try different username')

    return render_template('new_provider.html')


if __name__=="__main__":
    app.run()
