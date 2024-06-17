import json
from Base_User import BaseUser
from Customer import Customer
from PM import Project_Manager



class Service_Provider(BaseUser):
    Service_Providers_Lists = []

    def __init__(self, Username=None, ID=None, Gmail=None, Password=None):
        super().__init__(Username, ID, Gmail, Password)
        Service_Provider.Service_Providers_Lists.append(self)

    def create_account(self):
        self.create_username()
        self.create_gmail()
        self.create_password()
        self.create_id()

    def receive_customer_requests(self):
        for customer in Customer.Customers_Lists:
            if customer.requests:
                print(f"Requests for {customer.Username}: {customer.requests}")

    def price_request_and_respond(self, customer_id, request, price):
        customer = next((cust for cust in Customer.Customers_Lists if cust.ID == customer_id), None)
        if customer:
            if request in customer.eventname:
                bill = f"Request '{request}' priced at {price}"
                customer.bill.append(bill)
                print(bill)
                Customer.save_customers_to_file("Store_file.txt")
            else:
                print(f"Event name '{request}' not found in customer's booked events.")
        else:
            print(f"No customer found with ID {customer_id}")



    def determine_ready_date(self, customer_id, request, ready_date):
        customer = next((cust for cust in Customer.Customers_Lists if cust.ID == customer_id), None)
        pm = next((pm for pm in Project_Manager.project_manager_list if pm.ID == customer_id), None)
        if customer and request in customer.requests:
            response = f"Request '{request}' will be ready by {ready_date}"
            customer.responses.append(response)
            if pm:
                pm.responses.append(response)
            print(response)
            Project_Manager.save_pm_to_file("Store_PM_file.txt")
            Customer.save_customers_to_file("Store_file.txt")
        else:
            print(f"No customer found with ID {customer_id} or request '{request}' not found in customer's requests.")

    def show_customer_booking(self):
        for customer in Customer.Customers_Lists:
            if customer.bookings:
                print(f"Bookings for {customer.Username}: {customer.bookings}")

    def send_response_to_pm(self, pm_id, customer_id, response):
        pm = next((pm for pm in Project_Manager.project_manager_list if pm.ID == pm_id), None)
        if pm:
            pm.responses.append({"customer_id": customer_id, "response": response})
            print(f"Sending response '{response}' to project manager '{pm.Username}' for customer ID '{customer_id}'")
            Project_Manager.save_pm_to_file("Store_PM_file.txt")
        else:
            print(f"Project Manager with ID {pm_id} not found.")

    @classmethod
    def load_sp_from_file(cls, filename):
        try:
            with open(filename, 'r') as file:
                sp_data = json.load(file)
                for data in sp_data:
                    sp = cls.from_dict(data)
                    cls.Service_Providers_Lists.append(sp)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    @classmethod
    def save_sp_to_file(cls, filename):
        with open(filename, 'w') as file:
            sp_data = [sp.to_dict() for sp in cls.Service_Providers_Lists]
            json.dump(sp_data, file, indent=4)

    def manage_requests(self):
        while True:
            choice = input("Enter '1' to view requests, '2' to price requests,'3' to determine ready date, '4' to send response to PM, '5' to show customer booking, '5' to logout: ")
            if choice == '1':
                self.receive_customer_requests()
            elif choice == '2':
                try:
                    customer_id = int(input("Enter customer ID: "))
                    eventname = input("Enter Event_Name: ")
                    price = input("Enter price: ")
                    self.price_request_and_respond(customer_id, eventname, price)
                except ValueError:
                    print("Invalid input for customer ID. Please enter a valid number.")



            elif choice == '3':
                self.show_customer_booking()
                try:
                    customer_id = int(input("Enter customer ID: "))
                    request = input("Enter request: ")
                    ready_date = input("Enter ready date: ")
                    self.determine_ready_date(customer_id, request, ready_date)
                except ValueError:
                    print("Invalid input for customer ID. Please enter a valid number.")

            elif choice == '4':
                try:
                    pm_id = int(input("Enter PM ID: "))
                    customer_id = int(input("Enter customer ID: "))
                    response = input("Enter response: ")

                    self.send_response_to_pm(pm_id, customer_id, response)
                except ValueError:
                    print("Invalid input for customer ID or PM ID. Please enter a valid number.")

            elif choice == '5':
                self.show_customer_booking()

            elif choice == '6':
                break
            else:
                print("Invalid choice. Please enter '1', '2', '3', '4', '5',or '6'")

    def to_dict(self):
        data = super().to_dict()
        return data

    @classmethod
    def from_dict(cls, data):
        sp = super().from_dict(data)
        return sp
