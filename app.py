from flask import Flask, render_template, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION TYPE"] = "filesystetm"
app.config['SECRET_KEY'] = 'CHANGEME'

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/home")
def home2():
    return render_template("Home.html")

@app.route("/planyourvisit")
def planning():
    return render_template("Planning.html")

@app.route("/whatshere")
def whats_here():
    return render_template("Whats_here.html")

@app.route("/membership")
def membership():
    return render_template("Membership.html")

@app.route("/hotel")
def hotel():
    return render_template("Hotel.html")

@app.route("/booktickets")
def book_tickets():
    return render_template("Book_tickets.html")


if __name__ == '__main__':
    app.run()