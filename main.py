# CPSC 323

# Project #2 Stack implementation for a parser
   # We are going to explicitly write out the parsing table 
    ######## Production Rules ############ 
    # (1) E→E + T
    # (2) E→ T
    # (3) T→ T * F
    # (4) T→ F
    # (5) F→ (E)
    # (6) F→ id
    ######################################

def parser(input_string):

    parsing_table = { # This is a multi dimensional dictionary, where the keys (the numbers) are keys to other mini dictionaries
        # The numbers represent that states

    0: {"id": ("Shift", 5), "+": ("Shift", 4), "*": ("Shift", 1), "(": ("Shift", 2), ")": ("Shift", 3)},
    1: {"+": ("Reduce", ("E", "T")), "*": ("Reduce", ("E", "T")), ")": ("Reduce", ("E", "T")), "$": ("Accept", "")},
    2: {"id": ("Shift", 5), "+": ("Shift", 4), "*": ("Shift", 6), "(": ("Shift", 7), ")": ("Shift", 3)},
    3: {"+": ("Reduce", ("F", "id")), "*": ("Reduce", ("F", "id")), ")": ("Reduce", ("F", "id")), "$": ("Reduce", ("F", "id"))},
    4: {"id": ("Shift", 5), "+": ("Shift", 4), "*": ("Shift", 6), "(": ("Shift", 8), ")": ("Shift", 3)},
    5: {"+": ("Reduce", ("E", "T")), "*": ("Shift", 1), ")": ("Reduce", ("E", "T")), "$": ("Reduce", ("E", "T"))},
    6: {"id": ("Shift", 5), "+": ("Shift", 4), "*": ("Shift", 6), "(": ("Shift", 7), ")": ("Shift", 9)},
    7: {"id": ("Shift", 5), "+": ("Shift", 4), "*": ("Shift", 6), "(": ("Shift", 8), ")": ("Shift", 3)},
    8: {"+": ("Reduce", ("E", "E + T")), "*": ("Shift", 1), ")": ("Reduce", ("E", "E + T")), "$": ("Reduce", ("E", "E + T"))},
    9: {"+": ("Reduce", ("F", "(E)")), "*": ("Reduce", ("F", "(E)")), ")": ("Reduce", ("F", "(E)")), "$": ("Reduce", ("F", "(E)"))},
    10: {"+": ("Reduce", ("T", "T * F")), "*": ("Reduce", ("T", "T * F")), ")": ("Reduce", ("T", "T * F")), "$": ("Reduce", ("T", "T * F"))},
    11: {"+": ("Reduce", ("T", "F")), "*": ("Reduce", ("T", "F")), ")": ("Reduce", ("T", "F")), "$": ("Reduce", ("T", "F"))}
}

    

    input_mapping = {
        "id": "id",
        "+": "+",
        "*": "*",
        "(": "(",
        ")": ")",
        "$": "$"
    }
    
    input_index = 0
    stack = [0]
    
    while True:
        state = stack[-1]
        if input_index < len(input_string):
            symbol = input_string[input_index]
            if symbol in input_mapping:
                symbol = input_mapping[symbol]  # Map input symbol to the corresponding symbol in parsing table
            else:
                return "The input string is invalid"  # Return error for unrecognized symbols
        else:
            symbol = '$'

        if symbol in parsing_table[state]:
            action, goto = parsing_table[state][symbol]
            if action == "Shift":
                stack.append(symbol)
                stack.append(goto)
                input_index += 1
            elif action == "Reduce":
                production_rule = goto
                num_pop = 2 * len(production_rule[1])
                stack = stack[:-num_pop]
                state = stack[-1]
                stack.append(production_rule[0])
                stack.append(parsing_table[state][production_rule[0]][1])
            else:
                return "The input string is invalid"

            if action == "Accept":
                return "The input string is valid"
        else:
            return "The input string is invalid"


def main():
    input_strings = ["(id+id)*id$","id*id$","(id*)$"]

    for input_string in input_strings:
        print("Input string:", input_string)
        print(parser(input_string))


if __name__ == "__main__":
    main()