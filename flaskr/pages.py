from flask import render_template
from flask import request
import hashlib


def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("main.html") #"Hello, World!\n"

    # TODO(Project 1): Implement additional routes according to the project requirements.
    @app.route("/signup")
    def sing_up():
        return render_template("Sing_Up.html")
    
    @app.route("/login")
    def login():
        return render_template("Login.html")
    
    @app.route("/loginsuccesful", methods=['GET', 'POST'])
    def submit_login():
        #if Backend determines it can login <--------------------------------------------------------------------Important
        if request.method == 'POST':
            username = request.form['Username']
            password = hash = hashlib.blake2b(request.form['Password'].encode()).hexdigest()
        return render_template("Succesful.html", LogorSing = 'Login')
    
    @app.route("/Singsuccesful", methods=['GET', 'POST'])
    def submit_sing():
        #if Backend determines it can login <--------------------------------------------------------------------Important
        if request.method == 'POST':
            username = request.form['Username']
            password = hash = hashlib.blake2b(request.form['Password'].encode()).hexdigest()
        return render_template("Succesful.html", LogorSing = 'Sing Up')
