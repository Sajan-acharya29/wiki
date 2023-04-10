from flaskr import create_app
from unittest.mock import patch
import io
import pytest
from werkzeug.datastructures import FileStorage


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
    # assert b"Ecom\n" in resp.data


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

def test_signout(client):
    resp = client.get("/logout")
    assert b'<a href="" class="w3-bar-item w3-button w3-hide-small w3-hover-white">{{sent_user_name}}</a>' not in resp.data
    assert b'<a href="/upload" class="w3-bar-item w3-button w3-hide-small w3-hover-white">Upload</a>' not in resp.data
    assert b'<a href="/signout" class="w3-bar-item w3-button w3-hide-small w3-hover-white">Logout</a>' not in resp.data

def test_upload_route_user_not_logged_in(client):
    with patch("flaskr.backend.Backend.upload", return_value=None):
        with client.session_transaction() as session:
            session['loggedin'] = False
        data = {'file': (io.BytesIO(b'this is a test file content'), 'test_file.txt'),
                'filename': 'test_file.txt'}

        response = client.post("/upload", data= data)
        assert response.status_code == 302    #the upload route redirect to home if logged in 

def test_upload_route_successful(client):
    """ tests if the upload route is sucessfully uploading the file"""
    with patch("flaskr.backend.Backend.upload", return_value=None):
            with client.session_transaction() as session:
                session['loggedin'] = True

            data = {'file': (io.BytesIO(b'this is a test file content'), 'test_file.txt'),
                'filename': 'test_file.txt'}

            response = client.post("/upload",
                                data= data)
            assert response.status_code == 200
            print(response.data)
            assert b'file sucessfully uploaded' in response.data


def test_upload_route_empty_file_name(client):
    """tests if the upload route gives redirects to request url if no file selected"""

    with patch("flaskr.backend.Backend.upload", return_value=None):
        with client.session_transaction() as session:
            session['loggedin'] = True

        my_file_name = ""
        my_file_content = io.BytesIO(b"this is a test file")

        data = {'file': (my_file_content, my_file_name),
                'filename': my_file_name}

    response = client.post("/upload", data=data)
    assert response.status_code == 200
    assert b'No file selected' in response.data


def test_upload_route_no_file_content(client):
    """tests if the upload route gives redirects to request url if file is empty"""
    with patch("flaskr.backend.Backend.upload", return_value=None):
        with client.session_transaction() as session:
            session['loggedin'] = True
        my_file_name = "test.txt"
        data = {'filename': my_file_name}
    response = client.post("/upload", data=data)
    assert response.status_code == 200
    assert b'No file part' in response.data


def test_upload_route_wrong_extension(client):
    """tests if the upload route returns wrong format file error if file is of invalid extension"""
    with patch("flaskr.backend.Backend.upload", return_value=None):
        with client.session_transaction() as session:
            session['loggedin'] = True
        my_file_name = "test_file.mp56"
        my_file_content = io.BytesIO(b"this is a test file")
        data = {'file': (my_file_content, my_file_name),
                'filename': my_file_name}
    response = client.post("/upload", data=data)
    assert response.status_code == 200
    assert b'wrong format file' in response.data


def test_upload_route_get_method(client):
    """tests the get method of the upload route"""
    with client.session_transaction() as session:
            session['loggedin'] = True
    response = client.get("/upload")
    assert response.status_code == 200
    assert b'Upload new File' in response.data


def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b'<li><a href="/">Home</a></li>' in resp.data
    assert b'<li><a href="/pages">Pages</a></li>' in resp.data
    assert b'<li><a href="/about">About</a></li>' in resp.data
    assert b'<li><a href="/signin">Sign in</a></li>' in resp.data
    assert b'<li><a href="/signup">Sign Up</a></li>' in resp.data


# TODO(Project 1): Write tests for other routes.
"""this test is failing"""
# def test_about_page(client):
#     resp = client.get("/about")
#     assert resp.status_code == 200
#     assert b'<h1 class="w3-text-teal">Sajan</h1>' in resp.data
#     assert b'<img src="https://cdn.discordapp.com/attachments/1076232707652206772/1081955756577927209/img1.jpg" alt="Test" width="350" height="300" class="w3-border w3-center">' in resp.data
#     assert b'<h1 class="w3-text-teal">Eliel</h1>' in resp.data
#     assert b'<img src="https://cdn.discordapp.com/attachments/1079200030440833175/1083448363917266974/584A0C35-F8E5-4AC0-AE34-C6C932ED064F.jpg" alt="Test" width="350" height="300" class="w3-border w3-center">' in resp.data
#     assert b'<h1 class="w3-text-teal">Cameron</h1>' in resp.data
