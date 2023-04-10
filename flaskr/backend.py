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
            if blob.name.endswith(".txt") and blob.name[0:7] != "review_":
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

    """ Below methods for uploading and getting reviews"""

    def upload_reviews(self, page_name, curr_user_review, username):
        unique_review_connector = "&%!*Project#brainacs_sajan_acharya_@techx2023forSDS826%^&^%$%^&^%$%"         #this becomes the connector of the review. so we can seperate reviews based on this.
        review_txt_file = f"review_{page_name}.txt"        
        blob = self.content_bucket.blob(review_txt_file)
        if blob.exists():
          review_text = blob.download_as_text()
          old_reviews_list = review_text.split(unique_review_connector)
        else:
          old_reviews_list = []
        fresh_review = f"{username}: {curr_user_review}"
        old_reviews_list.append(fresh_review)
        updated_review_data = unique_review_connector.join(old_reviews_list)   #adds the fresh review to the old list with the unique connecter string added to the end.
        print(old_reviews_list, 'this is old review')
        print(updated_review_data, 'this is updated review')

        blob.upload_from_string(updated_review_data)
    
    def get_reviews(self, page_name):
        unique_review_connector = "&%!*Project#brainacs_sajan_acharya_@techx2023forSDS826%^&^%$%^&^%$%"         #this becomes the connector of the review. so we can seperate reviews based on this.
        review_txt_file = f"review_{page_name}.txt"
        blob = self.content_bucket.blob(review_txt_file)
        if blob.exists():
          review_data = blob.download_as_text()
          review_data_list = review_data.split(unique_review_connector)
          return review_data_list        
        else:
          return []


# my = Backend()
# #test for upload method.
# user = "sajan"
# page_name = "sajan_file_testing"
# review_text = "I liked the emoji at the end. So this means that you are doing your work"
# my.upload_reviews(page_name, review_text, user)
# print("succesfully worked")



# curr_review = my.get_reviews(page_name)
# print(curr_review)

##test for older methods
# get_page_names = my.get_all_page_names()
# print(get_page_names)
# get_page = my.get_wiki_page(get_page_names[0])
# print(get_page)

# get_page = my.get_wiki_page("greet.html")
# print(get_page)

#uploads file
# file = open("check_file.txt")
# my.upload("check_file.txt", file)
# print("completed upload")

# name = "sajan"
# password = "test10"
# print(my.sign_up(name, password))
# #added sajan.

# name = "sajan"
# password = "test10"
# print(my.sign_in(name, password))
# #returns true as user is signed in succesfully

# name = "sajan"
# password = "test1012"
# print(my.sign_in(name, password))
#returns False and error as user is not signed in succesfully

# image_bytes = my.get_image("img2.jpeg")
# with Image.open(io.BytesIO(image_bytes)) as img:
#     img.save("downloaded_img_file.jpeg")
# saves the image file into the current directory.
