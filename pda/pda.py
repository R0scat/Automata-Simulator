import collections

def printAutom(autom):
    print("Input parsed succesfully, given values:")
    print()
    for key in autom:
        print(f"{key}: {autom[key]}")
        print()

def extractInput(line):
    """Extracts comma-separated items or a single item from a line."""
    l = []
    clean_line = line.strip()
    if not clean_line: 
        return l
    if ',' in clean_line:
        processed_line = ''.join(clean_line.split()) 
        l = processed_line.split(',')
    else:
        l.append(clean_line)
    return l

def extractTransitionPDA(line):
    """Extracts a PDA transition tuple (5 elements)."""
    line = ''.join(line.split())
    if line:
        parts = tuple(line.split(","))
        if len(parts) == 5:
            return parts
        else:
            print(f"Warning: Transition '{line}' has incorrect format. Expected 5 parts (from_state,input,pop,to_state,push). Skipping.")
            return None
    return None

def addData(inpt, field_name, autom_dict):
    """Adds parsed data to the automata dictionary for the given field."""
    extracted_values = extractInput(inpt)
    if not extracted_values and field_name not in ['transitions', 'alphabet', 'stack alphabet', 'states']: # These can start empty and be populated
         # print(f"Note: No data provided for '{field_name}' from line '{inpt}' during initial add.")
         pass # Allow empty, validation will handle later if mandatory fields are missing items

    if field_name not in autom_dict:
        autom_dict[field_name] = extracted_values
    else:
        # Ensure list extension, not character-by-character for strings
        if isinstance(autom_dict[field_name], list) and isinstance(extracted_values, list):
             autom_dict[field_name].extend(extracted_values)
        elif isinstance(extracted_values, list) and extracted_values: # if autom_dict[field_name] was not init as list
             autom_dict[field_name] = extracted_values
        # Handle cases where a field might expect a single value but gets multiple lines; extractInput handles single/multiple items per line.
        # For 'start state' and 'initial stack symbol', validation will ensure only one item.


def addTransitionPDA(line_content, autom_dict):
    """Adds a parsed PDA transition to the automata dictionary."""
    transition_tuple = extractTransitionPDA(line_content)
    if transition_tuple:
        if 'transitions' not in autom_dict:
            autom_dict['transitions'] = [transition_tuple]
        else:
            autom_dict['transitions'].append(transition_tuple)

def checkValidityPDATransition(transition, autom_dict):
    """Checks if a single PDA transition is valid based on defined states and alphabets."""
    if not isinstance(transition, tuple) or len(transition) != 5:
        print(f"Error: Invalid transition structure: {transition}")
        return False

    from_state, input_char, pop_char, to_state, push_string = transition

    if from_state not in autom_dict.get('states', []):
        print(f"Error: Transition source state '{from_state}' not in defined states {autom_dict.get('states', [])}.")
        return False
    if input_char != 'epsilon' and input_char not in autom_dict.get('alphabet', []):
        print(f"Error: Transition input symbol '{input_char}' not in sigma {autom_dict.get('alphabet', [])} or not 'epsilon'.")
        return False
    if pop_char == 'epsilon' or pop_char not in autom_dict.get('stack alphabet', []): # pop_char cannot be epsilon and must be in stack alphabet
        print(f"Error: Transition stack pop symbol '{pop_char}' is 'epsilon' or not in stack alphabet {autom_dict.get('stack alphabet', [])}.")
        return False
    if to_state not in autom_dict.get('states', []):
        print(f"Error: Transition destination state '{to_state}' not in defined states {autom_dict.get('states', [])}.")
        return False
    
    if push_string != 'epsilon':
        for char_s in push_string:
            if char_s not in autom_dict.get('stack alphabet', []):
                print(f"Error: Symbol '{char_s}' in push string '{push_string}' not in stack alphabet {autom_dict.get('stack alphabet', [])}.")
                return False
    return True
    
