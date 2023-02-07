import pickle
import glob
from ticket import *
from clear import clear
import json
import logging
import os
from user import User
from admin import Admin
from bankAccount import BankAccount
from pprint import pprint

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
                    
menu = '''
__  __      _
|  \/  | ___| |_ _ __ ___
| |\/| |/ _ \ __| '__/ _ \

| |  | |  __/ |_| | | (_) |
|_|  |_|\___|\__|_|  \___/'''


def terminal_dictionary_display(dictionary):
    print(json.dumps(dictionary, indent=4))

class Menu:
    login_menu= {
        '1' : 'Bank Account Management',
        '2' : 'Buy Ticket',
        '3' : 'Take a Trip',
        '4' : 'Log out'}

    bank_acount_menu = {
        '1' : 'Deposit',
        '2' : 'Withdraw',
        '3' : 'Show Balance',
        '4' : 'Go back...'}

    buy_ticket_menu = {
        '1' : 'Chargeble',
        '2' : 'Disposable(you can use it only once)',
        '3' : 'Date Expirable',
        '4' : 'Show Ticket List',
        '5' : 'Charge Charble card'}

    admin_menu = {
        '1' : 'CREATE NEW ADMIN',
        '2' : 'CREATE TICKET',
        '3' : 'EDIT TICKETS',
        '4' : 'CREATE METRO SCHEDULE',
        '5' : 'EDIT METRO SCHEDULE',
        '6' : 'BAN USER',
        '7' : 'DELETE TICKET',
        '8' : 'Log out'
        }

    def show_ticket(self, generator):
        temp = []
        for i in enumerate(logged_in_person.show_ticket_list(), 1):
            temp.append(i)
        return

    @staticmethod
    def run():
        while True:
            clear()
            print(menu)
            print()
            print('Select one of the below')
            user_options= {
                '1' : 'Register New User',
                '2' : 'Log in as User',
                '3' : 'Log in as Administrator',
                '4' : 'Exit'
                }

            terminal_dictionary_display(user_options)

            user_input_menu = input('Choose: ')
            # REGISTER MENU
            if user_input_menu == '1':
                clear()
                name = input('Enter username: ')
                password = input('Enter password: ')
                user_obj = User(name, password)
                with open(f"users/{user_obj.id}.pickle" , 'wb') as user:
                    pickle.dump(user_obj, user)

                print('You Are Now Part of METRO')
                print(f'Your Metro ID: {user_obj.id}')
                input('C...')
            # LOGIN
            elif user_input_menu == '2':
                clear()
                objects = []
                user_id = input('Enter Unique ID(Forgot password?(y)): ')
                log_in_flag = False
                logged_in_person = None
                if user_id == 'y':
                    clear()
                    for file in glob.glob("users/*.pickle"):
                        with open(file, 'rb') as user:
                            while True:
                                try:
                                    content = pickle.load(user)
                                    objects.append(content)
                                except EOFError:
                                    break
                    # print(objects, type(objects[1].username) )
                    name = input('Enter username: ')
                    password = input('Enter password: ')
                    for user in objects:
                        # print(user.username , user.password)
                        if user.username == name:
                            if user.password == password:
                                print(f'Your id is:\n{user.id}')
                                input('C...')
                                clear()
                                break
                            else:
                                print("Wrong Password")
                                input('C...')
                                break
                # LOGIN FORGET PASSWORD
                else:
                    try:
                        with open(f"users/{user_id}.pickle", 'rb') as user:
                            user_obj = pickle.load(user)

                        logged_in_person = user_obj
                        log_in_flag = True
                    except FileNotFoundError:
                        print("User not found!")
                        input('C..')

                # LOGIN MENU
                while log_in_flag:
                    clear()
                    terminal_dictionary_display(Menu.login_menu)
                    login_user_input = input("What do you desire? ")
                    # BANK ACCOUNT MENU
                    if login_user_input == '1':
                        clear()
                        terminal_dictionary_display(Menu.bank_acount_menu)
                        user_input = input("Choose: ")
                        # DEPOSIT
                        if user_input == '1':
                            clear()
                            amount = input('The amount you want to deposit? ')
                            print('Shaparak')
                            input()
                            logged_in_person.make_deposit(float(amount))
                            print(logged_in_person.account.balance)
                            input('C...')
                        # WITHDRAW
                        elif user_input =='2':
                            pass
                        # SHOW BALANCE
                        elif user_input == '3':
                            clear()
                            try:
                                print(logged_in_person.account.display_account_info(logged_in_person.username))
                                input('C...')
                            except AssertionError as e:
                                print (e)
                                input('C...')
                    # BUY TICKET
                    elif login_user_input == '2':
                        clear()
                        terminal_dictionary_display(Menu.buy_ticket_menu)
                        user_ticket_choice  = input('choose: ')
                        if user_ticket_choice == '1':
                            try:
                                logged_in_person.make_withdraw(55)
                                ch_ticket = ChargebleTicket()
                                pickle_tickets(ch_ticket)
                                logged_in_person.buy_ticket(ch_ticket)
                                print(logged_in_person.ticket_list)
                                input("C...")
                            except AssertionError as k:
                                print(k)
                                input()
                        elif user_ticket_choice == '3':
                            try:
                                logged_in_person.make_withdraw(55)
                                ex_ticket = ExpirableTicket()
                                pickle_tickets(ex_ticket)
                                logged_in_person.buy_ticket(ex_ticket)
                                # print(logged_in_person.ticket_list)
                                input("C...")
                            except AssertionError as e:
                                print(e)
                                input('C...')
                        elif user_ticket_choice == '4':
                            clear()
                            for i in enumerate(logged_in_person.show_ticket_list(), 1):
                                print(i, '\n') 
                            input('C...')

                        elif user_ticket_choice == '5':
                            temp = []
                            for ticket in enumerate(logged_in_person.show_ticket_list(), 1):
                                if isinstance(ticket[1], ChargebleTicket):
                                    pprint( ticket, indent=1)
                                    temp.append(ticket)
                            charging = int(input('which card would you like to chrage? '))
                            amount = int(input('How much you want to charge your card?\n1.20\n2.30\n3.40\n'))
                            list_of_prices = [20, 30, 40]
                            logged_in_person.make_withdraw(list_of_prices[amount - 1])
                            # logged_in_person.ticket_list[charging - 1].charge_ticket(list_of_prices[amount-1])
                            logged_in_person.charge_chargeble_ticket(charging, list_of_prices[amount - 1])

                            print(logged_in_person.ticket_list)
                            input()


                    elif login_user_input =='3':
                        clear()
                        for i in enumerate(logged_in_person.show_ticket_list(), 1):
                                print(i, '\n') #indent=2)
                        chosen_ticket = input('Which ticket would you like to use for this Trip? ')

                        try:
                            if len(chosen_ticket) == 1 and chosen_ticket.isdigit():
                                logged_in_person.use_ticket_bynumber(int(chosen_ticket))
                            elif len(chosen_ticket) > 1:
                                logged_in_person.use_ticket_byid(chosen_ticket)

                            # logged_in_person.ticket_list[int(chosen_ticket) - 1].use_ticket()
                            print(logged_in_person.ticket_list)
                            input('Ticket has been used successfuly...')
                            input('You can now travel using metro...')
                        except AssertionError as e:
                            print(e)
                            input('C...')

                    elif login_user_input == '4':
                        with open(f'users/{logged_in_person.id}.pickle', 'wb') as user:
                            pickle.dump(logged_in_person, user)
                        break


            elif user_input_menu == '3':
                clear()
                admin_username = input('Enter username: ')
                admin_password = input('Enter password: ')
                admin_objs = []
                for file in glob.glob("admin/*.pickle"):
                        with open(file, 'rb') as admin:
                            while True:
                                try:
                                    content = pickle.load(admin)
                                    admin_objs.append(content)
                                except EOFError:
                                    break

                for admin in admin_objs:
                    if admin.username == admin_username and admin.password == admin_password:
                        terminal_dictionary_display(Menu.admin_menu)
                        admin_input = input('Choose: ')

                        if admin_input == '1':
                            name = input('Enter username: ')
                            password = input('Enter password: ')
                            admin_obj = Admin(name, password)
                            with open(f"admin/{admin_obj.id}.pickle" , 'wb') as admin:
                                pickle.dump(admin_obj, admin)
                            print('You Are Now METRO Admin')
                            print(f'Your Metro ID: {admin_obj.id}')
                            input('C...')

                        elif admin_input == '7':
                            ticket_id = input('Enter ticket ID')
                            os.chdir('tickets')
                            os.system(f'del {ticket_id}.pickle' if os.name =='nt' else f"rm {ticket_id}.pickle")
                            input()
                    else:
                        print("Are you on drugs?")
                        input('C...')

            elif user_input_menu == '4':
                break

if __name__ == '__main__':
    Menu.run()



