from flask import Flask, redirect, url_for, render_template, request, redirect, flash, url_for, make_response, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_session import Session
from datetime import timedelta

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION TYPE"] = "filesystetm"
app.config['SECRET_KEY'] = 'CHANGEME'

current_user = ""

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/Home")
def home2():
    return render_template("Home.html")

@app.route("/Login", methods=['GET', 'POST'])
def login():
    if "user" in session:
        return redirect(url_for('profile'))

    if request.method == "POST":
        uname = request.form.get("username")
        password = request.form.get("pword")

        

        con = sqlite3.connect('Health_app.db')

        cur = con.cursor()
        value = (uname)
        statement = "SELECT username, password FROM PublicUsers WHERE username = '" + uname+"';"

        method = cur.execute(statement)
        data = method.fetchall()
        print(data)
        if len(data)>0:
             cleaned = data[0]
             print(cleaned)
             unamedb = cleaned[0]
             passworddb = cleaned[1]


             if uname == unamedb and password == passworddb:

                session.permanent = True
                session["user"] = uname


                if "user" in session:
                    current_user = session["user"]


                    if uname == "AdminAccount23" and passworddb == "SuperDuperSecurePassword":
                        current_user = uname
                        return render_template("Admin.html")
                
                    else:
                        current_user = uname
                        return redirect(url_for("profile"))
                 
             
             elif uname == unamedb and password != passworddb:
                  return render_template("Login copy.html")
             
        else:
            return render_template("Register.html")

        con.commit()

    return render_template("Login.html")

@app.route('/Logout')
def logout():
    session.pop("user", None)
    return render_template('Login.html')


@app.route("/Register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        fname = request.form.get("firstname")
        lname = request.form.get("lastname")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("pword")


        data = (fname, lname, username, email, password)
        print(data)

        con = sqlite3.connect('Health_app.db')
        cur = con.cursor()
        cur.execute('INSERT OR REPLACE INTO PublicUsers VALUES(?, ?, ?, ?, ?)', data)
        con.commit()

        return render_template("Login.html")

    return render_template("Register.html")

@app.route("/Login/Profile", methods = ['GET'])
def profile():

    try:
        current_user = session.get("user")  # Get user from session consistently

        if not current_user:
            print("No current user")
            return redirect(url_for('login'))  # Redirect to login if no user

        if current_user == "AdminAccount23":
            print("Admin in charge")
            return redirect(url_for('admin'))

        else:
            print("customer")
            # Use parameterized query to prevent SQL injection
            statement = "SELECT firstname, lastname, username, email FROM PublicUsers WHERE username = ?;"
            
            con = sqlite3.connect('Health_app.db')
            cur = con.cursor()
            cur.execute(statement, (current_user,))
            data = cur.fetchone()
            con.close()  # Ensure the connection is closed

            if data:
                firstname, lastname, username, email = data
            else:
                # Handle case where no user is found
                firstname = lastname = username = email = "Not found"

            return render_template("Profile.html", first_name=firstname, last_name=lastname, user_name=username, e_mail=email)

    except Exception as e:
        print(f"An error occurred: {e}")
        return render_template("Login.html")

@app.route("/Admin")
def admin():
    render_template("Admin.html")


@app.route('/dict_cookie')
def new_dict_cookie():
    fname = request.form.get("firstname")
    lname = request.form.get("lastname")
    username = request.form.get("username")
    email = request.form.get("email")

    #user = (fname, lname, email, username)
    user = {"first_name": fname, "last_name":lname, "email":email, "username":username}
    print(user)
    store = json.dump(user, indent = 4)
    print(store)
    response = make_response(redirect(url_for('profile')))

    response.set_cookie("User_details", store)
    return response


@app.route("/show_dictcookie")
def show_dictcookie():
    cookie_value = request.cookies.get("User_details")
    print(type(cookie_value))
    print(cookie_value)
    unpacked = json.loads(cookie_value)
    print(unpacked)
    print(type(unpacked))
    unpackeddict = dict(unpacked)
    print(unpackeddict)
    print(type(unpackeddict))

    return unpackeddict

if __name__ == '__main__':
    app.run(debug=True)

