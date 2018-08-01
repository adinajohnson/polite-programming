import unittest
import interpret


class Tests(unittest.TestCase):
    snippets = (
                    # basics
                    ("hello goodbye", []),
                    ("hello please thankyou goodbye", []),

                    # print statements
                    ("hello please say 1 thankyou goodbye", [1]),

                    # arithmetic
                    ("hello please say 1+2 thankyou goodbye", [3]),
                    ("hello please say 1*2 thankyou goodbye", [2]),
                    ("hello please say 2-1 thankyou goodbye", [1]),
                    ("hello please say 6/3 thankyou goodbye", [2]),

                    # unary operations
                    ("hello please say 1+-1 thankyou goodbye", [0]),

                    # parentheses

                    # booleans
                    ("hello please say 1+2 is 3 thankyou goodbye", [True]),
                    ("hello please say 1+2 is 4 thankyou goodbye", [False]),

                    # if statements

                    # while loops

    )


    def test_snippets(self):
        for input, output in self.snippets:
            lexer = interpret.Lexer(input)
            parser = interpret.Parser(lexer)
            interpreter = interpret.Interpreter(parser)
            result = interpreter.interpret()
            self.assertEqual(result, output)

    def test_errors(self):
        # lexer unknown character error
        lexer = interpret.Lexer("<")
        def LexerErrorTest():
            lexer.get_next_token()
        self.assertRaises(Exception, LexerErrorTest)


if __name__ == '__main__':
    unittest.main()