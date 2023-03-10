from flaskr.backend import Backend
from unittest.mock import MagicMock
import pytest
import hashlib
# TODO(Project 1): Write tests for Backend methods.

@pytest.fixture
def backend():
    "Creates a backend instance and mocks the content and user bucket"
    backend = Backend()
    backend.content_bucket = MagicMock()
    backend.user_bucket = MagicMock()
    return backend

  
def test_get_wiki_page_if_page_found(backend):
    """Checks if the get_wiki_page method returns correct text for a existing specified page"""
    mock_page_name = "testing_page.html"
    mock_page_content = "<html><body>this is a test content</body></html>"
    
    mock_blob = MagicMock()
    mock_blob.exists.return_value = True
    backend.content_bucket.blob.return_value = mock_blob

    curr_page_blob = backend.content_bucket.blob(mock_page_name)
    curr_page_blob.upload_from_string(mock_page_content)

    recieved_text = backend.get_wiki_page(mock_page_name)
    assert recieved_text == curr_page_blob.download_as_text()

  
def test_get_wiki_page_if_page_not_found(backend):
    """Checks if the get_wiki_page method returns error for a page not present in the bucket"""
    unavilable_page = "page_not_found.html"   

    mock_blob = MagicMock()
    mock_blob.exists.return_value = False
    backend.content_bucket.blob.return_value = mock_blob
    
    expected_error = f"Erorr: The page {unavilable_page} does not exists in the bucket."
    recieved_error = backend.get_wiki_page(unavilable_page)
    assert expected_error == recieved_error


def test_get_all_page_names(backend):
    blob1 = MagicMock()
    blob1.name = "Pages/test_page1.html"

    blob2 = MagicMock()
    blob2.name = "Pages/test_page2.html"
    backend.content_bucket.list_blobs.return_value = [blob1, blob2]
    
    expected_page_list = ['test_page1.html', 'test_page2.html']
    recieved_list = backend.get_all_page_names()
    assert recieved_list == expected_page_list

def test_get_all_page_names_excluding_invalid_page_extension(backend):
    """ checks if get_all_page_names ignores other file that does not end with .html"""
    blob1 = MagicMock()
    blob1.name = "Pages/test_page1.html"

    blob2 = MagicMock()
    blob2.name = "Pages/test_page2.html"

    blob3 = MagicMock()
    blob3.name = "Pages/test_page3.txt"

    blob4 = MagicMock()
    blob4.name = "Pages/test_page_img.jpeg"

    blob5 = MagicMock()
    blob5.name = "Pages/test_page5.html"

    backend.content_bucket.list_blobs.return_value = [blob1, blob2, blob3, blob4, blob5]
    
    expected_page_list = ['test_page1.html', 'test_page2.html', 'test_page5.html']
    recieved_list = backend.get_all_page_names()
    assert recieved_list == expected_page_list


def test_upload_html_files(backend):
    """tests if the upload method works for the .txt files"""
    mock_file_name = "mock_file.html"
    curr_mock_file_content = "<html><head></head><body><This is testing content page</h1></body></html>"
  
    curr_mock_blob = MagicMock()
    backend.content_bucket.blob.return_value = curr_mock_blob
  
     # Call the upload method with the mock file
    backend.upload(mock_file_name, curr_mock_file_content)
  
    curr_mock_blob = backend.content_bucket.blob(mock_file_name)
    assert curr_mock_blob.exists()
    
    curr_mock_blob.download_as_text.return_value = curr_mock_file_content
    recieved_mock_content = curr_mock_blob.download_as_text() 

    assert recieved_mock_content == curr_mock_file_content
    
    curr_mock_blob.upload_from_file.assert_called_with(curr_mock_file_content)

def test_upload_txt_file(backend):
    """tests if the upload method works for the .txt files"""
    mock_file_name = "mock_text_file.txt"
    curr_mock_file_content = "This is testing file for a txt file"
  
    curr_mock_blob = MagicMock()
    backend.content_bucket.blob.return_value = curr_mock_blob
  
     # Call the upload method with the mock file
    backend.upload(mock_file_name, curr_mock_file_content)
  
    curr_mock_blob = backend.content_bucket.blob(mock_file_name)
    assert curr_mock_blob.exists()
    
    curr_mock_blob.download_as_text.return_value = curr_mock_file_content
    recieved_mock_content = curr_mock_blob.download_as_text() 

    assert recieved_mock_content == curr_mock_file_content
    
    curr_mock_blob.upload_from_file.assert_called_with(curr_mock_file_content)

# def test_upload_img_files(backend):


def test_signup_new_user(backend):
    """checks if the user is successfully registered"""
    username = "sajan"
    password = "testing_password_sajan"
    curr_mock_blob = MagicMock()
    curr_mock_blob.exists.return_value = False          #so it wont directly go to user already exists.
    backend.user_bucket.blob.return_value = curr_mock_blob
    recieved_confirmation = backend.sign_up(username,password)
    assert recieved_confirmation == True

def test_signup_user_already_exists(backend):
    """checks if the signup returns false if the current user is already registered"""
    username = "sajan"
    password = "testing_password_sajan"
    curr_mock_blob = MagicMock()
    curr_mock_blob.exists.return_value = True
    backend.user_bucket.blob.return_value = curr_mock_blob
    recieved_confirmation = backend.sign_up(username,password)
    assert recieved_confirmation == False

def test_sign_in_user_succesfully_signs_in(backend):
    """checks if the user with the correct password can sucessfully sign in"""
    username = "sajan"
    password = "testing_password_sajan"

    site_secret = "brainiacs_password"
    password_with_salt = f"{username}{site_secret}{password}"
    hashed_password = hashlib.blake2b(password_with_salt.encode()).hexdigest()

    curr_user_details = username + ":" + hashed_password
    
    curr_mock_blob = MagicMock()
    curr_mock_blob.download_as_text.return_value = curr_user_details       #downloaod as text will return value like line 77 "sajan:testing_password_sajan"

    backend.user_bucket.blob.return_value = curr_mock_blob

    received_confirmation = backend.sign_in(username, password)
    assert recieved_confirmation == True


def test_sign_in_user_inputs_wrong_password(backend):
    """checks if the user with the wrong password cannot signin"""
    username = "sajan"
    curr_wrong_password = "testing_wrong_password_sajan"
    
    stored_original_password = "corrent_testing_sajan"
    site_secret = "brainiacs_password"

    password_with_salt = f"{username}{site_secret}{stored_original_password}"
    hashed_password = hashlib.blake2b(password_with_salt.encode()).hexdigest()

    curr_user_details = username + ":" + hashed_password
    
    curr_mock_blob = MagicMock()
    curr_mock_blob.download_as_text.return_value = curr_user_details       #downloaod as text will return value like line 77 "sajan:testing_password_sajan"

    backend.user_bucket.blob.return_value = curr_mock_blob

    recieved_confirmation = backend.sign_in(username, curr_wrong_password)
    assert recieved_confirmation == False

def test_sign_in_user_not_found(backend):
    username = "midnight_user"
    password = "testing_password_sajan"
    curr_mock_blob = MagicMock()
    curr_mock_blob.exists.return_value = False           #means user not present
    backend.user_bucket.blob.return_value = curr_mock_blob
    recieved_confirmation = backend.sign_in(username, password)
    assert recieved_confirmation == False







    












