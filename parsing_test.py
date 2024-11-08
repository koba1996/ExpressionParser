import unittest
from parsing import lex, Token

class TestLexer(unittest.TestCase):

    def test_basic_lexing(self):
        result = lex('3+5')
        expected = [Token('3', 'number'), Token('+', 'op'), Token('5', 'number')]
        self.assertEqual(result, expected)

    def test_lexing_error(self):
        with self.assertRaises(ValueError):
            lex('\\')

    def test_lxing_ignores_whitespaces(self):
        result = lex('    ')
        expected = []
        self.assertEqual(result, expected)

    def test_lexing_handle_big_numbers(self):
        big_num = '999999999999999999999999999999999999999999999999999'
        result = lex(big_num)
        expected = [Token(big_num, 'number')]
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()