
class user_data:
    def __init__(self):
        self.username = ""
        self.first_name = ""
        self.last_name = ""
        self.email = ""

    def save_username(self, username):
        self.username = username

    def save_first_name(self, first_name):
        self.first_name = first_name

    def save_last_name(self, last_name):
        self.last_name = last_name

    def save_email(self, email):
        self.email = email

    def return_values(self):
        return {"username": self.username, "first_name": self.first_name, "last_name": self.last_name, "email":self.email}