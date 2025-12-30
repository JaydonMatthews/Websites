from flask import Flask, redirect, url_for, render_template, request, redirect, flash, url_for, make_response, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_session import Session
from datetime import timedelta
import requests
from markupsafe import Markup

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
    
    if request.method == "POST":
        uname = request.form.get("username")
        password = request.form.get("pword")
    
        con = sqlite3.connect('Bookclub.db')

        cur = con.cursor()
        value = (uname)
        statement = "SELECT Username, Password FROM UserDetailsTable WHERE Username = '" + uname+"';"

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
    return redirect(url_for("login"))


@app.route("/Login/ReaderProfile", methods = ['GET', 'POST'])
def profile():

    try:
        current_user = request.cookies.get("currentUser")

    except:
        print("No current user")
        return render_template("Login.html")

    else:
        current_user = session["user"]
        if current_user == "AdminAccount23":
            print("Admin in charge")
            return render_template('Admin.html')
        
        else:
            print("customer")
            

            statement = "SELECT firstname, lastname, username, email FROM UserDetailsTable WHERE username = ?;"
            con = sqlite3.connect('Bookclub.db')
            cur = con.cursor()
            method = cur.execute(statement, (current_user,))

            data = method.fetchall()

            if data:
                cleaned = data[0]
                firstname = cleaned[0]
                lastname = cleaned[1]
                username = cleaned[2]
                email = cleaned[3]

            else:
                
                firstname = lastname = username = email = "Not found"

            return render_template("ReaderProfile.html", first_name=firstname, last_name=lastname, user_name=username, e_mail=email)


@app.route("/login/BooksRead")
def booksRead():
    author = 'Jane Austen'
    params = {'inauthor': author}
    new_params = 'q='
    new_params += '+'.join('{}:{}'.format(key, value) for key, value in params.items())
    
    response = requests.get('https://www.googleapis.com/books/v1/volumes?', params=new_params)
    list_of_data = response.json()
    print(list_of_data)
    print(type(list_of_data))

    print(new_params)

    for key in list_of_data.keys():
        print(key)

    data = list_of_data['items']
    print(data)
    print(type(data))

    html_data = Markup("""<tr><td>Data</td><td>Data</td><td>Data</td><td>Data</td><td>Data</td><td>Data</td></tr>""")

    return render_template('BookRead.html', book_table = html_data, Book_Information = data)

@app.route('/search', methods=['GET'])
def search():

    query = request.args.get('query')
    if query:
        books = search_books(query)
        print(type(books))
        print(books)


        return render_template("BookRead.html", books=books)
    return render_template("BookRead.html", books=[])

def search_books(query):

    url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get('items', [])
    return []

@app.route("/Register", methods=['GET', 'POST'])
def register():
        if request.method == "POST":
            fname = request.form.get("firstname")
            lname = request.form.get("lastname")
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("pword")

            data = (fname, lname, username, email, password)
            
            con = sqlite3.connect('Bookclub.db')
            cur = con.cursor()
            cur.execute('INSERT OR REPLACE INTO UserDetailsTable VALUES(?,?,?,?,?)', data)
            con.commit()

            return render_template("Login.html")


        return render_template("Register.html")

@app.route('/BookRecommendations')
def bookrecommendations():
    return render_template('BookRecommendations.html')


if __name__ == '__main__':
    app.run()

