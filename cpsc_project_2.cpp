#include <iostream>
#include <string>
#include <map>
#include <stack>
#include <vector>

using namespace std;

// Structure to hold the production rules
map<int, string> production_rules = {
    {1, "E → E + T"},
    {2, "E → T"},
    {3, "T → T * F"},
    {4, "T → F"},
    {5, "F → (E)"},
    {6, "F → id"}
};

// Mapping production rules to the number of symbols to pop
map<int, int> rule_lengths = {
    {1, 3}, // E → E + T
    {2, 1}, // E → T
    {3, 3}, // T → T * F
    {4, 1}, // T → F
    {5, 3}, // F → (E)
    {6, 1}  // F → id
};

// Structure to hold the parsing table
map<int, map<string, string>> parsing_table = {
    {0, {{"id", "S5"}, {"(", "S4"}}},
    {1, {{"+", "S6"}, {"$", "acc"}}},
    {2, {{"+", "R2"}, {"*", "S7"}, {")", "R2"}, {"$", "R2"}}},
    {3, {{"+", "R4"}, {"*", "R4"}, {")", "R4"}, {"$", "R4"}}},
    {4, {{"id", "S5"}, {"(", "S4"}, {"E", "8"}}},
    {5, {{"+", "R6"}, {"*", "R6"}, {")", "R6"}, {"$", "R6"}}},
    {6, {{"id", "S5"}, {"(", "S4"}, {"T", "9"}}},
    {7, {{"id", "S5"}, {"(", "S4"}, {"F", "10"}}},
    {8, {{"+", "S6"}, {")", "S11"}}},
    {9, {{"+", "R1"}, {"*", "S7"}, {")", "R1"}, {"$", "R1"}}},
    {10, {{"+", "R3"}, {"*", "R3"}, {")", "R3"}, {"$", "R3"}}},
    {11, {{"+", "R5"}, {"*", "R5"}, {")", "R5"}, {"$", "R5"}}}
};

// Stack to maintain the parser state
stack<string> parse_stack;

void parseInput(const string& input) {
    parse_stack.push("0"); // Start state

    size_t index = 0;
    string action, state, symbol;
    bool accepted = false;

    while (index <= input.length()) {
        state = parse_stack.top();
        symbol = index < input.length() ? string(1, input[index]) : "$";

        cout << "Current state: " << state << ", Current symbol: " << symbol << endl;

        // Handle actions according to the parsing table
        if (parsing_table.count(stoi(state)) && parsing_table[stoi(state)].count(symbol)) {
            action = parsing_table[stoi(state)][symbol];
            cout << "Action taken: " << action << endl;

            if (action[0] == 'S') {
                // Shift action
                parse_stack.push(symbol); // Push symbol
                parse_stack.push(action.substr(1)); // Push state
                index++; // Move to next character
            } else if (action[0] == 'R') {
                // Reduce action
                int rule_number = stoi(action.substr(1));
                string production = production_rules[rule_number];
                cout << "Reduce using rule " << rule_number << ": " << production << endl;

                // Pop the symbols and states according to the rule length
                int num_symbols_to_pop = rule_lengths[rule_number] * 2;
                while (num_symbols_to_pop--) {
                    parse_stack.pop(); // Pop the symbol/state pairs
                }

                string lhs = production.substr(0, production.find("→") - 1); // Get the LHS of the production
                parse_stack.push(lhs); // Push the LHS nonterminal onto the stack
                string new_state = parsing_table[stoi(parse_stack.top())][lhs];
                parse_stack.push(new_state); // Push the new state obtained from the LHS
            } else if (action == "acc") {
                accepted = true;
                break;
            }
        } else {
            cout << "Error: No valid action for state " << state << " with symbol " << symbol << endl;
            break;
        }
    }

    if (accepted) {
        cout << "Input is accepted." << endl;
    } 
    else 
    {
        cout << "Input is not accepted." << endl; // at the end of the parsing process. Use this output to trace any issues if the parser doesn't behave as expected.
    }
}

int main() {
    string input;
    cout << "Enter input: ";
    cin >> input;
    parseInput(input);
    return 0;
}
