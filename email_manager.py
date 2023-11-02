import os
import smtplib
import requests

user_name = os.environ["user_name"]
base_url = "https://api.sheety.co"
sheet = os.environ["sheet"]
project = "cheapFlightDeals"
users_endpoint = f"{base_url}/{user_name}/{project}/{sheet}"

headers = {
    "Authorization": os.environ["Authorization"]
}

response = requests.get(url=users_endpoint, headers=headers)
users_data = response.json()["users"]


def get_row_id(email):
    for user_data in users_data:
        if user_data["email"] == email:
            return user_data["id"]


def email_in_data(email):
    for user_data in users_data:
        if email == user_data["email"]:
            return True
    return False


class EmailManager:
    def __init__(self):
        def update_sheet(first_name, last_name, user_email, put_data):
            data = {
                "user": {
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": user_email
                }
            }

            if put_data:
                row_id = get_row_id(user_email)
                put_endpoint = f"{users_endpoint}/{row_id}"
                response = requests.put(url=put_endpoint, json=data, headers=headers)
                print("Updated!")
            else:
                response = requests.post(url=users_endpoint, json=data, headers=headers)

        print("Welcome to Our Flight Club Company!")
        print("We will send you cheap flight details via email")
        self.f_name = input("What's your first name?\n").title()
        self.l_name = input("What's your last name?\n").title()
        email_matched = False
        put = False

        while not email_matched:
            self.email = input("What's your email address?\n")
            self.re_enter_email = input("Type your email again.\n")

            if self.email == self.re_enter_email:

                if email_in_data(self.email):
                    put = True

                email_matched = True
                update_sheet(self.f_name, self.l_name, self.email, put)


            else:
                print("Emails didn't matched try again.\n")

    def send_mail(self, message):
        sender_email = os.environ["sender_email"]
        sender_pass = os.environ["sender_pass"]
        receiver_mail = self.email

        subject = f"Subject:Cheap Flight Found!"

        message = message.encode('utf-8')

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=sender_email, password=sender_pass)
            connection.sendmail(from_addr=sender_email, to_addrs=receiver_mail,
                                msg=subject.encode('utf-8') + b'\n\n' + message)

        print("Mail sent successfully 🎉")
