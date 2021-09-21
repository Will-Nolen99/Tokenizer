import re



class Tokenizer:

    reserved_words = ["program",
                      "begin",
                      "end",
                      "int",
                      "if",
                      "then",
                      "else",
                      "while",
                      "loop",
                      "read",
                      "write"
                      ]

    symbols = [";", ",", "=", "!", "[", "]",
               "&&", "||", "(", ")", "+", "-",
               "*", "!=", "==", "<", ">", "<=",
               ">="
               ]

    END_OF_FILE = "EOF"
    EOF_TOKEN_NUMBER = 33

    IDENTIFIER_REGEX = "\A[A-Z]+[0-9]*\Z"  # This does not account for length of identifier.
    INTEGER_REGEX = "\A[\d]{1,8}\Z"    # This does length testing



    # Create a tokenizer with source as the file path to the source code.
    def __init__(self, source):
        self.source = source
        self.token_stream = []

    # read source file a single line at a time.
    # yields a string with the contents of an entire line
    # if file is empty, yields "EOF"
    def __read_line(self):
        # return each line for processing
        for line in open(self.source, "r"):
            yield line.strip()

        yield Tokenizer.END_OF_FILE


    def tokenize(self):

        line_reader = self.__read_line()
        current_line = next(line_reader)

        while current_line != "EOF":

            self.__process_line(current_line)

            current_line = next(line_reader)

        line_reader.close()

        print("Done Processing!")
        print("Final token Stream: ")
        print(self.token_stream)


    def __process_line(self, line):

        # break into tokens by whitespace for further processing
        token_candidates = line.split(" ")
        for token in token_candidates:
            print(token)

            # reserved word check
            if token in Tokenizer.reserved_words:
                self.token_stream.append(token)
                print("Added")

            # special char check
            elif token in Tokenizer.symbols:
                self.token_stream.append(token)
                print("Added")

            # Identifier check
            elif re.search(Tokenizer.IDENTIFIER_REGEX, token) is not None and len(token) <= 8:
                self.token_stream.append(token)
                print("Added")

            # integer check
            elif re.search(Tokenizer.INTEGER_REGEX, token) is not None:
                self.token_stream.append(token)
                print("Added")






    def get_token(self):
        pass

    def skip_token(self):
        pass

    def int_val(self):
        pass

    def id_name(self):
        pass





tk = Tokenizer("core1.txt")
tk.tokenize()

