# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import hashlib
from flask import send_file
import io
import sys


class Backend:

    def __init__(self):
        """
        Initializes a Backend object with clients for the content and user buckets."""
        self.content_bucket_name = "wiki_content_bucket"
        self.user_bucket_name = "users_passwords_bucket"
        self.client = storage.Client()
        self.content_bucket = self.client.bucket(self.content_bucket_name)
        self.user_bucket = self.client.bucket(self.user_bucket_name)

    def get_wiki_page(self, page_name):
        """
        Gets the content of a wiki page from the content bucket with the specified name
        returns Content of the wiki page, or None if the page does not exist.
        """
        specified_page = self.content_bucket.blob(page_name)
        if not specified_page.exists():
            return f"Erorr: The page {page_name} does not exists in the bucket."
        return specified_page.download_as_text()

    # def get_all_page_names(self):
    #     """returns names of all wiki pages or txt files user upload in the content bucket."""
    #     all_pages_list = []
    #     blobs = self.content_bucket.list_blobs(prefix="")
    #     for  blob in blobs:
    #         if blob.name.endswith(".txt"):
    #             all_pages_list.append(blob.name)
    #     return all_pages_list
    def get_all_page_names(self):
        """returns names of all wiki pages or txt files user upload in the content bucket."""
        all_pages_list = []
        blobs = self.content_bucket.list_blobs(prefix="")
        for blob in blobs:
            if blob.name.endswith(".txt"):
                curr_page_name = blob.name[:len(blob.name) - 4]
                all_pages_list.append(curr_page_name)
        return all_pages_list

    def upload(self, file_name, content):
        blob = self.content_bucket.blob(file_name)
        blob.upload_from_file(content)

    def sign_up(self, username, password):
        """
        Adds user data if it does not exist along with a hashed password.
        returns True if the user was added successfully, False if the user already exists.
        """
        site_secret = "brainiacs_password"
        blob = self.user_bucket.blob(username)
        if blob.exists():
            return False  #User already exists  so returns False

        password_with_salt = f"{username}{site_secret}{password}"
        hashed_password = hashlib.blake2b(
            password_with_salt.encode()).hexdigest()  #returns a str objects
        curr_user_details = username + ":" + hashed_password
        blob.upload_from_string(curr_user_details)
        return True  # User added successfully

    def sign_in(self, username, password):
        """
        Checks if a password, when hashed, matches the password in the user bucket.
        returns True if the password matches, False otherwise.
        """
        blob = self.user_bucket.blob(username)
        if not blob.exists():
            return False  #User does not exist
        curr_user_details = blob.download_as_text(
        )  #downloads : "sajan:testpassword"
        stored_user_password = curr_user_details.split(":")[1]

        site_secret = "brainiacs_password"
        password_with_salt = f"{username}{site_secret}{password}"
        hashed_password = hashlib.blake2b(
            password_with_salt.encode()).hexdigest()
        if hashed_password == stored_user_password:
            return True  #signed in successfully
        return False  #wrong password

    def get_image(self, image_name):
        """
        Gets an image from the image bucket.
        returns bytes: Binary data of the image, or None if the image does not exist.
        """

        blob = self.content_bucket.blob(image_name)
        if not blob.exists():
            return f"Error: Image {image_name} does not exists in the bucket."
        image_bytes = blob.download_as_bytes()
        return image_bytes

    def identify_wiki_page_content(self, page_name): 
        '''Gets the content of a wiki page from the content bucket 
        with the specified name returns Content of the wiki page as a list of words'''
        specified_page = self.content_bucket.blob(page_name)     
        if not specified_page.exists():
            return f"Erorr: The page {page_name} does not exists in the bucket."
        return specified_page.download_as_text().split()    #return a list of all the words. 
