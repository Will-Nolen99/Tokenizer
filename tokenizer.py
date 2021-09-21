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
        self.token_stream_literal = []
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
        num = 1

        while current_line != "EOF":

            self.__process_line(current_line, num)

            current_line = next(line_reader)
            num += 1

        line_reader.close()

        print("EOF found!")
        print("Added as ID 33")
        self.token_stream_literal.append("EOF")
        self.token_stream.append(33)




        print("Done Processing!")
        print("Final token Stream: ")
        print(self.token_stream_literal)
        print(self.token_stream)


    def __process_line(self, line, line_number):

        # break into tokens by whitespace for further processing
        token_candidates = line.split()
        for token in token_candidates:

            print(f"Current token candidate: {token}")

            # reserved word check
            if token in Tokenizer.reserved_words:
                self.token_stream_literal.append(token)
                self.token_stream.append(Tokenizer.reserved_words.index(token) + 1)
                print("Corresponding token id: ", Tokenizer.reserved_words.index(token) + 1)
                print("Added")

            # special char check
            elif token in Tokenizer.symbols:
                self.token_stream_literal.append(token)
                self.token_stream.append(Tokenizer.symbols.index(token) + 12)
                print("Corresponding token id: ", Tokenizer.symbols.index(token) + 12)
                print("Added")

            # Identifier check
            elif re.search(Tokenizer.IDENTIFIER_REGEX, token) is not None and len(token) <= 8:
                self.token_stream_literal.append(token)
                self.token_stream.append(32)
                print("Corresponding token id: ", 32)
                print("Added")

            # integer check
            elif re.search(Tokenizer.INTEGER_REGEX, token) is not None:
                self.token_stream_literal.append(token)
                self.token_stream.append(31)
                print("Corresponding token id: ", 31)
                print("Added")


            # given string is not a direct token. It maybe multiple tokens with no whitespace between    
            else:




                # print error message if token is not recognized and exit process
                print(f"Unknown Token encountered on line: {line_number}")
                print(f"{token} is unrecognized")
                exit()
            print()



    # breaks apart a string that can possibly contain multiple tokens into its componenet parts
    def __break_into_tokens(self, token_candidate):

        # order of check is the reverse of Tokenizer.symbols
        # followed by identifier followed by integer


        line = token_candidate # this is added to reduce unwanted reference side effects. It may not be needed

        while len(line) > 0:
           

            print("Odd token candidate encountered: ", line)

            # use each symbol as reg ex
            for symbol in reveresed(Tokenizer.symbols):
                print(f"Checking if {symbol} starts token candidate")

                # By add \A regex will only match if at the begining of the token candidate
                symbol_regex = "\A" + symbol

                # symbol check
                if re.search(symbol_regex, line) is not None:
                    # Token is in the current string
                    self.token_stream_literal.append(symbol)
                    self.token_stream.append(Tokenizer.symbols.index(symbol) + 12)

                    print("Corresponding token id: ", Tokenizer.symbols.index(token) + 12)
                    print("Added")

                    line = line[len(symbol):]

            # Since there is no longer a guarantee that this identifier is followed by whitespace
            # The endline regex portion must be removed
            id_regex = Tokenizer.IDENTIFIER_REGEX[:-2]
            int_regex = Tokenizer.INTEGER_REGEX[:-2]

            


                    
                    

                


            #add token to stream

            # recurse



    def get_token(self):
        pass

    def skip_token(self):
        pass

    def int_val(self):
        pass

    def id_name(self):
        pass




def main():

    tk = Tokenizer("core2.txt")
    tk.tokenize()


if __name__ == "__main__":
    main()




