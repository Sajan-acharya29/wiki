from flaskr import create_app

import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello, World!\n" in resp.data

# TODO(Project 1): Write tests for other routes.
#assert resp.data == b"<h1>hello world></h1>"
def test_signup(client):
    resp = client.get("/signup")
    assert resp.status_code == 200
    assert b'<h1 style="font-size: 6; color: rgb(0, 4, 255);">Sign Up</h1>' in resp.data
    assert b'<form method="post" enctype="multipart/form-data" id="register-form">' in resp.data
    assert b'<input type="text" id="Username" name="username" placeholder="Username" required>' in resp.data
    assert b'<input type="password" id="Password" name="password" placeholder="Password" required>' in resp.data
    assert b'<input type="submit" value="Register" id="register-form-submit">' in resp.data
    assert b'<h1 style="font-size: 6; color: rgb(0, 4, 255);">Sign In</h1>' not in resp.data

def test_signin(client):
    resp = client.get("/signin")
    assert resp.status_code == 200
    assert b'<h1 style="font-size: 6; color: rgb(0, 4, 255);">Sign In</h1>' in resp.data
    assert b'<form method="post" id="login-form">' in resp.data
    assert b'<input type="text" id="Username" name="username" placeholder="Username" required>' in resp.data
    assert b'<input type="password" id="Password" name="password" placeholder="Password" required>' in resp.data
    assert b'<input type="submit" value="Login" id="login-form-submit">' in resp.data
    assert b'<h1 style="font-size: 6; color: rgb(0, 4, 255);">Sign Up</h1>' not in resp.data

def test_upload(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b'<h1>Upload new File</h1>' in resp.data
    assert b'<form method=post enctype=multipart/form-data>' in resp.data
    assert b'<input type=file name=file>' in resp.data
    assert b'<input type=submit value=Upload>' in resp.data

def test_signout(client):
    resp = client.get("/signout")
    assert b'<a href="" class="w3-bar-item w3-button w3-hide-small w3-hover-white">{{sent_user_name}}</a>' not in resp.data
    assert b'<a href="/upload" class="w3-bar-item w3-button w3-hide-small w3-hover-white">Upload</a>' not in resp.data
    assert b'<a href="/signout" class="w3-bar-item w3-button w3-hide-small w3-hover-white">Logout</a>' not in resp.data


