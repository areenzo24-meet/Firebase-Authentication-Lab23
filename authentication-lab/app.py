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
  "databaseURL": "https://proj1-2b945-default-rtdb.firebaseio.com/"}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()

app= Flask(__name__, template_folder='templates' ,static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")

    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        usename = request.form['username']
        bio = request.form['bio']

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = { "email":email, "name":name , "usename":usename , "bio":bio }
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            users = db.child("Users").get().val()
            return redirect(url_for('add_tweet'))
        except Exception as e:
            print("SIGN UP ERROR:", e)
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method =='POST' :
        try:
            title = request.form['title']
            text = request.form['text']
            UID = login_session['user']['localId']
            tweet = {"uid":UID , "title": title , "text":text}
            db.child("tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except Exception as e:
            print("Add TWEET ERROR:", e)
            error = "Authentication failed"

    return render_template("add_tweet.html")


@app.route('/all_tweets')
def all_tweets():
    tweets = db.child('tweets').get().val()
    return render_template("tweets.html", tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)