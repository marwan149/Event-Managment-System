import random
import re
import json

class BaseUser:
    def __init__(self, Username=None, ID=None, Gmail=None, Password=None):
        self.Username = Username
        self.ID = ID
        self.Gmail = Gmail
        self.Password = Password
        self.contacts = []

    def create_gmail(self):
        while True:
            gmail = input("Enter a correct Gmail address: ")
            if re.match(r'^[a-zA-Z0-9._%+-]+@(gmail|yahoo)\.com$', gmail):
                self.Gmail = gmail
                break
            print("Invalid Gmail address. Please enter a correct one.")

    def create_id(self):
        self.ID = random.randint(1, 100000)

    def create_username(self):
        self.Username = input("Enter Your Username: ")

    def create_password(self):
        while True:
            password = input("Enter a strong Password (must contain alphabetic, numeric, and one of {@,#,$,%}): ")
            if re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%])[A-Za-z\d@#$%]{8,}$', password):
                self.Password = password
                break
            print("Invalid Password. Please try again with at least 8 characters including alphabets, numbers, and one of {@,#,$,%}.")

    def to_dict(self):
        return {
            "Username": self.Username,
            "ID": self.ID,
            "Gmail": self.Gmail,
            "Password": self.Password,
            "contacts": self.contacts
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            Username=data.get("Username"),
            ID=data.get("ID"),
            Gmail=data.get("Gmail"),
            Password=data.get("Password")
        )
        user.contacts = data.get("contacts", [])
        return user

    @staticmethod
    def check_existing_data(username, gmail, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
            for user_data in data:
                if user_data["Username"] == username:
                    return False, "Username already exists. Please choose another."
                if user_data["Gmail"] == gmail:
                    return False, "Gmail address already exists. Please enter a different one."
        return True, None


