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
        return render_template("main.html") #"Hello, World!\n"

    # TODO(Project 1): Implement additional routes according to the project requirements.

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'htm'}

    def allowed_file(filename):
        return '.' in filename and \
             filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        """checks the extension and uploads valid files to the content bucket"""
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
    
    

