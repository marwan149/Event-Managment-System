import json
from Customer import Customer
from PM import Project_Manager
from SP import Service_Provider
from Base_User import BaseUser

class Admin(BaseUser):
    Admins_List = []

    def __init__(self, Username=None, ID=None, Gmail=None, Password=None):
        super().__init__(Username, ID, Gmail, Password)
        Admin.Admins_List.append(self)

    def create_account(self):
        self.create_username()
        self.create_gmail()
        self.create_password()
        self.create_id()

    def manage_users(self):
        user_type = input("Enter user type to manage (customer/pm/sp): ").lower()
        if user_type in ['customer', 'pm', 'sp']:
            if user_type == 'customer':
                self._manage_specific_user(Customer.Customers_Lists, Customer.save_customers_to_file, "Store_file.txt")
            elif user_type == 'pm':
                self._manage_specific_user(Project_Manager.project_manager_list, Project_Manager.save_pm_to_file, "Store_PM_file.txt")
            elif user_type == 'sp':
                self._manage_specific_user(Service_Provider.Service_Providers_Lists, Service_Provider.save_sp_to_file, "Store_SP_file.txt")
        else:
            print("Invalid user type. Please enter 'customer', 'pm', or 'sp'.")

    def _manage_specific_user(self, user_list, save_function, filename):
        print(f"Managing users of type: {type(user_list[0]).__name__}")
        for user in user_list:
            print(f"Username: {user.Username}, ID: {user.ID}, Gmail: {user.Gmail}")

        user_id = int(input("Enter the user ID to manage: "))
        user = next((usr for usr in user_list if usr.ID == user_id), None)

        if user:
            print(f"Selected User: {user.Username}")
            action = input("Enter action (update/delete): ").lower()
            if action == "update":
                self.update_user(user)
                save_function(filename)
            elif action == "delete":
                user_list.remove(user)
                print("User deleted successfully.")
                save_function(filename)
            else:
                print("Invalid action. Please enter 'update' or 'delete'.")
        else:
            print("User not found.")

    def update_user(self, user):
        attribute = input("Enter attribute to update (username/gmail/password): ").lower()
        if attribute in ["username", "gmail", "password"]:
            new_value = input(f"Enter new {attribute}: ")
            setattr(user, attribute.capitalize(), new_value)
            print(f"{attribute.capitalize()} updated successfully.")
        else:
            print("Invalid attribute. Please enter 'username', 'gmail', or 'password'.")

    def view_all_users(self):
        print("Customers:")
        for customer in Customer.Customers_Lists:
            print(f"Username: {customer.Username}, ID: {customer.ID}, Gmail: {customer.Gmail}")
        print("\nProject Managers:")
        for pm in Project_Manager.project_manager_list:
            print(f"Username: {pm.Username}, ID: {pm.ID}, Gmail: {pm.Gmail}")
        print("\nService Providers:")
        for sp in Service_Provider.Service_Providers_Lists:
            print(f"Username: {sp.Username}, ID: {sp.ID}, Gmail: {sp.Gmail}")

    @classmethod
    def load_admins_from_file(cls, filename):
        try:
            with open(filename, 'r') as file:
                admins_data = json.load(file)
                cls.Admins_List = [cls.from_dict(data) for data in admins_data]
        except (FileNotFoundError, json.JSONDecodeError):
            cls.Admins_List = []

    @classmethod
    def save_admins_to_file(cls, filename):
        with open(filename, 'w') as file:
            admins_data = [admin.to_dict() for admin in cls.Admins_List]
            json.dump(admins_data, file, indent=4)



    def manage_admins(self):
        self.view_all_users()
        print("Admins:")
        for admin in Admin.Admins_List:
            print(f"Username: {admin.Username}, ID: {admin.ID}, Gmail: {admin.Gmail}")

        admin_id = int(input("Enter the admin ID to manage: "))
        admin = next((adm for adm in Admin.Admins_List if adm.ID == admin_id), None)

        if admin:
            print(f"Selected Admin: {admin.Username}")
            action = input("Enter action (update/delete): ").lower()
            if action == "update":
                self.update_user(admin)
                self.save_admins_to_file("admin_file.txt")
                self.log_admin_action(f"Updated admin {admin.Username}")
            elif action == "delete":
                Admin.Admins_List.remove(admin)
                print("Admin deleted successfully.")
                self.save_admins_to_file("admin_file.txt")
                self.log_admin_action(f"Deleted admin {admin.Username}")
            else:
                print("Invalid action. Please enter 'update' or 'delete'.")
        else:
            print("Admin not found.")

    def add_admin(self):
        new_admin = Admin()
        new_admin.create_account()
        Admin.Admins_List.append(new_admin)
        self.save_admins_to_file("admin_file.txt")
        self.log_admin_action(f"Added new admin {new_admin.Username}")

    def change_admin_password(self, admin):
        new_password = input("Enter new password: ")
        admin.Password = new_password
        self.save_admins_to_file("admin_file.txt")
        self.log_admin_action(f"Changed password for admin {admin.Username}")

    def manage_system(self):
        while True:
            action = input("Enter action (manage users/admins,add admin, change admin password, logout): ").lower()
            if action == "manage users":
                self.manage_users()
            elif action == "manage admins":
                self.manage_admins()
            elif action == "add admin":
                self.add_admin()
            elif action == "change admin password":
                self.change_admin_password(self)
            elif action == "logout":
                break
            else:
                print("Invalid action.")

