# CPSC-323-Project-2
This program simulates the parsing process of input strings consisting of identifiers, operators, and parentheses according to a given context-free grammar, utilizing a stack-based approach to track the parsing state and outputting whether each input string is accepted or not based on the grammar rules and parsing decisions.

Features:
  - The program parses each string iteratively, processing a list of input strings one by one.

Parsing Initialization: It initializes the parse stack with the start state "0" and starts parsing the input string.
Parsing Loop: The program iterates through the input string character by character.
It checks the current state from the top of the parse stack and the current input symbol.
It consults the parsing table to determine the appropriate action to take (shift, reduce, or accept).
If the action is a shift, it pushes the input symbol and the next state onto the stack and moves to the next character.
If the action is a reduce, it pops symbols and states from the stack according to the production rule's length and pushes the left-hand side nonterminal symbol along with the new state obtained from the LHS onto the stack.
If the action is accept, it indicates that the input string is accepted.
Error Handling: The program includes error handling mechanisms to detect and handle cases where there is no valid action defined for the current state and input symbol.

Output: The program outputs whether each input string is accepted or rejected based on the grammar rules and parsing decisions made during the process.
