class Parser:
    def __init__(self):
        # Define the complete parsing table using nested dictionaries
        self.table = {
            0: {'id': 'S5', '(': 'S4', 'E': 1, 'T': 2, 'F': 3},
            1: {'+': 'S6', '$': 'acc'},
            2: {'+': 'R2', '*': 'S7', ')': 'R2', '$': 'R2'},
            3: {'+': 'R4', '*': 'R4', ')': 'R4', '$': 'R4'},
            4: {'id': 'S5', '(': 'S4', 'E': 8, 'T': 2, 'F': 3},
            5: {'+': 'R6', '*': 'R6', ')': 'R6', '$': 'R6'},
            6: {'id': 'S5', '(': 'S4', 'E': 9, 'T': 3},
            7: {'id': 'S5', '(': 'S4', 'F': 10},
            8: {'+': 'S6', ')': 'S11'},
            9: {'+': 'R1', '*': 'S7', ')': 'R1', '$': 'R1'},
            10: {'+': 'R3', '*': 'R3', ')': 'R3', '$': 'R3'},
            11: {'+': 'R5', '*': 'R5', ')': 'R5', '$': 'R5'}
        }
        self.stack = [0]  # Initialize stack with state 0

    def parse(self, tokens):
        i = 0
        tokens.append('$')  # Ensure the end of the input is marked
        while i < len(tokens):
            current_state = self.stack[-1]
            token = tokens[i]
            action = self.table[current_state].get(token, None)

            if action is None:
                print(f"Error at state {current_state} with input '{token}'. No action defined.")
                return "String is not accepted"

            print(f"Step: {len(self.stack)//2}, Stack: {self.stack}, Input: {' '.join(tokens[i:])}, Action: {action}")

            if action.startswith('S'):
                new_state = int(action[1:])
                self.stack.extend([token, new_state])
                i += 1
            elif action.startswith('R'):
                # This needs to be fleshed out based on specific grammar rules
                self.apply_reduction(action)
            elif action == 'acc':
                return "String is accepted"

        return "String is not accepted"

    def apply_reduction(self, action):
        if action == 'R1':  # E → E + T
            # Pop T, +, E
            for _ in range(3):
                self.stack.pop()  # Pop state and symbol alternately
            left_E_state = self.stack[-1]  # Check the state after popping
            self.stack.append('E')
            self.stack.append(self.table[left_E_state]['E'])

        elif action == 'R2':  # E → T
            # Pop T
            self.stack.pop()  # Pop state
            self.stack.pop()  # Pop T
            T_state = self.stack[-1]
            self.stack.append('E')
            self.stack.append(self.table[T_state]['E'])

        elif action == 'R3':  # T → T * F
            # Pop F, *, T
            for _ in range(3):
                self.stack.pop()  # Pop state and symbol alternately
            left_T_state = self.stack[-1]  # Check the state after popping
            self.stack.append('T')
            self.stack.append(self.table[left_T_state]['T'])

        elif action == 'R4':  # T → F
            # Pop F
            self.stack.pop()  # Pop state
            self.stack.pop()  # Pop F
            F_state = self.stack[-1]
            self.stack.append('T')
            self.stack.append(self.table[F_state]['T'])

        elif action == 'R5':  # F → (E)
            # Pop ), E, (
            self.stack.pop()  # Pop state
            self.stack.pop()  # Pop )
            self.stack.pop()  # Pop state
            self.stack.pop()  # Pop E
            self.stack.pop()  # Pop state
            self.stack.pop()  # Pop (
            E_state = self.stack[-1]
            self.stack.append('F')
            self.stack.append(self.table[E_state]['F'])

        elif action == 'R6':  # F → id
            # Pop id
            self.stack.pop()  # Pop state
            self.stack.pop()  # Pop id
            id_state = self.stack[-1]
            self.stack.append('F')
            self.stack.append(self.table[id_state]['F'])


def main():
    parser = Parser()
    input_strings = ["(id+id)*id", "id*id", "(id*)"]

    for input_string in input_strings:
        print(f"Processing: {input_string}")
        tokens = input_string.replace("+", " + ").replace("*", " * ").replace("(", " ( ").replace(")", " ) ").split()
        result = parser.parse(tokens)
        print(result)
        parser.stack = [0]  # Reset the stack for the next input


if __name__ == "__main__":
    main()