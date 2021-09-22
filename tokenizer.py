import re
import sys


class Tokenizer:

    messages = {"candidate": lambda token: print(f"Current token candidate: {token}"),
                "word_id": lambda token: print(f"Added token id: {Tokenizer.reserved_words.index(token)+1}\n\n"),
                "symbol_id": lambda token: print(f"Added token id: {Tokenizer.symbols.index(token)+12}\n\n"),
                "id": lambda: print("Added token id: 32\n\n"),
                "int": lambda: print("Added token id: 31\n\n"),
                "odd": lambda line: print(f"Odd token candidate encountered: {line}\n"),
                "check": lambda symbol: print(f"Checking if {symbol} starts token candidate"),
                "id_f": lambda id: print(f"Identifier found: {id}\n\n"),
                "int_f": lambda id: print(f"Integer found: {id}\n\n"),
                "unknown_line": lambda line_number: print(f"Unknown Token encountered on line: {line_number}"),
                "unknown": lambda symbol: print(f"{symbol} is unrecognized\n"),
                "EOF": lambda: print("EOF found!\nAdded token id: 33\n")
                }



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
    def __init__(self, source, verbose=False):

        self.source = source
        self.token_stream_literal = []
        self.token_stream = []
        self.verbose = verbose

    def __message(self, message_type, value=None):

        if self.verbose:
            if value is None:
                Tokenizer.messages[message_type]()
            else:
                Tokenizer.messages[message_type](value)
        elif message_type == "unknown_line" or message_type == "unknown":
            Tokenizer.messages[message_type](value)

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
        num = 1

        while current_line != "EOF":

            self.__process_line(current_line, num)

            current_line = next(line_reader)
            num += 1

        line_reader.close()

        self.__message("EOF")
        self.token_stream_literal.append("EOF")
        self.token_stream.append(33)



        if self.verbose:
            print("Done Processing!")
            print("Final token Stream: ")
            print(self.token_stream_literal)
            print(self.token_stream)


    def __process_line(self, line, line_number):

        # break into tokens by whitespace for further processing
        token_candidates = line.split()
        for token in token_candidates:

            self.__message("candidate", token)

            # reserved word check
            if token in Tokenizer.reserved_words:
                self.token_stream_literal.append(token)
                self.token_stream.append(Tokenizer.reserved_words.index(token) + 1)
                self.__message("word_id", token)


            # special char check
            elif token in Tokenizer.symbols:
                self.token_stream_literal.append(token)
                self.token_stream.append(Tokenizer.symbols.index(token) + 12)
                self.__message("symbol_id", token)

            # Identifier check
            elif re.search(Tokenizer.IDENTIFIER_REGEX, token) is not None and len(token) <= 8:
                self.token_stream_literal.append(token)
                self.token_stream.append(32)
                self.__message("id")

            # integer check
            elif re.search(Tokenizer.INTEGER_REGEX, token) is not None:
                self.token_stream_literal.append(token)
                self.token_stream.append(31)
                self.__message("int")


            # given string is not a direct token. It maybe multiple tokens with no whitespace between    
            else:
                self.__break_into_tokens(token, line_number)


    # breaks apart a string that can possibly contain multiple tokens into its componenet parts
    def __break_into_tokens(self, token_candidate, line_number):

        # order of check is the reverse of Tokenizer.symbols
        # followed by identifier followed by integer


        line = token_candidate.strip()  # this is added to reduce unwanted reference side effects. It may not be needed

        token_found = True
        while len(line) > 0 and token_found:
           
            token_found = False
            self.__message("odd", line)

            # use each symbol as reg ex
            for symbol in reversed(Tokenizer.symbols):
                self.__message("check", symbol)

                # By add \A regex will only match if at the begining of the token candidate
                symbol_regex = "\A" + re.escape(symbol)

                # symbol check
                if re.search(symbol_regex, line) is not None:
                    # Token is in the current string
                    self.token_stream_literal.append(symbol)
                    self.token_stream.append(Tokenizer.symbols.index(symbol) + 12)
                    self.__message("symbol_id", symbol)
                    token_found = True

                    line = line[len(symbol):]

            # Since there is no longer a guarantee that this identifier is followed by whitespace
            # The endline regex portion must be removed
            id_regex = Tokenizer.IDENTIFIER_REGEX[:-2]
            int_regex = Tokenizer.INTEGER_REGEX[:-2]



            id_match = re.search(id_regex, line)
            if id_match is not None:
                end_idx = id_match.end()

                self.__message("id_f", line[:end_idx])
                token_found = True

                self.token_stream_literal.append(line[:end_idx])
                self.token_stream.append(32)

                line = line[end_idx:]

            id_match = re.search(int_regex, line)
            if id_match is not None:
                end_idx = id_match.end()

                self.__message("int_f", line[:end_idx])
                token_found = True

                self.token_stream_literal.append(line[:end_idx])
                self.token_stream.append(31)
                line = line[end_idx:]


        if len(line) > 0:
            # print error message if token is not recognized and exit process

            self.__message("unknown_line", line_number)
            self.__message("unknown", line)
            exit()


    def get_token(self):
        return self.token_stream[0]

    def skip_token(self):
        self.token_stream_literal.pop(0)
        self.token_stream.pop(0)

    def int_val(self):
        return self.token_stream_literal[0]

    def id_name(self):
        return self.token_stream_literal[0]




def main():
    file = sys.argv[1] if len(sys.argv) > 1 else input("Enter a file path: ")

    if len(sys.argv) > 2 and "-v" == sys.argv[2]:
        tokenizer = Tokenizer(file, True)
    else:
        tokenizer = Tokenizer(file)

    tokenizer.tokenize()


    token = tokenizer.get_token()
    print(token)

    while token != 33:
        tokenizer.skip_token()
        token = tokenizer.get_token()
        print(token)



if __name__ == "__main__":
    main()




