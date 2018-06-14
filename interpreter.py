(INT, PLUS, MINUS, MULT, DIV, LPAREN, RPAREN, NEWL,
    ID, ASSIGN, CALL, PLEASE, THANKYOU, HELLO, GOODBYE, EOF) = (
    'INT', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAREN', 'RPAREN', 'NEWL',
    'ID', 'ASSIGN', 'call', 'please', 'thankyou', 'hello', 'goodbye', 'EOF')


class Token():
    def __init__(self, type, value):
        self.type = type # ie INT, PLUS, EOF
        self.value = value # ie 1, 3, +, None

    def __str__(self): # ex "Token(INT, 3)
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


RESERVED_KEYWORDS = {
    'please': Token('please', 'please'),
    'thankyou': Token('thankyou', 'thankyou'),
    'hello': Token('hello', 'hello'),
    'goodbye': Token('goodbye', 'goodbye'),
    'call': Token('call', 'call'),
}


class Lexer():
    def __init__(self, text):
        self.text = text # string input to parse
        self.pos = 0 # index in string
        self.curr_char = self.text[self.pos]

    def error(self):
        raise Exception("impolite programming, fix your character")

    def peek(self): # check next char without advancing
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None  # EOF
        else:
            return self.text[peek_pos]

    def advance(self): # move to next char
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.curr_char = None  # EOF
        else:
            self.curr_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.curr_char is not None and self.curr_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.curr_char is not None and self.curr_char.isdigit():
            result += self.curr_char
            self.advance()
        return int(result)

    def _id(self): # handle identifiers and reserved keywords
        result = ''
        while self.curr_char is not None and self.curr_char.isalnum():
            result += self.curr_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self):
        while self.curr_char is not None: # make sure not EOF
            if self.curr_char.isspace():
                self.skip_whitespace()
                continue

            if self.curr_char.isdigit():
                return Token(INT, self.integer())

            if self.curr_char.isalpha():
                return self._id()

            if self.curr_char == ':':
                self.advance()
                return Token(ASSIGN, ':')

            if self.curr_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.curr_char == "-":
                self.advance()
                return Token(MINUS, "-")

            if self.curr_char == "*":
                self.advance()
                return Token(MULT, "*")

            if self.curr_char == "/":
                self.advance()
                return Token(DIV, "/")

            if self.curr_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.curr_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)


# classes for AST nodes
class AST():
    pass


class BinOp(AST): # binary operation node
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST): # unary operation node
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

class Assign(AST): # variable
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser():
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = self.lexer.get_next_token() # first token

    def error(self):
        raise Exception('impolite programming - fix your syntax')

    def eat(self, token_type):
        # ensure current token is expected token type
        # if so, progress
        if token_type == self.curr_token.type:
            self.curr_token = self.lexer.get_next_token()
        else:
            print(self.curr_token, token_type)
            self.error()

    def empty(self): # empty statement
        return NoOp()

    def program(self): # check beginning and end of program
        self.eat(HELLO)
        commands = []
        while self.curr_token.value != GOODBYE and self.curr_token.type != None: # iterate through commands
            commands.append(self.command())
        self.eat(GOODBYE)
        return commands

    def command(self): # check beginning and end of each command
        self.eat(PLEASE)
        if self.curr_token.type==CALL:
            token = self.assignment()
        else:
            token = self.expr()
        self.eat(THANKYOU)
        return token

    def assignment(self):
        self.eat(CALL)
        left = self.variable()
        token = self.curr_token

        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.curr_token)
        self.eat(ID)
        return node


    def factor(self):
        token = self.curr_token
        if token.type == INT:
            self.eat(INT)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        node = self.factor()
        while self.curr_token.type in (MULT, DIV):
            op = self.curr_token
            if op.type == MULT:
                self.eat(MULT)
            elif op.type == DIV:
                self.eat(DIV)
            node = BinOp(left=node, op=op, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.curr_token.type in (PLUS, MINUS):
            op = self.curr_token
            if op.type == PLUS:
                self.eat(PLUS)
            elif op.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=op, right=self.term())
        return node

    def parse(self):
        return self.program()


class NodeVisitor():
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MULT:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_UnaryOp(self, node):
        if node.op.type == PLUS:
            return +self.visit(node.expr)
        elif node.op.type == MINUS:
            return -self.visit(node.expr)

    def visit_Num(self, node):
        return node.value

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val


    def visit_NoneType(self, node):
        pass

    def interpret(self):
        trees = self.parser.parse()
        parsed = []
        for tree in trees:
            parsed.append(self.visit(tree))
        return parsed


def main():
    import sys
    text = open(sys.argv[1], 'r').read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    for r in result:
        if r is not None:
            print(r)


if __name__ == '__main__':
    main()




