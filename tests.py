import unittest
import interpret


class Tests(unittest.TestCase):
    working_snippets = (
                    # basics
                    ("hello goodbye", []),
                    ("hello please thankyou goodbye", []),

                    # print statements
                    ("hello please say 1 thankyou goodbye", [1]),
                    ("hello please say \"hi\" thankyou goodbye", ["hi"]),

                    # comments


                    # arithmetic
                    ("hello please say 1+2 thankyou goodbye", [3]),
                    ("hello please say 1*2 thankyou goodbye", [2]),
                    ("hello please say 2-1 thankyou goodbye", [1]),
                    ("hello please say 6/3 thankyou goodbye", [2]),

                    # unary operations
                    ("hello please say 1+-1 thankyou goodbye", [0]),

                    # parentheses
                    ("hello please say 7 + 3 * (10 / (12 / (3 + 1) - 1)) thankyou goodbye", [22]),

                    # booleans
                    ("hello please say 1+2 is 3 thankyou goodbye", [True]),
                    ("hello please say 1+2 is 4 thankyou goodbye", [False]),

                    # if statements
                    ("hello please perchance 1+2 is 3 naturally please say 3 thankyou thankyou goodbye", [3]),
                    ("hello please perchance 1+2 is 4 naturally please say 3 thankyou thankyou goodbye", []),

                    # while loops
                    ("hello please call a 1 thankyou please whilst a isnt 3 naturally please call a a+1 thankyou thankyou please say a thankyou goodbye", [3]),
    )


    def test_snippets(self):
        for input, output in self.working_snippets:
            lexer = interpret.Lexer(input)
            parser = interpret.Parser(lexer)
            interpreter = interpret.Interpreter(parser)
            result = interpreter.interpret()
            self.assertEqual(result, output)

    def test_lexer_errors(self):
        # lexer unknown character error
        lexer = interpret.Lexer("<")
        def LexerErrorTest():
            lexer.get_next_token()
        self.assertRaises(Exception, LexerErrorTest)

    parser_error_snippets = [
        # basics
        "hello",
        "hello 1+2",
        "hello please 1+2",
        "hello please 1+3 thankyou",

        # print statements
        "hello please say \"hi thankyou goodbye"
        "hello please say \"hi\"\" thankyou goodbye"

        # arithmetic
        "hello please 1+1+ thankyou goodbye",

        # parentheses
        "hello please 1+(1+1 thankyou goodbye",
        "hello please 1+(1+1)) thankyou goodbye",

        # booleans


        # if statements

        # while loops
    ]
    def test_parser_errors_basics(self):
        for command in self.parser_error_snippets:
            lexer = interpret.Lexer(command)
            parser = interpret.Parser(lexer)
            def ParserErrorTest():
                parser.program()
            self.assertRaises(Exception, ParserErrorTest)


if __name__ == '__main__':
    unittest.main()