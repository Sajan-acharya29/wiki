from flaskr import create_app
from unittest.mock import patch
import io
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
# def test_home_page(client):
#     resp = client.get("/")
#     assert resp.status_code == 200
#     assert b"Hello, World!\n" in resp.data

# TODO(Project 1): Write tests for other routes.
def test_upload_route_successful(client):
    """ tests if the upload route is sucessfully uploading the file"""
    with patch("flaskr.backend.Backend.upload", return_value = None):
        my_file_name = "test_file.txt"
        my_file = io.BytesIO(b"this is a test file")
        
        upload_data = {'filename': my_file_name, 'file':(my_file, my_file_name)}
    response = client.post("/upload", data = upload_data)
    assert response.status_code == 200
    assert b'file sucessfully uploaded' in response.data


def test_upload_route_empty_file_name(client):
    """tests if the upload route gives redirects to request url if no file selected"""

    with patch("flaskr.backend.Backend.upload", return_value = None):
        my_file_name = ""
        my_file_content = io.BytesIO(b"this is a test file")
        
        upload_data = {'filename': my_file_name, 'file':(my_file_content, my_file_name)}
    response = client.post("/upload", data = upload_data)
    assert response.status_code == 302            #using the flash
    assert b'Redirecting' in response.data
    
def test_upload_route_no_file_content(client):
    """tests if the upload route gives redirects to request url if file is empty"""
    with patch("flaskr.backend.Backend.upload", return_value = None):
        my_file_name = "test.txt"
        
        upload_data = {'filename': my_file_name}
    response = client.post("/upload", data = upload_data)
    assert response.status_code == 302      
    assert b'Redirecting' in response.data

def test_upload_route_wrong_extension(client):
    """tests if the upload route returns wrong format file error if file is of invalid extension"""
    with patch("flaskr.backend.Backend.upload", return_value = None):
        my_file_name = "test_file.mp56"
        my_file = io.BytesIO(b"this is a test file")
        
        upload_data = {'filename': my_file_name, 'file':(my_file, my_file_name)}
    response = client.post("/upload", data = upload_data)
    assert response.status_code == 200
    assert b'wrong format file' in response.data


def test_upload_route_get_method(client):
    """tests the get method of the upload route"""
    response = client.get("/upload")
    assert response.status_code == 200
    assert b'Upload new File' in response.data




