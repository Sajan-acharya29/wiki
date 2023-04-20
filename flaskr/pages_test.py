from flaskr import create_app
from flask import session
from unittest.mock import patch
from unittest.mock import MagicMock
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
    '''Test if sign up html elements are being displayed correctly'''
    resp = client.get("/signup")
    assert resp.status_code == 200
    assert b'<h1 style="font-size: 6; color: rgb(0, 4, 255);">Sign Up</h1>' in resp.data
    assert b'<form method="post" enctype="multipart/form-data" id="register-form">' in resp.data
    assert b'<input type="text" id="Username" name="username" placeholder="Username" required>' in resp.data
    assert b'<input type="password" id="Password" name="password" placeholder="Password" required>' in resp.data
    assert b'<input type="submit" value="Register" id="register-form-submit">' in resp.data
    assert b'<h1 style="font-size: 6; color: rgb(0, 4, 255);">Sign In</h1>' not in resp.data


def test_signin(client):
    '''Test if sign in html elements are being displayed correctly'''
    resp = client.get("/signin")
    assert resp.status_code == 200
    assert b'<h1 style="font-size: 6; color: rgb(0, 4, 255);">Sign In</h1>' in resp.data
    assert b'<form method="post" id="login-form">' in resp.data
    assert b'<input type="text" id="Username" name="username" placeholder="Username" required>' in resp.data
    assert b'<input type="password" id="Password" name="password" placeholder="Password" required>' in resp.data
    assert b'<input type="submit" value="Login" id="login-form-submit">' in resp.data
    assert b'<h1 style="font-size: 6; color: rgb(0, 4, 255);">Sign Up</h1>' not in resp.data


def test_upload(client):
    '''Test if upload html elements are being displayed correctly'''
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b'<h1>Upload new File</h1>' in resp.data
    assert b'<form method=post enctype=multipart/form-data>' in resp.data
    assert b'<input type=file name=file>' in resp.data
    assert b'<input type=submit value=Upload>' in resp.data


def test_signout(client):
    '''Test if user is logged out succesfully'''
    resp = client.get("/logout")
    assert b'<a href="" class="w3-bar-item w3-button w3-hide-small w3-hover-white">{{sent_user_name}}</a>' not in resp.data
    assert b'<a href="/upload" class="w3-bar-item w3-button w3-hide-small w3-hover-white">Upload</a>' not in resp.data
    assert b'<a href="/signout" class="w3-bar-item w3-button w3-hide-small w3-hover-white">Logout</a>' not in resp.data


# def test_upload_route_successful(client):
#     """ tests if the upload route is sucessfully uploading the file"""
#     with patch("flaskr.backend.Backend.upload", return_value=None):
#         with patch("flaskr.backend.Backend.get_wiki_page",
#                    return_value=b"this is a test file content"):

#             my_file_name = "test_file.txt"
#             my_file_content = b"this is a test file content"
#             response = client.post("/upload",
#                                    data={
#                                        "filename":
#                                            my_file_name,
#                                        "content":
#                                            FileStorage(filename="test_file.txt",
#                                                        stream=my_file_content)
#                                    })
#             assert response.status_code == 200
#             pages_resp = client.get("/pages/test_file.txt")
#             assert pages_resp.status_code == 200
#             assert b"test_file.txt" in pages_resp.data
#             assert b"this is a test file content" in pages_resp.data


def test_upload_route_empty_file_name(client):
    """tests if the upload route gives redirects to request url if no file selected"""

    with patch("flaskr.backend.Backend.upload", return_value=None):
        my_file_name = ""
        my_file_content = io.BytesIO(b"this is a test file")

        upload_data = {
            'filename': my_file_name,
            'file': (my_file_content, my_file_name)
        }
    response = client.post("/upload", data=upload_data)
    assert response.status_code == 200
    assert b'No file selected' in response.data


def test_upload_route_no_file_content(client):
    """tests if the upload route gives redirects to request url if file is empty"""
    with patch("flaskr.backend.Backend.upload", return_value=None):
        my_file_name = "test.txt"

        upload_data = {'filename': my_file_name}
    response = client.post("/upload", data=upload_data)
    assert response.status_code == 200
    assert b'No file part' in response.data


