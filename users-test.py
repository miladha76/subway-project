import unittest
from bank_acc import BankAccount
from usser import User
from tickett import *

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User("test_user", "test_password")

    def test_init(self):
        self.assertEqual(self.user.username, "test_user")
        self.assertEqual(self.user.password, "test_password")
        self.assertIsInstance(self.user.account, BankAccount)
        self.assertEqual(self.user.account.balance, 10)
        self.assertEqual(self.user.ticket_list, [])

    def test_make_deposit(self):
        self.user.make_deposit(100)
        self.assertEqual(self.user.account.balance, 110)

    def test_make_withdraw(self):
        self.user.make_withdraw(5)
        self.assertEqual(self.user.account.balance, 5)

    def test_buy_ticket(self):
        ticket = Ticket(location="New York")
        self.user.buy_ticket(ticket)
        self.assertEqual(len(self.user.ticket_list), 1)
        self.assertEqual(self.user.ticket_list[0].location, "New York")

    def test_use_ticket_bynumber(self):
        ticket = Ticket(location="New York")
        self.user.buy_ticket(ticket)
        self.user.use_ticket_bynumber(1)
        self.assertEqual(len(self.user.ticket_list), 0)

    def test_use_ticket_byid(self):
        ticket = Ticket(location="New York")
        self.user.buy_ticket(ticket)
        self.user.use_ticket_byid(str(ticket.ticket_id))
        self.assertEqual(len(self.user.ticket_list), 0)

    def test_charge_chargeble_ticket(self):
        ticket = ChargebleTicket(location="New York")
        self.user.buy_ticket(ticket)
        self.user.charge_chargeble_ticket(1, 20)
        self.assertEqual(self.user.ticket_list[0].amount_left, 20)

    def test_show_ticket_list(self):
        ticket = Ticket(location="New York")
        self.user.buy_ticket(ticket)
        ticket_list = list(self.user.show_ticket_list())
        self.assertEqual(len(ticket_list), 1)
        self.assertEqual(ticket_list[0].location, "New York")

    def test_show_account_information(self):
        self.assertEqual(self.user.show_account_information(),
                         "username:test_user\nuser_id:" + str(self.user.id) + "\n")

if __name__ == '__main__':
    unittest.main()