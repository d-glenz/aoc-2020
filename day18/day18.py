import fileinput
import re


def expression1(words):
    a = int(term1(words))
    while words and words[-1] != ')':
        tok = words.pop()
        if tok == '+':
            a += term1(words)
        elif tok == '*':
            a *= term1(words)
        else:
            assert False, "Operator can only be * or +"

    return a


def term1(words):
    tok = words.pop()

    if tok.isnumeric():
        return int(tok)

    if tok == '(':
        val = expression1(words)
        assert words.pop() == ')', 'expected closing paren'
        return val

    assert False, "Term can only be number or expression in parentheses"


def expression2(words):
    """
        <expression> ::= <term> [ "*" <tern> [ "*" <term> ... ] ] 
    """
    a = int(term2(words))
    while words and words[-1] != ')':
        tok = words.pop()
        if tok == '*':
            a *= term2(words)
        else:
            assert False, "Operator can only be *"

    return a


def term2(words):
    """
        <term> ::= <factor> [ "+" <factor> [ "+" <factor> ... ] ] | <factor> "*" <factor>
    """
    a = int(factor2(words))
    while words and words[-1] != ')':
        tok = words.pop()
        if tok == '+':
            a += factor2(words)
        elif tok == '*':  # this is counter-intuitive
            a *= term2(words)
        else:
            assert False, f"Operator can only be + or *"

    return a


def factor2(words):
    """
        <factor> ::= <id> | <number> | "(" <expression> ")"
    """
    if not words:
        return 0

    tok = words.pop()
    if tok.isnumeric():
        return int(tok)

    if tok == '(':
        val = expression2(words)
        assert words.pop() == ')', 'expected closing paren'
        return val

    assert False, "Factor can only ever be 0 (for +), number, or paren"


total = 0
for i, line in enumerate(fileinput.input()):
    result = []
    line = line.strip()
    result = re.findall('\(|\)|\*|\+|\d+', line)
    total += expression2(result[::-1])

print(total)
