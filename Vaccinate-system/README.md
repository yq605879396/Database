# Database
Project for database + web application

## Introduction
The goal of this project is to build a web-based system for signing up people for COVID-19 vaccinations. There are three kinds of people who will interact with the system - Administrator, Provider and Patient. Provider and patient need to register in the system while we would assume that administrator has already be assigned a super account which can directly login to the system. Provider can also provide appointments while patients can provide their availabilities. And our system will regularly running a matching algorithm to matching patients with the appointments. After been assigned an appointment, patient need to respond in certain time, other wise the appointment will expire - situation includes: patient accepts an appointment and successfully gets vaccinated, patient accepts an appointment but not show up, patient accepts an appointment but cancels it before the appointment date, patient declined an appointment, patient doesn't respond to the appointment. For each assigned appointment, if it expires or be declined or be cancelled we will re-match the appointment to other patients.

## Structure
backend Database: MySQL  
database schema:  
**Group**(priority, description, startdt) PK: priority  
**Patient**(pid, pname, SSN, birthdt, paddress, px, py, pphone, username, password, maxdix, priority) PK:PID FK: priority  
**PatientAva**(pid, avad, avatime) PK: pid, avadt, avatime FK: pid  
**Provider**(pvid, pvname, pvphone, pvaddress, pvx, pvy, pvtype)  
**Appointment**(apid, pvid, time) PK:apid FK: pvid  
**Book**(pid, apid, offerdt, deadlinedt, replydt, status)  PK: pid, apid FK: pid, apid  

web-application: Flask  

This folder includes:  s
`project`  
|------ `static`: store some static files for the front-end display - including some style settings, pictures  
|------ `template`: includes five html files   
|                   `new_patient.html` and `new_provider.html` are for registration when a patient/provider want to open an account on this platform  
|                   `login.html` is the first webpage we people will encounter  
|                    `patient_main.html` and `provider_main.html` are the most important webpage where user can reach after login  
|------ `app.py`: the back end of this application, using Flask framework  
|------ `database_func.py`: ensemble of functions that dealing with database, will be called by `app.py`  
|------ `helper.py`: some helper functions like checking the format of a string, time comparison,  will be called by `app.py`  
|------ `matching.py`: program that should should be start once the platform start, it will regularly update the status of matching according   
|         to current time, and also will match patient with appointments and insert new match into the database  
|------ `encrypt.py`: encrypt function and decrypt function for username  


## How to use it  
we need to run two files  

> python app.py  # this will start the web application, once start we can visit the 127.0.0.1:5000 locally
> python match.py # this will regularly update the status according to current time and also regularly make matches between waiting patients and free appointment

## Some screen shots

<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/login.png" width="600" height="400" /> 
<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Patient-Regis.png" width="600" height="400" /> 
<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Patient-Home.png" width="600" height="400" /> 
<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Patient%20Information.png" width="600" height="400" /> 
<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Patient-Availability.png" width="600" height="400" />
<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Patient-Maching.png.png" width="600" height="400" /> 

<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Provider-Regis.png" width="600" height="400" /> 
<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Provider-Main.png" width="600" height="400" /> 
<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Provider-Information.png" width="600" height="400" /> 
<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Provider-History%20Appointment.png" width="600" height="400" /> 
<img src="https://github.com/yq605879396/Database/blob/main/Vaccinate-system/images/Provider-Matching.png" width="600" height="400" />


## More to add:
provider should be able to change status of any match: didn't show up/ vaccinated (now we directly set the status to vaccinated)  
session management  
improve matching algorithm  
