SUPPORTED_OPERATORS = ['+', '-', '*', '/']
SUPPORTED_BRACKETS = ['(', ')']
WHITESPACE = [' ', '\n', '\t']

class Token:
    def __init__(self, value, type):
        if type == 'number':
            self.value = int(value)
        elif type == 'op':
            self.value = value
        elif type == 'bracket':
            self.value = value
        elif type == 'error':
            self.value = 'There was an error during the process: ' + value
        else:
            raise ValueError
        self.type = type


def print_lex_result(tokens):
    result = '['
    for token in tokens:
        result += str(token.value) + ', '
    result = result[:-2]
    result += ']'
    print(result)


def lex(code: str) -> list[Token]:
    i = 0
    tokens = []
    while i < len(code):
        if '0' <= code[i] <= '9':
            number = code[i]
            i += 1
            while i < len(code) and '0' <= code[i] <= '9':
                number += code[i]
                i += 1
            tokens.append(Token(number, 'number'))
        elif code[i] in SUPPORTED_OPERATORS:
            tokens.append(Token(code[i], 'op'))
            i += 1
        elif code[i] in SUPPORTED_BRACKETS:
            tokens.append(Token(code[i], 'bracket'))
            i += 1
        elif code[i] in WHITESPACE:
            i += 1
        else:
            raise ValueError
    return tokens


def parse(tokens):
    print_lex_result(tokens)
    tokens = parse_brackets(tokens)
    tokens = parse_set_of_operations(tokens, ['*', '/'])
    tokens = parse_set_of_operations(tokens, ['+', '-'])
    if len(tokens) != 1:
        return Token('Could not parse expression', 'error')
    return tokens[0]


def find_closing_for_bracket(tokens, start):
    count = 0
    for index in range(start + 1, len(tokens)):
        if tokens[index].value == ')':
            if count > 0:
                count -= 1
            else:
                return index
        if tokens[index].value == '(':
            count += 1
    return -1


def is_bracket_in_expression(tokens):
    for index in range(len(tokens)):
        if tokens[index].type == 'bracket':
            return index
    return -1


def parse_brackets(tokens):
    bracket_start = is_bracket_in_expression(tokens)
    while bracket_start != -1:
        if tokens[bracket_start].value == ')':
            return [Token('Bracket started with ")"!', 'error')]
        bracket_end = find_closing_for_bracket(tokens, bracket_start)
        if bracket_end == -1:
            return [Token('Starting bracket was never closed!', 'error')]
        if bracket_end == bracket_start + 1:
            return [Token('Empty bracket!', 'error')]
        tokens = replace_tokens(bracket_start, bracket_end, parse(tokens[bracket_start + 1:bracket_end]), tokens)
        bracket_start = is_bracket_in_expression(tokens)
    return tokens


def parse_set_of_operations(tokens, operators_to_be_parsed):
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type == 'op' and token.value in operators_to_be_parsed:
            try:
                if i == 0:
                    raise IndexError
                if tokens[i - 1].type == 'op' or tokens[i + 1].type == 'op':
                    raise TypeError
                tokens = parse_simple_operator(tokens, i)
            except IndexError:
                return [Token('Operation started or ended with operator!', 'error')]
            except TypeError:
                return [Token('Two or more consecutive operators!', 'error')]
            except:
                return [Token('Error during parsing!', 'error')]
        elif token.type == 'error':
            return [Token(token.value, 'error')]
        else:
            i += 1
    return tokens


def parse_simple_operator(tokens, index):
    token = tokens[index]
    if token.value == '+':
        tokens = replace_tokens(index - 1, index + 1, Token(tokens[index - 1].value + tokens[index + 1].value, 'number'), tokens)
    elif token.value == '-':
        tokens = replace_tokens(index - 1, index + 1, Token(tokens[index - 1].value - tokens[index + 1].value, 'number'), tokens)
    elif token.value == '*':
        tokens = replace_tokens(index - 1, index + 1, Token(tokens[index - 1].value * tokens[index + 1].value, 'number'), tokens)
    elif token.value == '/':
        if tokens[index + 1].value == 0:
            return [Token('Division by zero error!', 'error')]
        tokens = replace_tokens(index - 1, index + 1, Token(tokens[index - 1].value // tokens[index + 1].value, 'number'), tokens)
    return tokens


def replace_tokens(begin, end, replacement, tokens):
    return tokens[:begin] + [replacement] + tokens[end + 1:]

example = '8 / 2 * (2 + (2 - 2)) * 3'
lexed = lex(example)
print(parse(lexed).value)