import unittest
import logging
from bank_acc import BankAccount
from uuid import UUID
from usser import User, Admin

class TestUserMethods(unittest.TestCase):
    def setUp(self):
        self.user = User('user1', 'password1')

    def test_user_properties(self):
        self.assertEqual(self.user.username, 'user1')
        self.assertEqual(self.user.password, 'password1')
        self.assertEqual(self.user.account.title, 'Main_Account')
        self.assertEqual(self.user.account.balance, 10)
        self.assertIsInstance(self.user.id, UUID)

    def test_user_methods(self):
        self.user.make_deposit(100)
        self.assertEqual(self.user.account.balance, 110)
        self.user.make_withdraw(10)
        self.assertEqual(self.user.account.balance, 100)
        self.user.buy_ticket('ticket1')
        self.assertEqual(self.user.ticket_list, ['ticket1'])
        self.user.show_ticket_list()
        self.assertIsInstance(self.user.show_ticket_list(), list)
        self.assertEqual(self.user.show_account_information(), '\n                    username:user1\n                    user_id:' + str(self.user.id) + '\n                    ')

class TestAdminMethods(unittest.TestCase):
    def setUp(self):
        self.admin = Admin('admin1', 'password1')

    def test_admin_properties(self):
        self.assertEqual(self.admin.username, 'admin1')
        self.assertEqual(self.admin.password, 'password1')
        self.assertEqual(self.admin.account.title, 'Main_Account')
        self.assertEqual(self.admin.account.balance, 10)
        self.assertIsInstance(self.admin.id, UUID)

    def test_admin_methods(self):
        self.admin.make_ticket('ticket1')
        self.assertEqual(self.admin.ticket_list, ['ticket1'])
        
        
if __name__ == '__main__':
    unittest.main()