from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {"apiKey": "AIzaSyAKXr0OURJMdycX-AX_7Sufm8_1qSfgNAc",
  "authDomain": "proj1-2b945.firebaseapp.com",
  "projectId": "proj1-2b945",
  "storageBucket": "proj1-2b945.appspot.com",
  "messagingSenderId": "703486803598",
  "appId": "1:703486803598:web:11e5cb191e6b80ae2a13df",
  "measurementId": "G-B6QD5J1QLC",
  "databaseURL": ""}

  fierbase=pyrebase.initialize_app(config)
  auth=fierbase.auth()


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = 
auth.sign_in_with_email_and_password(email, password)
           return redirect(url_for('home'))
       except:
           error = "Authentication failed"
   return render_template("signin.html")

    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = 
auth.create_user_with_email_and_password(email, password)
           return redirect(url_for('home'))
       except:
           error = "Authentication failed"
   return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)