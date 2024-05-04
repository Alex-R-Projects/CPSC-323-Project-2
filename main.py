class Parser:
    def __init__(self):
        # We used a nested dictionary to define the parsing table
        self.table = {
            0: {'id': 'S5', '(': 'S4', 'E': 1, 'T': 2, 'F': 3},
            1: {'+': 'S6', '$': 'acc'},
            2: {'+': 'R2', '*': 'S7', ')': 'R2', '$': 'R2'},
            3: {'+': 'R4', '*': 'R4', ')': 'R4', '$': 'R4'},
            4: {'id': 'S5', '(': 'S4', 'E': 8, 'T': 2, 'F': 3},
            5: {'+': 'R6', '*': 'R6', ')': 'R6', '$': 'R6'},
            6: {'id': 'S5', '(': 'S4', 'T': 9, 'F': 3},
            7: {'id': 'S5', '(': 'S4', 'F': 10},
            8: {'+': 'S6', ')': 'S11'},
            9: {'+': 'R1', '*': 'S7', ')': 'R1', '$': 'R1'},
            10: {'+': 'R3', '*': 'R3', ')': 'R3', '$': 'R3'},
            11: {'+': 'R5', '*': 'R5', ')': 'R5', '$': 'R5'}
        }
        self.stack = [0]  # Initialize stack with state 0

    def parse(self, tokens):
        i = 0
        tokens.append('$')  # Ensure the end of the input is marked by a $
        while i < len(tokens): # Iterating through the tokens from the input strings
            current_state = self.stack[-1] # Looking at the top of the stack, (-1 does that) to determine the current state
            token = tokens[i] # whatever token we are processing
            action = self.table[current_state].get(token, None) # Gets the action dependent on the state and token

            if action is None: # If theres no action in the parsing table --> print out action on {state number}
                print(f"Error at state {current_state} with input '{token}'. No action defined.")
                return "String is not accepted"
            # Formatting for printing the stack, input string, and actions
            print(f"Step: {len(self.stack)//2}, Stack: {self.stack}, Input: {' '.join(tokens[i:])}, Action: {action}")


            if action.startswith('S'): # This conditional handles shifts
                new_state = int(action[1:]) # Will decide which state to shift to
                self.stack.extend([token, new_state]) # pushes the a token from the input string/state on to the stack
                i += 1 # Moves the state by 1
            elif action.startswith('R'): # Condition to handle reductions
                self.apply_reduction(action) # moves to applying reductions method
            elif action == 'acc': # outputs string is accepted once, condition is true
                return "String is accepted"

        return "String is not accepted"

    def apply_reduction(self, action):
        # This method handles different reduction rules based on the grammar specified in the action.
        # Each rule specifies which elements to pop from the stack and what to push back.

 
        if action == 'R1':  # E -> E + T
            # Pop T, +, E
            for _ in range(6):
                self.stack.pop()
            left_state = self.stack[-1]
            self.stack.append('E')
            next_state = self.table[left_state].get('E')
            if next_state is None:
                print(f"Error: No transition defined for 'E' in state {left_state}") # This statement is for error checking
                return
            self.stack.append(next_state)

        elif action == 'R2':  # E -> T
            # Pop T
            for _ in range(2):
                self.stack.pop()
            left_state = self.stack[-1]
            self.stack.append('E')
            next_state = self.table[left_state].get('E')
            if next_state is None:
                print(f"Error: No transition defined for 'E' in state {left_state}")
                return
            self.stack.append(next_state)

        elif action == 'R3':  # T -> T * F
            # Pop F, *, T
            for _ in range(6):
                self.stack.pop()
            left_state = self.stack[-1]
            self.stack.append('T')
            next_state = self.table[left_state].get('T')
            if next_state is None:
                print(f"Error: No transition defined for 'T' in state {left_state}")
                return
            self.stack.append(next_state)

        elif action == 'R4':  # T -> F
            # Pop F
            for _ in range(2):
                self.stack.pop()
            left_state = self.stack[-1]
            self.stack.append('T')
            next_state = self.table[left_state].get('T')
            if next_state is None:
                print(f"Error: No transition defined for 'T' in state {left_state}")
                return
            self.stack.append(next_state)

        elif action == 'R5':  # F -> (E)
            # Pop ), E, (
            for _ in range(6):
                self.stack.pop()
            left_state = self.stack[-1]
            self.stack.append('F')
            next_state = self.table[left_state].get('F')
            if next_state is None:
                print(f"Error: No transition defined for 'F' in state {left_state}")
                return
            self.stack.append(next_state)

        elif action == 'R6':  # F -> id
            # Pop id and its state
            for _ in range(2):
                self.stack.pop()
            if not self.stack:
                print("Error: Stack is empty after popping 'id'.")
                return
            left_state = self.stack[-1]
            self.stack.append('F')
            next_state = self.table[left_state].get('F')
            if next_state is None:
                print(f"Error: No transition defined for 'F' in state {left_state}")
                return
            self.stack.append(next_state)



def main():
    parser = Parser()
    input_strings = ["(id+id)*id", "id*id", "(id*)"] # Put the input strings in a list to handle all 3 at once

    for input_string in input_strings: # Iterating through each index, and parsing each inputstring
        print(f"Processing: {input_string}")
        tokens = input_string.replace("+", " + ").replace("*", " * ").replace("(", " ( ").replace(")", " ) ").split() 
        # Tokenizing the input makesit easier for the parser to read, especially for 'id'; during the development it would read as 'i'
        result = parser.parse(tokens)
        print(result) # output the results
        parser.stack = [0]  # Reset the stack for the next input


if __name__ == "__main__":
    main()