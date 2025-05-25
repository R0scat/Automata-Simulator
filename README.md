# Automata Simulator
Python script that simulates a working DFA and NFA, reads a string of commands, displays the states the automata passes through and checks if the final state is accepted or not.

## Deterministic Formal Automata (DFA)
Given states and an alphabet it passes through them and checks if the final one is accepted or not. For it to change states it always needs an input. 

### Setup
In the *in.txt* file:
- include your automata states, alphabet, transitions, start state and final states in this order
- include *#end* after each field
- write transitions with the following format: 
    
        [start state], [alphabet letter], [final state] 

*Note:*You can add comments anywhere using "#"; if you want to add multiple states/ words on one line you must seperate them with a ",".

## Non-deterministic Formal Automata (NFA)
Similar to the NFA, except it can pass through states without 'consuming' an input. For that to happen the transition epsilon (written as e) must be present in the transition states 

### Setup 
Very similar to the DFA setup, except:
- must add 'e' to your alphabet
- must specify transitons possible with e as well

 
