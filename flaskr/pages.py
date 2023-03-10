from flask import render_template

def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("home.html")#"Hello, World!\n"


    # TODO(Project 1): Implement additional routes according to the project requirements.

    @app.route('/about')
    def about():
        return render_template("about.html")
    
    @app.route('/pages')
    def pages():
        return render_template("pages.html")
    
    @app.route('/Hillwood')
    def hilwood():
        return render_template("Hillwood.html")
    
    @app.route('/Basilica')
    def basilica():
        return render_template("Basilica.html")
    
    @app.route('/Albert')
    def albert():
        return render_template("Albert.html")

    @app.route('/Anderson')
    def anderson():
        return render_template("Anderson.html")

    @app.route('/Arboetum')
    def arboetum():
        return render_template("Arboetum.html")
    
    @app.route('/Dumbarton')
    def dumbarton():
        return render_template("Dumbarton.html")
    
    @app.route('/Lincoln')
    def lincoln():
        return render_template("Lincoln.html")
    
    @app.route('/Office')
    def office():
        return render_template("Office.html")
    
    @app.route('/Postal')
    def postal():
        return render_template("Postal.html")

    @app.route('/Wilson')
    def wilson():
        return render_template("Wilson.html")
