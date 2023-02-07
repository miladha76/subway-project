import unittest
import uuid
import datetime
import os
import pickle
from unittest import mock

from tickett import Ticket, ExpirableTicket, ChargebleTicket

class TestTicket(unittest.TestCase):
	def setUp(self):
		self.ticket = Ticket()
		self.expirable_ticket = ExpirableTicket()
		self.chargeble_ticket = ChargebleTicket()

	def test_Ticket(self):
		self.assertIsInstance(self.ticket, Ticket)
		self.assertIsNotNone(self.ticket.ticket_id)
		self.assertIsInstance(self.ticket.creation_date, datetime.datetime)
		self.assertFalse(self.ticket.expire)

	def test_ExpirableTicket(self):
		self.assertIsInstance(self.expirable_ticket, ExpirableTicket)
		self.assertIsNotNone(self.expirable_ticket.ticket_id)
		self.assertIsInstance(self.expirable_ticket.creation_date, datetime.datetime)
		self.assertIsInstance(self.expirable_ticket.expiration_date, datetime.datetime)
		self.assertEqual(self.expirable_ticket.balance, 50)

	def test_chargeble_ticket(self):
		self.assertIsInstance(self.chargeble_ticket, ChargebleTicket)
		self.assertIsNotNone(self.chargeble_ticket.ticket_id)
		self.assertIsInstance(self.chargeble_ticket.creation_date, datetime.datetime)
		self.assertEqual(self.chargeble_ticket.balance, 50)

	def test_use_ticket_ExpirableTicket(self):
		self.expirable_ticket.use_ticket()
		self.assertEqual(self.expirable_ticket.balance, 40)

	def test_charge_ticket_ChargebleTicket(self):
		self.chargeble_ticket.charge_ticket(10)
		self.assertEqual(self.chargeble_ticket.balance, 60)

	def test_update_ExpirableTicket(self):
		self.expirable_ticket._update()
		ticket_id = self.expirable_ticket.ticket_id
		with open(f"C:/Users/DearUser/Desktop/metro-gp/tickets/{ticket_id}.ticket.pickle", 'rb') as ticket:
			loaded_ticket = pickle.load(ticket)
			self.assertEqual(loaded_ticket.ticket_id, ticket_id)

	def test_update_ChargebleTicket(self):
		self.chargeble_ticket._update()
		ticket_id = self.chargeble_ticket.ticket_id
		with open(f"C:/Users/DearUser/Desktop/metro-gp/tickets/{ticket_id}.ticket.pickle", 'rb') as ticket:
			loaded_ticket = pickle.load(ticket)
			self.assertEqual(loaded_ticket.ticket_id, ticket_id)
    
def test_delete_chargeble_ticket(self):
    self.assertEqual(self.chargeble_ticket._delete_ticket(), 'File has been deleted')
    self.assertFalse(os.path.isfile(f"C:/Users/DearUser/Desktop/metro-gp/tickets/{self.chargeble_ticket.ticket_id}.ticket.pickle"))

def test_delete_expirable_ticket(self):
    self.assertEqual(self.expirable_ticket._delete_ticket(), 'File has been deleted')
    self.assertFalse(os.path.isfile(f"C:/Users/DearUser/Desktop/metro-gp/tickets/{self.expirable_ticket.ticket_id}.ticket.pickle"))
        
def test_repr_expirable_ticket(self):
    expirable_ticket = ExpirableTicket()
    expected_repr = f'\tType: Expirable Ticket\n\tTicket ID: {expirable_ticket.ticket_id}\n\tExpiration Date: {expirable_ticket.expiration_date}\n\tCredit: {expirable_ticket.balance}'
    self.assertEqual(repr(expirable_ticket), expected_repr)

def test_repr_chargeable_ticket(self):
    chargeable_ticket = ChargebleTicket()
    expected_repr = f'\tType: Chargeble Ticket\n\tTicket ID: {chargeable_ticket.ticket_id}\n\tCredit: {chargeable_ticket.balance}'
    self.assertEqual(repr(chargeable_ticket), expected_repr)

@mock.patch("os.remove")
def test_chargeble_ticket_expire(self, mock_remove):
        ticket = ChargebleTicket()
        ticket.expire()
        file_path = f"C:/Users/DearUser/Desktop/metro-gp/tickets/{ticket.ticket_id}.pickle"
        mock_remove.assert_called_once_with(file_path)

@mock.patch("os.remove")
def test_expirable_ticket_expire(self, mock_remove):
        ticket = ExpirableTicket()
        with mock.patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2022, 12, 31)
            ticket.expire()
        file_path = f"C:/Users/DearUser/Desktop/metro-gp/tickets/{ticket.ticket_id}.pickle"
        mock_remove.assert_not_called()

        with mock.patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1)
            ticket.expire()
        mock_remove.assert_called_once_with(file_path)

if __name__ == "__main__":
    unittest.main()



