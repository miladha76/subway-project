import unittest
from bank_acc import BankAccount

class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.bank_account = BankAccount(title="Test Account", balance=100)
    
    def test_deposit(self):
        self.bank_account.deposit(50)
        self.assertEqual(self.bank_account.balance, 150)
    
    def test_withdraw(self):
        self.bank_account.withdraw(50)
        self.assertEqual(self.bank_account.balance, 50)
        
    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(AssertionError) as context:
            self.bank_account.withdraw(200)
        self.assertEqual(str(context.exception), "Insufficient Funds")
        
    def test_display_account_info(self):
        result = self.bank_account.display_account_info("Test User")
        self.assertEqual(result, "User:Test User's Test Account and account balance is $99.0.\nCharging 1$ for taking balance!")
        
    def test_display_account_info_insufficient_funds(self):
        bank_account = BankAccount(title="Test Account", balance=0)
        with self.assertRaises(AssertionError) as context:
            bank_account.display_account_info("Test User")
        self.assertEqual(str(context.exception), "Insufficient Funds")

if __name__ == '__main__':
    unittest.main()