def isInputStringValid(input_str, alphabet):
    """Checks if all symbols in the input string are in the defined alphabet."""
    if not input_str.strip(): # Empty string is a valid sequence of 0 symbols
        return True
    symbols = input_str.split()
    for sym in symbols:
        if sym not in alphabet:
            return False
    return True

def startCompilingPDA(input_sequence_str, autom_dict):
    """Simulates the PDA execution for the given input string."""
    input_symbols = input_sequence_str.split() if input_sequence_str.strip() else []

    if not autom_dict.get('start state') or not autom_dict.get('initial stack symbol'):
        print("Error: Start state or initial stack symbol not defined.")
        return False
        
    initial_state = autom_dict['start state'][0]
    initial_stack_sym = autom_dict['initial stack symbol'][0]

    if initial_stack_sym == 'epsilon' or initial_stack_sym not in autom_dict.get('stack alphabet',[]):
        print(f"Error: Initial stack symbol '{initial_stack_sym}' is 'epsilon' or not in stack alphabet.")
        return False
        
    # Queue stores: (current_state, input_index, current_stack_list)
    # input_index is the index of the *next* symbol to read.
    queue = collections.deque([(initial_state, 0, [initial_stack_sym])])
    # Visited stores: (state, input_index, tuple(stack))
    visited = set([(initial_state, 0, tuple([initial_stack_sym]))])

    accepted_configurations_details = [] # To store details of accepting paths

    max_stack_heuristic = len(input_symbols) + len(autom_dict.get('states', [])) + 50 # Basic heuristic

    while queue:
        current_state, input_idx, current_stack = queue.popleft()

        # --- 1. Try Epsilon-input transitions first ---
        # (state, 'epsilon', pop_sym) -> (next_state, push_syms)
        for trans_idx, trans in enumerate(autom_dict.get('transitions', [])):
            if trans[0] == current_state and trans[1] == 'epsilon':
                pop_symbol = trans[2]
                
                if not current_stack or current_stack[-1] != pop_symbol:
                    continue # Stack empty or top doesn't match pop_symbol

                new_stack_after_pop = list(current_stack[:-1])
                final_new_stack_eps = list(new_stack_after_pop) # Make a copy

                symbols_to_push = trans[4]
                if symbols_to_push != 'epsilon':
                    for char_idx in range(len(symbols_to_push) - 1, -1, -1): # Push in reverse
                        final_new_stack_eps.append(symbols_to_push[char_idx])
                
                # Heuristic stack depth check
                if len(final_new_stack_eps) > max_stack_heuristic :
                    # print(f"Warning: Stack depth limit exceeded on epsilon transition. Pruning path.")
                    continue

                next_config_tuple = (trans[3], input_idx, tuple(final_new_stack_eps))
                
                if next_config_tuple not in visited:
                    visited.add(next_config_tuple)
                    queue.append((trans[3], input_idx, final_new_stack_eps))
                    # print(f"  Epsilon transition {trans} -> State={trans[3]}, Idx={input_idx}, Stack={final_new_stack_eps}")


        # --- 2. Check for acceptance if input is fully consumed ---
        # This check happens after all possible epsilon transitions from the current state are explored.
        if input_idx == len(input_symbols):
            if current_state in autom_dict.get('accepted states', []):
                accept_detail = f"Accepted: State={current_state}, Input Consumed, Stack={current_stack}"
                if accept_detail not in accepted_configurations_details: # Avoid duplicate messages for same end state
                    accepted_configurations_details.append(accept_detail)
                # To find one acceptance: return True. To find all, continue processing queue.
                # For this implementation, we'll gather all and report at the end.

        # --- 3. Try transitions consuming an input symbol ---
        if input_idx < len(input_symbols):
            current_input_char = input_symbols[input_idx]
            for trans_idx, trans in enumerate(autom_dict.get('transitions', [])):
                if trans[0] == current_state and trans[1] == current_input_char:
                    pop_symbol = trans[2]

                    if not current_stack or current_stack[-1] != pop_symbol:
                        continue # Stack empty or top doesn't match pop_symbol
                        
                    new_stack_after_pop = list(current_stack[:-1])
                    final_new_stack_input = list(new_stack_after_pop) # Make a copy

                    symbols_to_push = trans[4]
                    if symbols_to_push != 'epsilon':
                        for char_idx in range(len(symbols_to_push) - 1, -1, -1):
                            final_new_stack_input.append(symbols_to_push[char_idx])
                    
                    if len(final_new_stack_input) > max_stack_heuristic:
                        # print(f"Warning: Stack depth limit exceeded on input transition. Pruning path.")
                        continue

                    next_config_tuple = (trans[3], input_idx + 1, tuple(final_new_stack_input))
                    
                    if next_config_tuple not in visited:
                        visited.add(next_config_tuple)
                        queue.append((trans[3], input_idx + 1, final_new_stack_input))
                        # print(f"  Consumed '{current_input_char}', trans {trans} -> State={trans[3]}, Idx={input_idx + 1}, Stack={final_new_stack_input}")
    
    if accepted_configurations_details:
        print(f"\nInput string '{input_sequence_str}' is ACCEPTED.")
        for detail in accepted_configurations_details:
             print(f"  {detail}")
        return True
    else:
        print(f"\nInput string '{input_sequence_str}' is REJECTED.")
        return False

