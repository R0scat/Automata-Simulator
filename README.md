# Automata Simulator
Python script that simulates a working DFA and NFA, reads a string of commands, displays the states the automata passes through and checks if the final state is accepted or not.

**OBS:** For each script you'll find a .txt file containing an example input for the setup!

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

## Pushdown Automaton (PDA)

Simulates a Pushdown Automaton. It uses states, an input alphabet, and a stack to process input strings. Transitions depend on the current state, input symbol (or epsilon), and the top stack symbol. It checks if the input string leads to an accepted final state.

### Setup

In the `in.txt` file:
- define PDA sections in this order:
     `states`
     `input alphabet`
     `stack alphabet`
     `transitions`
     `start state`
     `initial stack symbol`
     `accepted states`
- end each section with a line containing only `# end`.
- write **transitions** with the following 5-part format:
```
      currentState,inputSymbolOrEpsilon,stackSymbolToPop,nextState,stringOfSymbolsToPush`
```
- keep in mind that:
     * `inputSymbolOrEpsilon`: An input symbol, or `epsilon`.
     * `stackSymbolToPop`: Symbol popped from stack (cannot be `epsilon`).
     * `stringOfSymbolsToPush`: Symbols pushed to stack (rightmost first), or `epsilon` for no push.
       
*Example:* `q0,a,Z,q1,AZ`

*Note:*
* For multiple items (states, alphabet symbols) on one line, separate them with a comma (`,`) without spaces. E.g., `a,b,c`.
* The simulator will prompt for an input string (symbols separated by spaces) after parsing `in.txt`.

 ## Turing Machine (TM)

Simulates a Turing Machine. It uses a tape, states, an input alphabet, and a tape alphabet to process input strings. Transitions depend on the current state and the symbol read by the tape head. The TM can read, write, and move the head along the tape. It checks if the input string leads to an accepted final state.

### Setup

In the `in.txt` file:
- define TM sections in this order:
     `states`
     `input alphabet` (subset of tape alphabet)
     `tape alphabet` (includes input alphabet and blank symbol)
     `blank symbol` (one symbol from tape alphabet, usually not in input alphabet)
     `transitions`
     `start state`
     `accepted states`
- end each section with a line containing only `# end`.
- write **transitions** with the following 5-part format:
```
    `currentState,readSymbol,nextState,writeSymbol,Direction`
```
- where:
     * `readSymbol`: Symbol read from the tape under the head.
     * `writeSymbol`: Symbol written to the tape at the head's current position.
     * `Direction`: `L` (Left), `R` (Right), or `S` (Stay) for tape head movement.

*Example:* `q0,a,q1,X,R` (In state `q0`, if 'a' is read: go to state `q1`, write 'X', move head Right).
