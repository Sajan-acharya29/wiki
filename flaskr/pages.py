from flask import Flask, flash, request, redirect, url_for, render_template
from flaskr.backend import Backend

def make_endpoints(app):

    
    my_backend = Backend()
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("home.html") #"Hello, World!\n"

    # TODO(Project 1): Implement additional routes according to the project requirements.

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'htm'}

    def allowed_file(filename):
        return '.' in filename and \
             filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                my_backend.upload(f'{file.filename}',file) 
    
        return render_template("upload.html")  
    

    # this is just for the checking purpose.
    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        if request.method == 'POST':
            print("function calleeddd")
            username = request.form['username']
            password = request.form['password']
            # with open("text_file.txt", "w") as file:
            #     file.write(f'{username}, {password} this is the returned signin') 
            if my_backend.sign_in(username, password):
                return render_template("login_succesfull.html", sent_user_name = username)
                # return render_template("login_succesfull.html")

        return render_template("signin.html")

    @app.route('/signout', methods=['GET', 'POST'])
    def signout():
        return redirect("/")

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            print("function calleeddd")
            username = request.form['username']
            password = request.form['password']
            # with open("text_file.txt", "w") as file:
            #     file.write(f'{username}, {password} this is the returned register details') 
            if my_backend.sign_up(username, password):
                return render_template("login_succesfull.html")
  
        return render_template("signup.html")
    
    #this is camerons

    @app.route('/about')
    def about():
        # first_image_bytes = my.get_image("cameron.jpeg")
        # with Image.open(io.BytesIO(first_image_bytes)) as img:
        #     img.save("downloaded_img_file.jpeg")
        # saves the image file into the current directory.
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
