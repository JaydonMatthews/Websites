# Library imports
from flask import Flask, render_template, url_for

app = Flask(__name__)

# Loads the Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Loads the About Page
@app.route("/about")
def about():
    return render_template("about.html")

# Loads the Services Page
@app.route("/services")
def services():
    return render_template("services.html")

# Loads the Careers Page
@app.route("/careers")
def careers():
    return render_template("careers.html")

# Loads the Contact Page
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Loads the Terms of Service Page
@app.route("/t_of_s")
def t_of_s():
    return render_template("t_of_s.html")

# Loads the Privacy Policy Page
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# Loads the Cookies Page
@app.route("/cookies")
def cookies():
    return render_template("cookies.html")

# Loads the Equality and Diversity Page
@app.route("/e_and_d")
def e_and_d():
    return render_template("e_and_d.html")

if __name__ == '__main__':
    app.run()