from flask import Flask, redirect, url_for, render_template, request, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/home")
def home2():
    return render_template("Home.html")

@app.route("/about")
def about():
    return render_template("About.html")

@app.route("/contact")
def contact():
    return render_template("Contact.html")

@app.route("/education")
def educcation():
    return render_template("Education.html")

@app.route("/online-courses")
def certificates():
    return render_template("Online-courses.html")

@app.route("/projects")
def projects():
    return render_template("Projects.html")

@app.route("/privacy")
def privacy():
    return render_template("Privacy.html")

@app.route("/terms")
def terms():
    return render_template("Terms.html")

if __name__ == '__main__':
    app.run(debug=True)