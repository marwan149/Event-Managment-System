import json
from Base_User import BaseUser
from Customer import Customer

class Project_Manager(BaseUser):
    project_manager_list = []

    def __init__(self, Username=None, ID=None, Gmail=None, Password=None):
        super().__init__(Username, ID, Gmail, Password)
        self.requests = []
        self.response = []
        self.bill = []
        Project_Manager.project_manager_list.append(self)

    def create_account(self):
        self.create_username()
        self.create_gmail()
        self.create_password()
        self.create_id()

    def receive_customer_requests(self):
        for customer in Customer.Customers_Lists:
            if customer.requests:
                print(f"Requests for {customer.Username}: {customer.requests}")



    def add_request(self, request):
        self.requests.append(request)
        print(f"Request added: {request}")



    def contact_customer(self, customer_id, response):
        customer = next((cust for cust in Customer.Customers_Lists if cust.ID == customer_id), None)
        if customer:
            self.response.append({"customer_id": customer_id, "response": response})
            print(f"Sending response '{response}' for customer '{customer.Username}'")
            customer.responses.append(response)
            self.save_pm_to_file("Store_PM_file.txt")
            Customer.save_customers_to_file("Store_file.txt")
        else:
            print(f"Customer with ID {customer_id} not found.")

    def forward_response_to_customer(self, customer_id):
        customer = next((cust for cust in Customer.Customers_Lists if cust.ID == customer_id), None)
        if customer:
            for resp in self.response:
                if resp["customer_id"] == customer_id:
                    customer.responses.append(resp["response"])
                    print(f"Forwarding response '{resp['response']}' to customer '{customer.Username}'")
            Customer.save_customers_to_file("Store_file.txt")
        else:
            print(f"Customer with ID {customer_id} not found.")


    def notify_new_requests(self):
        new_requests_count = sum(1 for customer in Customer.Customers_Lists if customer.requests)
        if new_requests_count > 0:
            print(f"You have {new_requests_count} new customer requests.")

    def manage_requests(self):
        while True:
            choice = input("Enter '1' to view requests, '2' to send response,'3' to forward response to Customer, '4' to notify new requests, '5' to logout: ")
            if choice == '1':
                self.receive_customer_requests()
            elif choice == '2':
                try:
                    customer_id = int(input("Enter customer ID: "))
                    response = input("Enter response: ")
                    self.contact_customer(customer_id, response)
                except ValueError:
                    print("Invalid input for customer ID. Please enter a valid number.")


            elif choice == '3':
                try:
                    customer_id = int(input("Enter customer ID: "))
                    self.forward_response_to_customer(customer_id)
                except ValueError:
                    print("Invalid input for customer ID. Please enter a valid number.")
            elif choice == '4':
                self.notify_new_requests()
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please enter '1', '2', '3', '4',or '5'.")

    @classmethod
    def load_pm_from_file(cls, filename):
        try:
            with open(filename, 'r') as file:
                pm_data = json.load(file)
                for data in pm_data:
                    pm = cls.from_dict(data)
                    cls.project_manager_list.append(pm)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    @classmethod
    def save_pm_to_file(cls, filename):
        with open(filename, 'w') as file:
            pm_data = [pm.to_dict() for pm in cls.project_manager_list]
            json.dump(pm_data, file, indent=4)

    @classmethod
    def from_dict(cls, data):
        return cls(
            Username=data.get('Username'),
            ID=data.get('ID'),
            Gmail=data.get('Gmail'),
            Password=data.get('Password')
        )

    def to_dict(self):
        return {
            'Username': self.Username,
            'ID': self.ID,
            'Gmail': self.Gmail,
            'Password': self.Password,
            'requests': self.requests,
            'response': self.response,
            'bill': self.bill
        }