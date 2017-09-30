# coding=utf-8

import environment
import lexer
import schemeobj


def main():
    top_env = environment.Environment.get_default_env()
    while True:
        try:
            input_string = raw_input("λ ")
            ret_val = schemeobj.SchemeObject(lexer.lex_input(input_string)).create_obj().eval(top_env)
            if ret_val is not None:
                ret_val.print_value()
        except KeyboardInterrupt:  # This catches the Ctrl+C and terminates the program
            return


if __name__ == "__main__":
    main()


# TODO List:
# case, set!