def runPDA(autom_dict):
    print("\nIntroduce PDA input string (symbols separated by spaces):")
    steps = input()
    if not isInputStringValid(steps, autom_dict.get('alphabet', [])):
        print("Error: Input string contains characters not in the defined alphabet.")
        return False
    else:
        return startCompilingPDA(steps, autom_dict)
    
def parseAndValidate(autom_dict, pda_fields_list):
    """Validates the parsed PDA structure."""
    # Basic structural checks
    for field in ['states', 'alphabet', 'stack alphabet', 'transitions', 'start state', 'initial stack symbol', 'accepted states']:
        if field not in autom_dict:
            if field == 'transitions': # Transitions can be empty for some PDAs
                autom_dict['transitions'] = []
            else:
                print(f"Error: Mandatory field '{field}' is missing from the definition.")
                return False
        # Ensure fields that expect lists are lists
        if field in ['states', 'alphabet', 'stack alphabet', 'transitions', 'accepted states'] and not isinstance(autom_dict[field], list):
             print(f"Error: Field '{field}' should be a list. Found: {type(autom_dict[field])}")
             return False
        # Ensure single-item fields are lists of one item
        if field in ['start state', 'initial stack symbol']:
            if not isinstance(autom_dict[field], list) or len(autom_dict[field]) != 1:
                print(f"Error: Field '{field}' must contain exactly one item. Found: {autom_dict[field]}")
                return False


    # Validate states, alphabet, stack alphabet (ensure no 'epsilon' keyword unless intended, and no duplicates)
    for field_name in ['states', 'alphabet', 'stack alphabet']:
        if not autom_dict.get(field_name): # Allow empty alphabet/stack alphabet if not used by transitions
            if field_name == 'states' : # States cannot be empty
                print(f"Error: '{field_name}' cannot be empty.")
                return False
            # print(f"Warning: '{field_name}' is empty.")
            autom_dict[field_name] = [] # Ensure it's an empty list
        
        # Check for duplicates
        if len(autom_dict[field_name]) != len(set(autom_dict[field_name])):
            print(f"Error: Duplicate items found in '{field_name}': {autom_dict[field_name]}")
            return False
        # 'epsilon' should not be a state name or stack symbol by convention
        if 'epsilon' in autom_dict[field_name] and field_name != 'alphabet': # epsilon can be in sigma
             print(f"Warning: 'epsilon' found in '{field_name}'. This is unconventional.")


    # Validate start state
    start_state = autom_dict['start state'][0]
    if start_state not in autom_dict['states']:
        print(f"Error: Start state '{start_state}' not in defined states {autom_dict['states']}.")
        return False

    # Validate initial stack symbol
    initial_stack_sym = autom_dict['initial stack symbol'][0]
    if initial_stack_sym == 'epsilon' or initial_stack_sym not in autom_dict['stack alphabet']:
        print(f"Error: Initial stack symbol '{initial_stack_sym}' is 'epsilon' or not in stack alphabet {autom_dict['stack alphabet']}.")
        return False

    # Validate accepted states
    if not autom_dict.get('accepted states'): # Accepted states list can be empty
        # print("Warning: No accepted states defined.")
        pass
    for acc_state in autom_dict.get('accepted states', []):
        if acc_state not in autom_dict['states']:
            print(f"Error: Accepted state '{acc_state}' not in defined states {autom_dict['states']}.")
            return False

    # Validate transitions
    valid_transitions = []
    for t_idx, trans_tuple in enumerate(autom_dict.get('transitions', [])):
        if checkValidityPDATransition(trans_tuple, autom_dict):
            valid_transitions.append(trans_tuple)
        else:
            print(f"Error: Invalid transition #{t_idx + 1}: {trans_tuple}. Automata cannot run.")
            return False # Stop if any transition is invalid
    autom_dict['transitions'] = valid_transitions 
    
    return True


