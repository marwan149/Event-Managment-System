import json
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from Base_User import BaseUser



class Customer(BaseUser):
    Customers_Lists = []

    def __init__(self, Username=None, ID=None, Gmail=None, Password=None):
        super().__init__(Username, ID, Gmail, Password)
        self.bookings = []
        self.eventname = []  # List to store event names
        self.requests = []
        self.responses = []
        self.bill = []
        Customer.Customers_Lists.append(self)

    def create_account(self):
        self.create_username()
        self.create_gmail()
        self.create_password()
        self.create_id()
        self.send_email_notification("Account Creation", f"Your account has been created with ID: {self.ID} and password: {self.Password}")


    def create_password(self):
        while True:
            password = input("Enter a strong Password (must contain alphabetic, numeric, and one of {@,#,$,%}): ")
            if re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@#$%])[A-Za-z\d@#$%]{8,}$', password):
                self.Password = password
                break
            print("Invalid Password. Please try again with at least 8 characters including alphabets, numbers, and one of {@,#,$,%}.")

    def book_event(self):
        print("Enter The Event Details :\n")
        event_name = input("Enter The Name of The Event: \n")
        event_date = input("Enter The Date: \n")
        event_time = input("Enter The Time: \n")
        event_venue = input("Enter Event Venue: \n")
        event_info = input("What The Event About: ")

        if self.validate_event_details(event_date, event_name, event_time, event_venue, event_info):
            self.bookings.append({"name": event_name, "date": event_date, "time": event_time, "venue": event_venue, "info": event_info})
            self.eventname.append(event_name)  # Store event name in the list
            print("Event booked successfully!")
            print("Reservation number:", self.ID)
            self.send_email_notification("Event Booking", f"Your event has been booked with reservation number: {self.ID}")
        else:
            print("Invalid event details. Please enter in the correct format.")

    def validate_event_details(self, event_date, event_name, event_time, event_venue, event_info):
        return all([event_date.strip(), event_name.strip(), event_time.strip(), event_venue.strip(), event_info.strip()])

    def manage_booking(self):
        print("Your bookings:")
        for idx, booking in enumerate(self.bookings, 1):
            print(f"{idx}. {booking}")

        choice = input("Enter the number of the booking you want to Delete (0 to cancel): ")
        if choice.isdigit() and 0 < int(choice) <= len(self.bookings):
            self.bookings.pop(int(choice) - 1)
            print("Booking Deleted successfully!")
        else:
            print("Invalid choice.")

    def contact_project_manager(self, pm_id, message):
        from PM import Project_Manager  # Avoid circular import
        pm = next((pm for pm in Project_Manager.project_manager_list if pm.ID == pm_id), None)
        if pm:
            self.requests.append(message)
            pm.requests.append({"customer_id": self.ID, "message": message})
            print("Message sent successfully!")
        else:
            print(f"No project manager found with ID {pm_id}")

    def view_responses(self):
        if not self.responses:
            print("No responses to display.")
        for response in self.responses:
            print(f"Response: {response}")

    def view_bill(self):
        if not self.bill:
            print("No bills to display.")
        for bill in self.bill:
            print(f"Bill: {bill}")

    def add_bill(self, bill_details):
        self.bill.append(bill_details)
        print("Bill added successfully!")

    def receive_customer_response(self):
        for response in self.responses:
            print(f"Response: {response}")
        if not self.responses:
            print("No responses to display.")

    def send_request(self, request):
        self.requests.append(request)
        print("Request successfully sent")
        self.save_customers_to_file("Store_file.txt")

    def save_eventname(self, event_name):
        self.eventname.append(event_name)
        self.save_customers_to_file("Store_file.txt")

    def send_email_notification(self, subject, body):
        sender_email = "your_email@example.com"
        receiver_email = self.Gmail
        password = "your_email_password"

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print(f"Email sent to {self.Gmail}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "bookings": self.bookings,
            "eventname": self.eventname,
            "requests": self.requests,
            "responses": self.responses,
            "bill": self.bill
        })
        return data

    @classmethod
    def from_dict(cls, data):
        customer = super().from_dict(data)
        customer.bookings = data.get("bookings", [])
        customer.eventname = data.get("eventname", [])
        customer.requests = data.get("requests", [])
        customer.responses = data.get("responses", [])
        customer.bill = data.get("bill", [])
        return customer

    @classmethod
    def load_customers_from_file(cls, filename):
        try:
            with open(filename, "r") as f:
                customers_data = json.load(f)
                cls.Customers_Lists = [cls.from_dict(data) for data in customers_data]
        except (FileNotFoundError, json.JSONDecodeError):
            cls.Customers_Lists = []

    @classmethod
    def save_customers_to_file(cls, filename):
        with open(filename, "w") as f:
            json.dump([customer.to_dict() for customer in cls.Customers_Lists], f, indent=4)