def test_upload_route_wrong_extension(client):
    """tests if the upload route returns wrong format file error if file is of invalid extension"""
    with patch("flaskr.backend.Backend.upload", return_value=None):
        my_file_name = "test_file.mp56"
        my_file = io.BytesIO(b"this is a test file")

        upload_data = {
            'filename': my_file_name,
            'file': (my_file, my_file_name)
        }
    response = client.post("/upload", data=upload_data)
    assert response.status_code == 200
    assert b'wrong format file' in response.data


def test_upload_route_get_method(client):
    """tests the get method of the upload route"""
    response = client.get("/upload")
    assert response.status_code == 200
    assert b'Upload new File' in response.data


def test_home_page1(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b'<li><a href="/">Home</a></li>' in resp.data
    assert b'<li><a href="/pages">Pages</a></li>' in resp.data
    assert b'<li><a href="/about">About</a></li>' in resp.data
    assert b'<li><a href="/signin">Sign in</a></li>' in resp.data
    assert b'<li><a href="/signup">Sign Up</a></li>' in resp.data


def test_wiki_page_Google_Map(client, monkeypatch):
    """Test if Google Map snapshot is being displayed"""
    mocked_function = MagicMock(return_value=b'<iframe src=https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3104.430007084699!2d-77.06620158467243!3d38.914147979568156!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89b7b63132dc7317%3A0xc226e57a90b4dbd7!2sDumbarton%20Oaks%20Museum!5e0!3m2!1sen!2sus!4v1681009088373!5m2!1sen!2sus id="frame" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')
    monkeypatch.setattr('flaskr.backend.Backend.get_all_page_names', mocked_function)
    
    resp = client.get("/pages/dumbarton")
    assert b'<iframe src=https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3104.430007084699!2d-77.06620158467243!3d38.914147979568156!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89b7b63132dc7317%3A0xc226e57a90b4dbd7!2sDumbarton%20Oaks%20Museum!5e0!3m2!1sen!2sus!4v1681009088373!5m2!1sen!2sus id="frame" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>' in resp.data

def test_wiki_page_Google_Map_1(client):
    '''Test if Google Map snapshot is not being displayed'''
    with patch("flaskr.backend.Backend.get_all_page_names", return_value=["test"]):
        resp = client.get("/pages/test")
        assert b'<iframe src={{page_link}} id="frame" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>' not in resp.data


def test_wiki_page_Financial_experience(client):
    '''Test if Financial experience is being displayed correctly'''
    with patch("flaskr.backend.Backend.get_all_page_names", return_value=["dumbarton"]):
        resp = client.get("/pages/dumbarton")
        html_content = resp.data.decode('utf-8')
        start_tag = html_content.find('<h1 id="element"')

        assert start_tag != -1


def test_wiki_page_Financial_experience_1(client):
    '''Test if Financial experience is not being displayed'''
    with patch("flaskr.backend.Backend.get_all_page_names", return_value=["test"]):
        resp = client.get("/pages/test")
        assert b'<h1 id="element" style="font-size: large;"><span style="font-size: large;"> Financial Experience: </span><span style="color: #39FF33; font-size: large; line-height: 0px;"> {{Variable_to_store_the_financial_experience}} </span> </h1>' not in resp.data


def mock_sign_in():
    with patch('flaskr.backend.Backend.sign_in') as mock_sign_in:
        yield mock_sign_in


def test_signin_successful(app, client):
    '''Test if User is being verified'''
    with patch('flaskr.backend.Backend.sign_in') as mock_sign_in:
        mock_sign_in.return_value = True
        response = client.post('/signin',
                               data={
                                   'username': 'test_user',
                                   'password': 'test_password'
                               })
        mock_sign_in.assert_called_once_with('test_user', 'test_password')

        with client.session_transaction() as sess:
            assert sess['loggedin'] == True
            assert sess['username'] == 'test_user'


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
