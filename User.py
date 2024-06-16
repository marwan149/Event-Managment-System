from Customer import Customer
from PM import Project_Manager
from SP import Service_Provider
from Admin import Admin
import json

def load_all_users():
    try:
        Customer.load_customers_from_file("Store_file.txt")
        Project_Manager.load_pm_from_file("Store_PM_file.txt")
        Service_Provider.load_sp_from_file("Store_SP_file.txt")
        Admin.load_admins_from_file("Store_Admin_file.txt")
        print("Users loaded successfully.")
    except FileNotFoundError:
        print("One or more user data files not found.")
    except json.JSONDecodeError:
        print("Error decoding JSON from user data files.")

def save_all_users():
    try:
        Customer.save_customers_to_file("Store_file.txt")
        Project_Manager.save_pm_to_file("Store_PM_file.txt")
        Service_Provider.save_sp_to_file("Store_SP_file.txt")
        Admin.save_admins_to_file("Store_Admin_file.txt")
        print("Users saved successfully.")
    except Exception as e:
        print(f"Error saving users: {e}")

def create_account():
    print("\nSelect your role:")
    print("1. Customer")
    print("2. Project Manager")
    print("3. Service Provider")
    print("4. Admin")

    choice = input("Enter the number corresponding to your role: ")

    if choice == '1':
        user = Customer()
    elif choice == '2':
        user = Project_Manager()
    elif choice == '3':
        user = Service_Provider()
    elif choice == '4':
        user = Admin()
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
        return

    user.create_account()
    save_all_users()
    print(f"{user.__class__.__name__} account created successfully!")

def login():
    print("\nSelect your role to login:")
    print("1. Customer")
    print("2. Project Manager")
    print("3. Service Provider")
    print("4. Admin")

    role_choice = input("Enter the number corresponding to your role: ")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = None

    if role_choice == '1':
        user = next((cust for cust in Customer.Customers_Lists if cust.Username == username and cust.Password == password), None)
    elif role_choice == '2':
        user = next((pm for pm in Project_Manager.project_manager_list if pm.Username == username and pm.Password == password), None)
    elif role_choice == '3':
        user = next((sp for sp in Service_Provider.Service_Providers_Lists if sp.Username == username and sp.Password == password), None)
    elif role_choice == '4':
        user = next((admin for admin in Admin.Admins_List if admin.Username == username and admin.Password == password), None)
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")
        return

    if user:
        print(f"Welcome, {user.Username}!")
        if isinstance(user, Customer):
            manage_customer(user)
        elif isinstance(user, Project_Manager):
            manage_pm(user)
        elif isinstance(user, Service_Provider):
            manage_sp(user)
        elif isinstance(user, Admin):
            manage_admin(user)
    else:
        print("Invalid username or password.")

def manage_customer(customer):
    while True:
        print("\n1. Book Event\n2. Manage Booking\n3. Send Request\n4. View Bill\n5. Receive Response\n6. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            customer.book_event()
        elif choice == '2':
            customer.manage_booking()
        elif choice == '3':
            request = input("Enter your request: ")
            customer.send_request(request)
        elif choice == '4':
            customer.view_bill()
        elif choice == '5':
            customer.receive_customer_response()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

def manage_pm(pm):
    pm.manage_requests()

def manage_sp(sp):
    sp.manage_requests()

def manage_admin(admin):
    while True:
        print("\n1. Manage Users\n2. Add Admin\n3. Change Admin Password\n4. Logout")
        choice = input("Enter your choice: ")
        if choice == '1':
            admin.manage_users()
        elif choice == '2':
            admin.add_admin()
        elif choice == '3':
            admin.change_admin_password(admin)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter '1', '2', '3',or '4'.")

def main():
    load_all_users()
    while True:
        try:
            print("\n1. Create Account\n2. Login\n3. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                create_account()
            elif choice == '2':
                login()
            elif choice == '3':
                save_all_users()
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
