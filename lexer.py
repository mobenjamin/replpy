def lex_input(input_string):
    token = ""
    output_list = []
    i = 0
    while i < len(input_string):
        char = input_string[i]
        if char == "\"":
            i += 1
            token = char
            while i < len(input_string) and input_string[i] != "\"":
                token += input_string[i]
                i += 1
            token += char
            output_list.append(token)
            token = ""

        elif char == "(" or char == ")" or char == "'":  # Add more if needed
            if token != "":
                output_list.append(token)
                token = ""
            output_list.append(char)

        elif char == " " or char == "\n" or char == "\t" or char == "\r":
            if token != "":
                output_list.append(token)
                token = ""

        else:
            token += char

        i += 1
    if token != "":
        output_list.append(token)

    return output_list
