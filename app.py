






from collections import Counter
import dataclasses
from importlib.abc import PathEntryFinder
from multiprocessing import connection
from flask import Flask, render_template, request, session, Response, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import  matplotlib.pyplot as plt
import sqlite3
from collections import defaultdict
from sqlalchemy import func



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///DATA.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


class webmedconsultmaster(db.Model):
    sno = db.Column(db.Integer, primary_key=True)   
    name = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    Age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    Weight = db.Column(db.Integer, nullable=False)
    bloodgroup = db.Column(db.String(50), nullable=False)


    def __repr__(self) -> str:
        return f"{self.sno} {self.name} {self.phone} {self.email} {self.Age} {self.gender} {self.height} {self.Weight} {self.bloodgroup}"
    

class Appoinment(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    appoinmentname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    doctor = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(250), nullable=False)
    appointment_datetime = db.Column(db.DateTime, nullable=False) 
    def __repr__(self) -> str:
        return f"{self.sno} {self.appoinmentname} {self.email} {self.doctor} {self.message} {self.appointment_datetime}"
    
class Contact(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    message = db.Column(db.String(250), nullable=False)
    def __repr__(self) -> str:
        return f"{self.sno} {self.name} {self.email} {self.message}"

with app.app_context():
    db.create_all()



@app.route('/')
def hello_world():
    # return 'Hello, World!'
    return render_template('index.html')

@app.route('/contact', methods=["GET", "POST"])
def contact():
    # return 'Hello, World!'
    if request.method == 'POST':
        # gender = request.form['gender']
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        rushi = Contact(name=name, email=email, message=message)
        db.session.add(rushi)
        db.session.commit()
    return render_template('return3.html')

@app.route('/form', methods=["GET", "POST"])
def form():
    print("inside function")
    if request.method == 'POST':
        # gender = request.form['gender']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        print(name)
        Age = request.form['Age']
        print(Age)
        gender = request.form['gender']
        print(gender)
        height = request.form['height']
        Weight = request.form['Weight']
        bloodgroup = request.form['bloodgroup']
        print("Entered in loop")
        rusih = webmedconsultmaster(name=name, phone=phone, email=email, Age=Age, gender=gender, height=height, Weight=Weight, bloodgroup=bloodgroup)
        db.session.add(rusih)
        # db.session.commit()   
        print("Executed")
        db.session.commit()
        return render_template('return.html')

    # return 'Hello, World!'
    return render_template('form.html')

@app.route('/Analysis')
def Analysis():
    # Fetch data for the first graph (appointments by doctor)
    appointments = Appoinment.query.all()
    doctor_counts = {}
    for appointment in appointments:
        doctor = appointment.doctor
        doctor_counts[doctor] = doctor_counts.get(doctor, 0) + 1
    doctor_labels = list(doctor_counts.keys())
    doctor_data = list(doctor_counts.values())

    # Fetch data for the second graph (blood groups of patients)
    patients = webmedconsultmaster.query.all()
    bloodgroups = {}
    for patient in patients:
        bloodgroups[patient.bloodgroup] = bloodgroups.get(patient.bloodgroup, 0) + 1
    bloodgroup_labels = list(bloodgroups.keys())
    bloodgroup_data = list(bloodgroups.values())

    return render_template('Analysis.html', 
                           doctor_labels=doctor_labels, 
                           doctor_data=doctor_data,
                           bloodgroup_labels=bloodgroup_labels,
                           bloodgroup_data=bloodgroup_data)

@app.route('/Analysis2')
def Analysis2():
    # Fetch appointment names from the database
    appointments = Appoinment.query.all()
    appointment_names = [appointment.appoinmentname for appointment in appointments]

    # Count occurrences of each appointment name
    appointment_counts = Counter(appointment_names)

    # Prepare data for the histogram
    labels = list(appointment_counts.keys())
    data = list(appointment_counts.values())

    # Query the database to get the data for the second graph
    # Replace this with your actual query to get the count of appointments for each appointment_datetime
    appointment_datetimes = [appointment.appointment_datetime for appointment in appointments]

    # Count occurrences of each appointment datetime
    appointment_datetime_counts = Counter(appointment_datetimes)

    # Prepare data for the second graph
    datetime_labels = list(appointment_datetime_counts.keys())
    datetime_data = list(appointment_datetime_counts.values())


    #-------
    appointments = db.session.query(func.date(Appoinment.appointment_datetime), Appoinment.doctor, func.count('*')).group_by(func.date(Appoinment.appointment_datetime), Appoinment.doctor).all()
    
    # Prepare data for plotting the graph
    doctor_labels = set()
    date_labels = set()
    appointment_data = defaultdict(dict)

    for appointment in appointments:
        date = appointment[0]
        doctor = appointment[1]
        count = appointment[2]
        doctor_labels.add(doctor)
        date_labels.add(date)
        appointment_data[date][doctor] = count

    doctor_labels = sorted(doctor_labels)
    date_labels = sorted(date_labels)

    # Prepare data for the graph
    graph_data = {
        'doctor_labels': doctor_labels,
        'date_labels': date_labels,
        'appointment_data': appointment_data
    }

    return render_template('Analysis2.html', labels=labels, data=data, datetime_labels=datetime_labels, datetime_data=datetime_data,  graph_data=graph_data)



@app.route('/Analysis3')
def Analysis3():
    # Query the database to fetch appointments grouped by date, doctor, and count
    appointments = db.session.query(func.date(Appoinment.appointment_datetime), Appoinment.doctor, func.count('*')).group_by(func.date(Appoinment.appointment_datetime), Appoinment.doctor).all()
    
    # Prepare data for plotting the graph
    doctor_labels = set()
    date_labels = set()
    appointment_data = defaultdict(dict)

    for appointment in appointments:
        date = appointment[0]
        doctor = appointment[1]
        count = appointment[2]
        doctor_labels.add(doctor)
        date_labels.add(date)
        appointment_data[date][doctor] = count

    doctor_labels = sorted(doctor_labels)
    date_labels = sorted(date_labels)

    # Prepare data for the graph
    graph_data = {
        'doctor_labels': doctor_labels,
        'date_labels': date_labels,
        'appointment_data': appointment_data
    }

    return render_template('Analysis3.html', graph_data=graph_data)



@app.route('/videocall')
def videocall():
    # return 'Hello, World!'
    return render_template('videocall.html')

@app.route('/doctinfo1')
def doctinfo1():
    # return 'Hello, World!'
    return render_template('doctinfo1.html')

@app.route('/doctinfo2')
def doctinfo2():
    # return 'Hello, World!'
    return render_template('doctinfo2.html')

@app.route('/doctinfo3')
def doctinfo3():
    # return 'Hello, World!'
    return render_template('doctinfo3.html')

@app.route('/docs')
def docs():
    # return 'Hello, World!'
    return render_template('docs.html')

@app.route('/gmeet')
def gmeet():
    # return 'Hello, World!'
    return render_template('gmeet.html')

@app.route('/appoinment', methods=["GET", "POST"])
def appoinment():
    if request.method == 'POST':
        # gender = request.form['gender']
        appoinmentname = request.form['appoinmentname']
        email = request.form['email']
        doctor = request.form['doctor']
        message = request.form['message']
        appointment_datetime = request.form['datetime'] 

        appointment_datetime = datetime.strptime(appointment_datetime, '%Y-%m-%dT%H:%M')
          
          # Check if the selected appointment datetime is in the future
        if appointment_datetime < datetime.now():
            return render_template('invalid_datetime.html')

        existing_appointment = Appoinment.query.filter((Appoinment.email == email) | (Appoinment.appoinmentname == appoinmentname)).first()
        if existing_appointment:
       
            return render_template('appontment_exist.html')

        bookappoinment = Appoinment(appoinmentname=appoinmentname, email=email, doctor=doctor, message=message, appointment_datetime=appointment_datetime)
        db.session.add(bookappoinment)
        # db.session.commit()   
        print("Executed")
        db.session.commit()
        return render_template('return2.html')
    # return 'Hello, World!'
    return render_template('appoinment.html')


  
@app.route('/cancel_appointment', methods=["POST"])
def cancel_appointment():
    if request.method == 'POST':
        cancel_appointmentname = request.form['cancel-appointmentname']
        cancel_email = request.form['cancel-email']
        
        # Query the database to find the appointment to cancel
        appointment_to_cancel = Appoinment.query.filter_by(appoinmentname=cancel_appointmentname, email=cancel_email).first()
        
        if appointment_to_cancel:
            db.session.delete(appointment_to_cancel)
            db.session.commit()
            return render_template('appointment_cancelled.html')
        else:
            return render_template('appointment_not_found.html')



if __name__ =="__main__":
    app.run(debug=True)

