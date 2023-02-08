from bank_acc import BankAccount
import pickle
import os
import uuid
import logging
from tickett import *

admin_logger = logging.getLogger('Admin_logger')
admin_logger.setLevel(logging.INFO)
admin_f_h = logging.FileHandler('Admins.log')
admin_f_f = logging.Formatter('%(asctime)s - %(message)s')
admin_f_h.setFormatter(admin_f_f)
admin_f_h.setLevel(level=logging.INFO)
admin_logger.addHandler(admin_f_h)

class User:
    def __init__(self, username, password):
        self.username = username
        self.__password = password
        self.account = BankAccount(title="Main_Account", balance = 10)
        self.ticket_list = []
        self.__id = uuid.uuid1()

        logging.basicConfig(filename='user_instances.log', level=logging.INFO,
        format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
        logging.info('User instance created: name=%s, id=%r', self.username, self.__id)

    @property
    def id(self):
        return self.__id

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, newpass):
        self.validate_password(newpass)
        self.__password = newpass

    def reset_password(self):
        npass = self.security()
        if npass:
            self._password = npass

    def make_deposit(self, amount):
        self.account.deposit(amount)
        return self

    def make_withdraw(self, amount):
        self.account.withdraw(amount)
        return self

    def display_account_info(self):
        self.account.display_account_info(self.username)
        return self

    def buy_ticket(self, ticket):
        self.ticket_list.append(ticket)


    def make_trip(self, location):
        pass

    def use_ticket_bynumber(self, ticket):
        self.ticket_list[ticket - 1].use_ticket()
        self.ticket_validation(self.ticket_list[ticket - 1])

    def use_ticket_byid(self, ticket_id):
        for ticket in self.ticket_list:
            print(ticket)
            if ticket_id == str(ticket.ticket_id):
                ticket.use_ticket()
                self.ticket_validation(ticket)

    def charge_chargeble_ticket(self, number, amount):
        self.ticket_list[number - 1].charge_ticket(amount)


    def ticket_validation(self, ticket):
        if ticket.check_expiration():
            self.ticket_list.remove(ticket)

    def show_ticket_list(self):
        for ticket in (self.ticket_list):
            yield ticket
    def update_user(self):
        with open(f"C:/Users/DearUser/Desktop/metro-gp/user/{self.id}.pickle", 'wb') as user:
            pickle.dump(self, user)

    def show_account_information(self):
        return f"""
                    username:{self.username}
                    user_id:{self.__id}
                    """

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)

    def create_new_admin(self):
        pass

    def make_ticket(self, ticket):
        self.ticket_list.append(ticket)

    def find_user(self, filename, search_path):
        result = []
        for root, dirname, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
        with open(f'{result[0]}', 'rb') as f:
            user = pickle.load(f)
        return user

    def find_ticket(self, filename, search_path):
        result = []
        for root, dirname, files in os.walk(search_path):
            if filename in files:
                result.append(os.path.join(root, filename))
        with open(f'{result[0]}', 'rb') as f:
            ticket = pickle.load(f)
        return ticket

    def save_user(self, path="admins"):
        with open(f"{path}/{self.id}.pickle", 'wb') as user:
            pickle.dump(self, user)

    def ban_user(self, user : User):
        user.banned_user = True
        # self.__class__.ticket_list.append()

    def delete_ticket_by_id(self, ticket_id):
        os.chdir('tickets')
        os.system(f'del {ticket_id}.pickle' if os.name =='nt' else f"rm {ticket_id}.pickle")
        input()
