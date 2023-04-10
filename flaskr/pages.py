from flask import Flask, flash, request, redirect, url_for, render_template, session
from flaskr.backend import Backend


def make_endpoints(app):

    my_backend = Backend()
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.

        #return render_template("home.html")
        greetings = "Welcome To Brainiacs"
        return render_template("main.html", greetings=greetings)

    # @app.route('/about')
    # def about():
    #     # first_image_bytes = my.get_image("cameron.jpeg")
    #     # with Image.open(io.BytesIO(first_image_bytes)) as img:
    #     #     img.save("downloaded_img_file.jpeg")
    #     # saves the image file into the current directory.
    #     return render_template("about.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        """checks the extension and uploads valid files to the content bucket"""
        if session.get('loggedin', False) == False:
            return redirect(url_for('home'))

        ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'html', 'htm'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return render_template('upload.html', message="No file part")

            file = request.files['file']
            if file.filename == '':
                flash('No file selected')
                return render_template('upload.html', message="No file selected")

            if file and allowed_file(file.filename):
                my_backend.upload(f'{file.filename}', file)
                return render_template('upload.html',message="file sucessfully uploaded")
            else:
                return render_template('upload.html',message="wrong format file")
        return render_template("upload.html")

    # this is just for the checking purpose.
    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        if session.get('loggedin', False) == True:
            return redirect(url_for('home'))  
        message = None
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            if my_backend.sign_in(username, password):  # True if sign up is successful
                session['loggedin'] = True
                session['username'] = username
                if "page_to_redirect" in session:
                    redirect_page = session.pop("page_to_redirect")
                    return redirect(redirect_page)   
                return render_template("main.html",
                                       sent_user_name=username,
                                       signed_in=True)
            else:
                message = "Incorrect username or password"
        return render_template("signin.html", message=message)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():  
        if session.get('loggedin', False) == True:
            return redirect(url_for('home'))

        message = None  
        if request.method == 'POST':
            print("function calleeddd")
            username = request.form['username']
            password = request.form['password']
            # with open("text_file.txt", "w") as file:
            #     file.write(f'{username}, {password} this is the returned register details')
            if my_backend.sign_up(username, password):
                session['loggedin'] = True
                session['username'] = username                
                return render_template("login_succesfull.html")
            else:
                message = "Username already present"
        return render_template("signup.html", message = message)

    #this is camerons

    @app.route('/about')
    def about():
        # first_image_bytes = my.get_image("cameron.jpeg")
        # with Image.open(io.BytesIO(first_image_bytes)) as img:
        #     img.save("downloaded_img_file.jpeg")
        # saves the image file into the current directory.


        return render_template("about.html")

    @app.route('/pages/<page_name>', methods = ["GET", "POST"])
    def page(page_name):
        #adding sessions to prevent from logging out without logout
        if request.method == "POST":
            if "loggedin" not in session:
                if request.form.get("review") and not request.form.get("review").isspace():
                    session["page_to_redirect"] = url_for('page', page_name=page_name)
                    session["review_text"] = request.form.get("review")
        
                return redirect("/signin")
            else:         
                review_data = request.form.get("review")
                username = session.get("username")   
                if review_data and not review_data.isspace():
                    my_backend.upload_reviews(page_name, review_data, username)
                else:                  
                    flash(f'ERROR: Empty review.')
                    return redirect(url_for('page', page_name=page_name))
                return redirect(url_for('page', page_name=page_name))
        else:
            final_page_name = page_name + ".txt"
            curr_page_content = my_backend.get_wiki_page(final_page_name)
            stored_reviews = my_backend.get_reviews(page_name)
            if "review_text" in session:
                old_review_text = session.pop("review_text")
            else:
                old_review_text = ""
            return render_template("wiki_page.html",
                                page_name=final_page_name,
                                page_content=curr_page_content,
                                reviews = stored_reviews,
                                review_text = old_review_text)

    @app.route('/pages')
    def pages():
        """gets the page names from bucket and passes it to """
        all_page_names = my_backend.get_all_page_names()
        return render_template("pages.html", all_page_names=all_page_names)

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        if session.get('loggedin', False) == False:
            return redirect(url_for('home'))
        
        session.pop('loggedin', None)
        session.pop('username', None)
        return redirect(url_for("home"))
