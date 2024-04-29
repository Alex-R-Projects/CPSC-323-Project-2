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

# Defining the production rules as a global dictionary 
prod_rules = {
    1: ('E', 'E + T'),
    2: ('E', 'T'),
    3: ('T', 'T * F'),
    4: ('T', 'F'),
    5: ('F', '(E)'),
    6: ('F', 'id')
}

# Defining the parsing table as a global dictionary, where the the states are keys to other dictionaries containing the actions for the parsing table
parsing_table = {
    0: {'id': 'S5', '+': None, '*': 'S4', '(': 'S2', ')': None, '$': None, 'E': 1, 'T': 2, 'F': 3},
    1: {'id': None, '+': 'S6', '*': None, '(': None, ')': None, '$': 'acc', 'E': None, 'T': None, 'F': None},
    2: {'id': None, '+': 'R2', '*': 'S7', '(': None, ')': 'R2', '$': 'R2', 'E': None, 'T': None, 'F': None},
    3: {'id': None, '+': 'R4', '*': 'R4', '(': None, ')': 'R4', '$': 'R4', 'E': None, 'T': None, 'F': None},
    4: {'id': 'S5', '+': None, '*': 'S4', '(': 'S8', ')': None, '$': None, 'E': 8, 'T': 2, 'F': 3},
    5: {'id': None, '+': 'R6', '*': 'R6', '(': None, ')': 'R6', '$': 'R6', 'E': None, 'T': None, 'F': None},
    6: {'id': 'S5', '+': None, '*': 'S4', '(': 'S9', ')': None, '$': None, 'E': None, 'T': 9, 'F': 3},
    7: {'id': 'S5', '+': None, '*': 'S4', '(': 'S8', ')': None, '$': None, 'E': None, 'T': None, 'F': 10},
    8: {'id': 'S5', '+': None, '*': 'S4', '(': 'S11', ')': None, '$': None, 'E': None, 'T': None, 'F': 11},
    9: {'id': None, '+': 'R1', '*': 'S7', '(': None, ')': 'R1', '$': 'R1', 'E': None, 'T': None, 'F': None},
    10: {'id': None, '+': 'R3', '*': 'R3', '(': None, ')': 'R3', '$': 'R3', 'E': None, 'T': None, 'F': None},
    11: {'id': None, '+': 'R5', '*': 'R5', '(': None, ')': 'R5', '$': 'R5', 'E': None, 'T': None, 'F': None}
}

def parser(input_string, parsing_table):
    stack = [0]  # Initialize stack with starting state 0
    input_index = 0  # Initialize input index

    while True:
        state = stack[-1]  # Get the current state from the top of the stack
        symbol = input_string[input_index] if input_index < len(input_string) else '$'  # Get next input symbol

        # Debug prints
        print("Current state:", state)
        print("Parsing table:", parsing_table)

        # Check if state is in parsing table
        if state not in parsing_table:
            print("State", state, "is not in parsing table")
            return "The input string is invalid"

        # Get action from parsing table
        action = parsing_table[state].get(symbol)

        if action is None:  # If no action is defined for the current state and symbol
            return "The input string is invalid"  # Return invalid input

        # Perform the specified action
        if action[0] == 'S':  # Shift action
            stack.append(symbol)  # Push input symbol to stack
            stack.append(action[1])  # Push next state to stack
            input_index += 1  # Move to the next input symbol
        elif action[0] == 'R':  # Reduce action
            # Retrieve production rule index from action
            rule_index = int(action[1:])
            # Pop symbols from stack based on the length of the right-hand side of the production rule
            for _ in range(2 * len(prod_rules[rule_index][1])):
                stack.pop()
            # Get the non-terminal symbol from the left-hand side of the production rule
            non_terminal = prod_rules[rule_index][0]
            # Get the next state from the top of the stack
            state = stack[-1]
            # Push non-terminal symbol to stack
            stack.append(non_terminal)
            # Push the next state based on the non-terminal and current state to stack
            stack.append(parsing_table[state][non_terminal])
        elif action == 'acc':  # Accept action
            return "The input string is valid"  # Return valid input







def main():
    
    # Defining a list for the input strings
    input_strings = ["(id+id)*id$", "id*id$", "(id*)$"]

    for input_string in input_strings: # Iterating through inputs strings to test validity
        print("Input string:", input_string)
        print(parser(input_string, parsing_table))

if __name__ == "__main__":
    main()


