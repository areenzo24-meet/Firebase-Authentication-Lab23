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
            return redirect(url_for('brand'))
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

        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = { "email":email, "name":name , "usename":usename }
            UID = login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            users = db.child("Users").get().val()
            return redirect(url_for('brand'))
        except Exception as e:
            print("SIGN UP ERROR:", e)
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/brand', methods=['GET', 'POST'])
def brand():
    return render_template("brand.html")


@app.route('/dior', methods=['GET', 'POST'])
def dior():
    if request.method == "POST":
        d_link = request.form.get('product')
        dior = {"link": d_link}
        db.child("Cart").push(dior)
        return redirect(url_for('cart'))
    return render_template('dior.html')


@app.route('/essence', methods=['GET', 'POST'])
def essence():
    if request.method == "POST":
        e_link = request.form.get('product')
        ess = {"link": e_link}
        db.child("Cart").push(ess)
        return redirect(url_for('cart'))
    return render_template('essence.html')


@app.route('/flormar', methods=['GET', 'POST'])
def flormar():
    if request.method == "POST":
        f_link = request.form.get('product')
        flo = {"link": f_link}
        db.child("Cart").push(flo)
        return redirect(url_for('cart'))
    
    return render_template('flormar.html')


@app.route('/nars', methods=['GET', 'POST'])
def nars():
    if request.method == "POST":
        n_link = request.form.get('product')
        nars = {"link": n_link}
        db.child("Cart").push(nars)
        return redirect(url_for('cart'))
    return render_template('nars.html')


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    products = db.child("Cart").get().val()
    return render_template('cart.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)