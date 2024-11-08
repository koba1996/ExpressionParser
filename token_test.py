import unittest
from parsing import Token

class TestToken(unittest.TestCase):

    def test_positive_number_token(self):
        under_test = Token('42', 'number')
        self.assertEqual(under_test.value, 42)

    def test_negative_number_token(self):
        under_test = Token('-42', 'number')
        self.assertEqual(under_test.value, -42)

    def test_unsupported_number_token(self):
        with self.assertRaises(ValueError):
            Token('4.2', 'number')

    def test_bracket_token(self):
        under_test = Token('(', 'bracket')
        self.assertEqual(under_test.value, '(')

    def test_operator_token(self):
        under_test = Token('*', 'op')
        self.assertEqual(under_test.value, '*')

    def test_error_token(self):
        under_test = Token('TestError', 'error')
        self.assertEqual(under_test.value, 'There was an error during the process: TestError')

    def test_unsupported_token_type(self):
        with self.assertRaises(ValueError):
            Token('42', 'NotExistingType')

if __name__ == '__main__':
    unittest.main()