# --- Main script execution ---
if __name__ == "__main__":
    autom = {}
    # Order is important for parsing based on 'end' keyword
    pda_fields = ['states', 'alphabet', 'stack alphabet', 'transitions', 
                  'start state', 'initial stack symbol', 'accepted states']
    current_field_idx = 0
    
    try:
        with open('in.txt', 'r') as fin:
            lines = fin.readlines()
    except FileNotFoundError:
        print("Error: 'in.txt' not found. Please create the file with PDA definition.")
        exit()

    for line_num, line_content in enumerate(lines):
        line_content = line_content.strip()

        if not line_content: # Skip empty lines
            continue
        
        if line_content.startswith('#'): # Skip full comment lines
            # Check for 'end' within a comment, which is unusual but technically possible
            if 'end' in line_content.lower() and current_field_idx < len(pda_fields) and line_content.strip().lower() == f"# {pda_fields[current_field_idx]} end": # A very specific comment format
                current_field_idx +=1
            elif 'end' in line_content.lower() and not line_content.lower().startswith('# end'): # avoid generic #...end...
                 pass # Just a comment with 'end' in it.
            elif line_content.lower() == '# end': # Generic '# end'
                current_field_idx +=1

            continue # Process next line

        # Handle comments at the end of a line
        if '#' in line_content:
            line_content, _ = line_content.split('#', 1)
            line_content = line_content.strip()
            if not line_content: # Line became empty after stripping comment
                 continue


        if 'end' in line_content.lower(): # Check for 'end' keyword
            # Simple 'end' or 'section end' should advance the field index
            # More robustly, check if it's ONLY 'end' possibly with section name
            # e.g. "# end states" or simply "end"
            is_section_end = False
            if line_content.lower() == 'end':
                is_section_end = True
            elif current_field_idx < len(pda_fields) and \
                 line_content.lower() == f"{pda_fields[current_field_idx]} end": # e.g. "states end"
                is_section_end = True
            
            if is_section_end:
                current_field_idx += 1
                if current_field_idx > len(pda_fields):
                    print(f"Warning (line {line_num+1}): Too many 'end' markers or incorrect file structure. Expected {len(pda_fields)} sections.")
                continue # Move to next line after processing 'end'

        if current_field_idx >= len(pda_fields):
            if line_content: # Non-empty, non-comment line after all fields parsed
                 print(f"Warning (line {line_num+1}): Data '{line_content}' found after all expected sections have been closed.")
            continue

        current_field_name = pda_fields[current_field_idx]

        if current_field_name == 'transitions':
            addTransitionPDA(line_content, autom)
        else:
            addData(line_content, current_field_name, autom)

    print("--- Parsed Automata Structure ---")
    printAutom(autom)
    print()

    if parseAndValidate(autom, pda_fields):
        print("\nPDA definition is valid.")
        runPDA(autom)
    else:
        print("\nPDA definition has errors. Cannot run simulation.")