import unittest
from VoucherApp import VoucherPrinter

class PrintTests(unittest.TestCase):

    def setUp(self):
        self.voucher = VoucherPrinter()
        self.columns = 3
        self.voucher_1 = {'serial_number': '100000000', 
                            'expiry_date': '2020-01-01', 
                            'description': 'Cell-C 10.00', 
                            'pin': '6374897623'}
        self.voucher_2 = {'serial_number': '300000010', 
                            'expiry_date': '2020-01-01', 
                            'description': 'Vodacom 12.00', 
                            'pin': '2436234623344'}
        self.voucher_3 = {'serial_number': '100000005', 
                            'expiry_date': '2020-01-01', 
                            'description': 'Cell-C 10.00', 
                            'pin': '6374806733'}
        self.voucher_4 = {'serial_number': '300000012', 
                            'expiry_date': '2020-01-01', 
                            'description': 'Vodacom 12.00', 
                            'pin': '1451357622123'}
        self.voucher_5 = {'serial_number': '300000013', 
                            'expiry_date': '2020-01-01', 
                            'description': 'Vodacom 12.00', 
                            'pin': '2374897623135'}

    def test_items(self):
        items = [
            self.voucher_1,
            self.voucher_2,
            self.voucher_3
        ]
        response = self.voucher.get_items_to_print(self.columns, items)
        self.assertEqual(len(response), 3)
        self.assertEqual(len(items), 0)

    def test_no_items(self):
        items = []
        response = self.voucher.get_items_to_print(self.columns, items)
        self.assertEqual(len(response), 0)
        self.assertEqual(len(items), 0)

    def test_items_not_enough(self):
        items = [
            self.voucher_1,
            self.voucher_2
        ]
        response = self.voucher.get_items_to_print(self.columns, items)
        self.assertEqual(len(response), 2)
        self.assertEqual(len(items), 0)

    def test_items_left_over(self):
        items = [
            self.voucher_1,
            self.voucher_2,
            self.voucher_3,
            self.voucher_4
        ]
        response = self.voucher.get_items_to_print(self.columns, items)
        self.assertEqual(len(response), 3)
        self.assertEqual(len(items), 1)

    def test_items_left_over_no_columns(self):
        items = [
            self.voucher_1,
            self.voucher_2,
            self.voucher_3,
            self.voucher_4
        ]
        response = self.voucher.get_items_to_print(0, items)
        self.assertEqual(len(response), 0)
        self.assertEqual(len(items), 4)


if __name__ == '__main__':
    unittest.main()
