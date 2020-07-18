from app import app

from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

import smtplib
from email.mime.text import MIMEText

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jamiebrown@localhost/websynth'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def create_db():
    db.create_all()

class AccountDetails(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(200), unique = True)
    email = db.Column(db.String(200), unique = True)
    password = db.Column(db.String(200))
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.template_filter('clean_date')
def clean_date(dt):
    return dt.strftime('%d %b %Y')

@app.route('/')
def index():
    return render_template('public/index.html')

@app.route('/cv')
def cv():
    return render_template('public/cv.html') 

@app.route('/blog')
def blog():
    return render_template('public/blog.html') 

@app.route('/websynth')
def websynth():
    #load_user_preset()
    return render_template('public/websynth/websynth.html') 

@app.route('/websynth/sign-up', methods = ['GET', 'POST'])
def websynth_signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(email, username, password)

        #TODO: check user is/isn't in database
        #IF already if exists THEN return render_template('/public/websynth/signup.html', message='Already exists, try again')
        if db.session.query(AccountDetails).filter(AccountDetails.username == username).count() == 0:
            #new user TODO: encrypt password 
            data = AccountDetails(username, email, password)
            db.session.add(data)
            db.session.commit()

            #on successful account creation, redirect ot the websynth, TODO: user session
            send_email(username, email) 
            return redirect(url_for('.websynth_login', message='Created an account, now you can log-in.'))
        else:
            return redirect(url_for('.websynth_signup', message='Username or email address already exists'))
    try:
        if request.args['message']:
            message = request.args['message']
            return render_template('public/websynth/signup.html', message=message)
    except:
        return render_template('public/websynth/signup.html')

@app.route('/websynth/log-in', methods = ['GET', 'POST'])
def websynth_login():
    try:
        message = request.args['message']
        print(message)
    finally:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            rows = db.session.query(AccountDetails).filter(AccountDetails.username == username).all()

            #validate that there is only one username of this type, otherwise send email to admin notifying of mess up in the db
            if len(rows) == 1:
                account = rows[0]
                if password == account.password:
                    print('SUCCESSFUL LOGIN')
                    #TODO: create user session
                else:
                    print('WRONG PASSWORD')
            elif len(rows) < 1:
                print('NO USER')
            else:
                print('FATAL, USER NOT UNIQUE IN DB CONTACT ADMIN!')

        return render_template('public/websynth/login.html')

def send_email(username, email):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '26ec4006d7dc45'
    password = '13d00af8d37798'
    message = f"<h3>WebSynth User Account Created</h3><ul><li>Username: {username}</li><li>Email: {email}</li></ul>"

    sender = 'email1@example.com'
    receiver = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'WebSynth Account Creation'
    msg['From'] = sender
    msg['To'] = receiver

    #send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender, receiver, msg.as_string())
