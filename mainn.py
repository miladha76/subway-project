
import pickle
import glob
from tickett import *
from clearr import clear
import json
import logging
import os
from usser import User, Admin
from bank_acc import BankAccount
from pprint import pprint
from exceptions import *


logging.basicConfig(filename='metro.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s %(module)s')
logger = logging.getLogger(__name__)
error_logger = logging.getLogger('error_logger')
error_f_h = logging.FileHandler('errors.log')
error_f_f = logging.Formatter('%(asctime)s - %(message)s %(name)s %(message)s %(module)s')
error_f_h.setFormatter(error_f_f)
error_logger.addHandler(error_f_h)
                    
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
        '1': 'CREATE NEW ADMIN',
        '2': 'BAN USER',
        '3': 'TICKET EIDT TOOLS',
        '4': 'Log out'
            }

    admin_ticket = {
        '1': 'CREATE TICKET',
        '2': 'EDIT TICKETS',
        '3': 'DELETE TICKET'
            }
    def show_ticket(person, generator):
        temp = []
        for i in enumerate(person.show_ticket_list(), 1):
            temp.append(i)
        return temp

    
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
                try:
                    user_obj = User(name, password)
                    with open(f"C:/Users/DearUser/Desktop/metro-gp/user/{user_obj.id}.pickle" , 'wb') as user:
                        pickle.dump(user_obj, user)

                    print('You Are Now Part of METRO')
                    print(f'Your Metro ID: {user_obj.id}')
                    input('C...')

                except AssertionError as e:
                    error_logger.error(e)
                    print(e)
                except DuplicateUsernameError as k:
                    error_logger.error(k)
                    print(k)
                except SpecialCharError as s:
                    error_logger.error(s)
                    print(s)
                
                
            # LOGIN
            elif user_input_menu == '2':
                clear()
                objects = []
                user_id = input('Enter Unique ID(Forgot password?(y)): ')
                log_in_flag = False
                logged_in_person = None
                if user_id == 'y':
                    clear()
                    for file in glob.glob("C:/Users/DearUser/Desktop/metro-gp/user/*.pickle"):
                        with open(file, 'rb') as user:
                            while True:
                                try:
                                    content = pickle.load(user)
                                    objects.append(content)
                                except EOFError:
                                    break
                    
                    name = input('Enter username: ')
                    password = input('Enter password: ')
                    for user in objects:
                      
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
                        with open(f"C:/Users/DearUser/Desktop/metro-gp/user/{user_id}.pickle", 'rb') as user:
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
                            logger.info("%s has successfuly deposited %s", logged_in_person.username, amount)
                        # WITHDRAW
                        elif user_input =='2':
                              clear()
                              amount = input('The amount you want to Withdraw? ')
                              input('Shaparak')
                              try:
                                logged_in_person.make_withdraw(float(amount))
                                print(logged_in_person.account.balance)
                                logger.info("%s has successfuly withdrew %s", logged_in_person.username, amount)
                                input('C...')
                              except AssertionError as e:
                                print(e)
                                error_logger.error(e)
                                input()
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
                            try:
                                logged_in_person.make_withdraw(list_of_prices[amount - 1])
                                logged_in_person.charge_chargeble_ticket(charging, list_of_prices[amount - 1])
                            except AssertionError as e:
                                error_logger.error(e)
                                print(e)
                                input()
                            print(logged_in_person.ticket_list)
                            c_flag = True
                            input()
                        else:
                            input('Invalid Input...')
                            
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
                        with open(f'C:/Users/DearUser/Desktop/metro-gp/user/{logged_in_person.id}.pickle', 'wb') as user:
                            pickle.dump(logged_in_person, user)
                        break


            elif user_input_menu == '3':
                clear()
                a = ''' With Great power comes great responsibility'''
                b = len(a) * '_'
                print(f"\t{b}\n\n\t{a}\n\t{b}\n")
                admin_username = input('\tEnter username: ')
                admin_password = input('\tEnter password: ')
                admin_objs = []
                Menu.extract_pickle_files(admin_objs, "admins")
               
                logged_in_admin = False
                the_admin = object
                for admin in admin_objs:
                    if admin.username == admin_username and admin.password == admin_password:
                        logged_in_admin = True
                        the_admin = admin

                if not logged_in_admin:
                    clear()
                    print("Are you on drugs?")
                    input('C...')
                    continue

                while True:
                    if logged_in_admin:
                        clear()
                        
                        terminal_dictionary_display(Menu.admin_menu)
                        admin_input = input('Choose: ')

                        if admin_input == '1':
                            clear()
                            name = input('Enter username: ')
                            password = input('Enter password: ')
                            admin_obj = Admin(name, password)
                            admin_obj.save_user()
                            print('You Are Now METRO Admin')
                            print(f'Your Metro ID: {admin_obj.id}')
                            input('C...')
                        # BAN USER
                        if admin_input == '2':
                            clear()
                            user_id = input("user ID to ban: ")
                            filename = f'{user_id}.pickle'
                            try:
                                user = the_admin.find_user(filename, './users')
                                print(user ,'\n')
                                x = input("Are you sure?(y/n)")
                                authentication = True if x =='y' else False
                                print(authentication)
                                if authentication is True:
                                    the_admin.ban_user(user)

                                    print("User banned successfuly!")
                                    input()
                                else:
                                    input()
                            except IndexError as e:
                                print("no User found!")
                                input()
                            user.update_user()



                        # CREATE TICKET
                        elif admin_input == '3':
                            clear()
                            terminal_dictionary_display(Menu.admin_ticket)
                            aticket_input = input('Choose: ')

                            if aticket_input == '1':
                                ticket_kind = int(input("What kind of ticket do you want me to create?\n1. chargeble\n2. expirable\n3. disposable\n"))
                                if ticket_kind == 1:
                                    the_admin.make_ticket(ChargebleTicket())
                                    print('1', show_ticket(the_admin, the_admin.show_ticket_list()))
                                    try:
                                        print(the_admin.show_ticket_list(1))

                                    except IndexError as e:
                                        print(e)
                                    input()
                                elif ticket_kind == 3:
                                    the_admin.make_ticket(DisposableTicket())
                                    print(the_admin.ticket_list[-1])
                                elif ticket_kind == 2:
                                    the_admin.make_ticket(ExpirableTicket())
                                    print(the_admin.ticket_list[-1])
                            elif aticket_input == '2':
                                print("Do you want to search by ID?")
                                os.chdir("tickets")
                                clear()
                                ticket_id = input("user ID to ban: ")
                                filename = f'{user_id}.pickle'
                                ticket = the_admin.find_ticket(filename, './tickets')
                                print(ticket ,'\n')
                                x = input("Are you sure?(y/n)")
                                authentication = True if x =='y' else False
                                if authentication is True:
                                    the_admin.ban_user(user)
                                    input()

                            elif aticket_input == '3':
                                clear()
                                ticket_id = input('Enter ticket ID: ')
                                os.chdir('tickets')
                                os.system(f'del {ticket_id}.pickle' if os.name == 'nt' else f"rm {ticket_id}.pickle")
                                input()

                        elif admin_input == '4':
                            the_admin.update_user()
                            break

            elif user_input_menu == '4':
                break
if __name__ == '__main__':
    Menu.run()

