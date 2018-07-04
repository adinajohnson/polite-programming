# token class: represents individual segments of the input
class Token:
    def __init__(self, type, val):
        self.type = type # ie INT, VAR, PLUS
        self.val = val # ie 5, a, +

    def __str__(self):
        return "Token type: " + self.type + ", value: " + self.val


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.curr_ch = text[0]
        self.keywords = { # saved keywords with special meaning in the language
                    "hello":Token('hello', 'hello'),
                    "goodbye":Token('goodbye', 'goodbye'),
                    "please": Token('please', 'please'),
                    "thankyou": Token('thankyou', 'thankyou'),
                    "call": Token('call', 'call'),
                    "is": Token('is', 'is'),
                    "isnt": Token('isnt', 'isnt'),
                    "perchance": Token('perchance', 'perchance'),
                    "naturally": Token('naturally', 'naturally'),
        }

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text): # check for EOF
            self.curr_ch = None
        else:
            self.curr_ch = self.text[self.pos]

    # raised when encountering an unrecognized character
    def error(self):
        raise Exception("impolite programming, fix your character", self.curr_ch)

    def get_next_token(self):
        while self.curr_ch is not None:
            if self.curr_ch.isspace():
                self.skip_whitespace()
                continue
            if self.curr_ch.isdigit():
                return Token("INT", self.integer())
            if self.curr_ch.isalpha():
                return self.alpha()
            if self.curr_ch == '+':
                self.advance()
                return Token("PLUS", self.curr_ch)
            if self.curr_ch == '-':
                self.advance()
                return Token("MINUS", self.curr_ch)
            if self.curr_ch == '*':
                self.advance()
                return Token("MULT", self.curr_ch)
            if self.curr_ch == '/':
                self.advance()
                return Token("DIV", self.curr_ch)
            if self.curr_ch == '(':
                self.advance()
                return Token("LPAREN", self.curr_ch)
            if self.curr_ch == ')':
                self.advance()
                return Token("RPAREN", self.curr_ch)
            self.error()
        return Token("EOF", None)

    def skip_whitespace(self):
        while self.curr_ch is not None and self.curr_ch.isspace():
            self.advance()

    def integer(self):
        num = ""
        while self.curr_ch is not None and self.curr_ch.isdigit():
            num += self.curr_ch
            self.advance()
        return int(num)

    def alpha(self):
        word = ""
        while self.curr_ch is not None and self.curr_ch.isalpha():
            word += self.curr_ch
            self.advance()
        if word in self.keywords:
            return self.keywords[word]
        else:
            return Token("VAR", word)


# node classes for use in AST
class Num:
    def __init__(self, token):
        self.token = token
        self.val = token.val


class BinOp: # binary operation
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class UnaryOp: # unary operation node
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class BoolOp:
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Assign: # to assign a variable
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Var: # referencing a variable
    def __init__(self, token):
        self.token = token
        self.val = token.val

class Opt:
    def __init__(self, perchance, naturally):
        self.perchance = perchance
        self.naturally = naturally

class NoOp:
    pass


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('impolite programming - fix your syntax')

    # check whether next token is the expected type, then advance
    def consume(self, expected):
        if self.curr_token.type == expected:
            self.curr_token = self.lexer.get_next_token()
        else:
            print("Expected", expected, "got", self.curr_token.type)
            self.error()

    # check beginning and end of program for hello and goodbye
    # then run through command lines in program
    def program(self):
        self.consume("hello")
        commands = []
        while self.curr_token.val != "goodbye" and self.curr_token.type != None: # iterate through commands
            commands.append(self.command())
        self.consume("goodbye")
        return commands

    # check beginning and end of each command for hello and goodbye
    def command(self):
        self.consume("please")
        node = NoOp() # default is empty operation
        if self.curr_token.type=="call": # check is command is assigning a variable
            node = self.assignment()
        elif self.curr_token.type=="perchance": # check for if statement
            node = self.opt()
        if self.curr_token.type != "thankyou":
            node = self.bool() # can handle any other type of command
        self.consume("thankyou")
        return node

    def opt(self):
        self.consume("perchance")
        perchance = self.bool()
        self.consume("naturally")
        naturally = []
        while self.curr_token.type=="please":
            self.consume("please")
            if self.curr_token.type=="call": # check is command is assigning a variable
                naturally.append(self.assignment())
            elif self.curr_token.type == "perchance":  # check for if statement
                naturally.append(self.opt())
            else:
                naturally.append(self.bool())
            self.consume("thankyou")
        return Opt(perchance, naturally)

    def assignment(self): # assigning a variable
        self.consume("call")
        left = self.curr_token
        self.consume("VAR")
        right = self.bool()
        node = Assign(left, right)
        return node

    def factor(self):
        token = self.curr_token
        if token.type == "INT":
            self.consume("INT")
            return Num(token)
        elif token.type == "VAR":
            self.consume("VAR")
            return Var(token)
        elif token.type == "LPAREN":
            self.consume("LPAREN")
            node = self.bool()
            self.consume("RPAREN")
            return node
        elif token.type == "PLUS":
            self.consume("PLUS")
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == "MINUS":
            self.consume("MINUS")
            node = UnaryOp(token, self.factor())
            return node
        else:
            node = Var(self.curr_token)
            return node

    def term(self):
        node = self.factor()
        while self.curr_token.type in ("MULT", "DIV"):
            op = self.curr_token
            if op.type == "MULT":
                self.consume("MULT")
            elif op.type == "DIV":
                self.consume("DIV")
            node = BinOp(node, op, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.curr_token.type in ("PLUS", "MINUS"):
            op = self.curr_token
            if op.type == "PLUS":
                self.consume("PLUS")
            elif op.type == "MINUS":
                self.consume("MINUS")
            node = BinOp(node, op, self.term())
        return node

    def bool(self):
        node = self.expr()
        while self.curr_token.type in ("is", "isnt"):
            op = self.curr_token
            if op.type == "is":
                self.consume("is")
            elif op.type == "isnt":
                self.consume("isnt")
                node = BoolOp(node, op, self.term())
            node = BoolOp(node, op, self.term())
        return node

    def parse(self):
        return self.program()


class Interpreter:

    def __init__(self, parser):
        self.parser = parser
        self.vars = {} # keep track of values assigned to vars

    # call visit function for specific node type
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    # if visit function for node type can't be found
    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_BinOp(self, node):
        if node.op.type == "PLUS":
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == "MINUS":
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == "MULT":
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == "DIV":
            return self.visit(node.left) / self.visit(node.right)

    def visit_UnaryOp(self, node):
        if node.op.type == "PLUS":
            return +self.visit(node.expr)
        elif node.op.type == "MINUS":
            return -self.visit(node.expr)

    def visit_BoolOp(self, node):
        if node.op.type == "is":
            return self.visit(node.left) is self.visit(node.right)
        elif node.op.type == "isnt":
            return self.visit(node.left) is not self.visit(node.right)

    def visit_Num(self, node):
        return node.val

    def visit_Assign(self, node):
        self.vars[node.left.val] = self.visit(node.right)

    def visit_Var(self, node):
        return self.vars[node.val]

    def visit_Opt(self, node):
        if self.visit(node.perchance):
            for item in node.naturally:
                self.visit(item)

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        trees = self.parser.parse()
        parsed = []
        for tree in trees:
            result = self.visit(tree)
            if result is not None:
                parsed.append(result)
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
