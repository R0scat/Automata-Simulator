import collections

# elemente de configuratie
MAX_TM_STEPS = 5000  # nr maxim de pasi pe care ii poate face TM-ul 
TAPE_WINDOW_SIZE = 15 # pt tape delay

def printAutom(autom_dict):
    print("Input parsed successfully, given values:")
    print()
    for key, value in autom_dict.items():
        print(f"{key}: {value}")
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

def extractTransitionTM(line):
    """Extracts a TM transition tuple (5 elements)."""
    line_no_space = ''.join(line.split())
    if line_no_space:
        parts = tuple(line_no_space.split(","))
        if len(parts) == 5:
            # current_state, read_symbol, next_state, write_symbol, direction
            return parts
        else:
            print(f"Warning: TM Transition '{line}' has incorrect format. Expected 5 parts. Skipping.")
            return None
    return None

def addData(inpt, field_name, autom_dict_ref):
    """Adds parsed data to the automata dictionary for the given field."""
    extracted_values = extractInput(inpt)
    if extracted_values or field_name in ['states', 'input alphabet', 'tape alphabet', 'transitions', 'accepted states']:
        if field_name not in autom_dict_ref:
            autom_dict_ref[field_name] = extracted_values
        else:
            if isinstance(autom_dict_ref[field_name], list) and isinstance(extracted_values, list):
                autom_dict_ref[field_name].extend(extracted_values)
            elif isinstance(extracted_values, list) and extracted_values: # if field was somehow not a list but should be
                autom_dict_ref[field_name] = extracted_values


def addTransitionTM(line_content, autom_dict_ref):
    """Adds a parsed TM transition to the automata dictionary."""
    transition_tuple = extractTransitionTM(line_content)
    if transition_tuple:
        if 'transitions' not in autom_dict_ref:
            autom_dict_ref['transitions'] = [transition_tuple]
        else:
            autom_dict_ref['transitions'].append(transition_tuple)

def checkValidityTMTransition(transition, autom_dict):
    if not isinstance(transition, tuple) or len(transition) != 5:
        print(f"Error: Invalid TM transition structure: {transition}")
        return False
    current_state, read_sym, next_state, write_sym, direction = transition

    if current_state not in autom_dict.get('states', []):
        print(f"Error: TM Transition current state '{current_state}' not in defined states.")
        return False
    if read_sym not in autom_dict.get('tape alphabet', []):
        print(f"Error: TM Transition read symbol '{read_sym}' not in tape alphabet.")
        return False
    if next_state not in autom_dict.get('states', []):
        print(f"Error: TM Transition next state '{next_state}' not in defined states.")
        return False
    if write_sym not in autom_dict.get('tape alphabet', []):
        print(f"Error: TM Transition write symbol '{write_sym}' not in tape alphabet.")
        return False
    if direction.upper() not in ['L', 'R', 'S']:
        print(f"Error: TM Transition direction '{direction}' is not L, R, or S.")
        return False
    return True

def isInputStringValidTM(input_str, input_alphabet_list):
    if not input_str.strip():
        return True
    symbols = input_str.split() 
    for sym in symbols:
        if sym not in input_alphabet_list:
            print(f"Error: Input symbol '{sym}' not in defined input alphabet: {input_alphabet_list}")
            return False
    return True

def print_tape_snapshot(tape, head_pos, current_state, step_count, blank_sym, window=TAPE_WINDOW_SIZE):
    """Prints a snapshot of the tape around the head position."""
    display_indices = range(head_pos - window // 2, head_pos + window // 2 + 1)
    
    tape_view = []
    head_line = []
    index_line = []

    for i in display_indices:
        symbol = str(tape.get(i, blank_sym))
        tape_view.append(symbol)
        index_line.append(str(i).center(len(symbol))) 
        if i == head_pos:
            head_line.append("^".center(len(symbol)))
        else:
            head_line.append(" ".center(len(symbol)))
            
    print(f"\nStep: {str(step_count):>5} | State: {current_state:<12} | Head @ {head_pos}")
    print(f"Idxs: {' '.join(index_line)}")
    print(f"Tape: {' '.join(tape_view)}")
    print(f"Head: {' '.join(head_line)}")

def startTuringMachineSimulation(input_sequence_str, autom_dict):
    blank_symbol = autom_dict.get('blank symbol', [None])[0]
    if not blank_symbol or blank_symbol not in autom_dict.get('tape alphabet', []):
        print(f"Critical Error: Blank symbol '{blank_symbol}' is not defined or not in tape alphabet.")
        return False

    tape = collections.defaultdict(lambda: blank_symbol)
    input_symbols = input_sequence_str.split() if input_sequence_str.strip() else []

    for i, char_sym in enumerate(input_symbols):
        tape[i] = char_sym
    
    head_pos = 0
    current_state = autom_dict['start state'][0]
    step_count = 0

    print("\n--- Starting Turing Machine Simulation ---")
    print(f"Initial Input: '{input_sequence_str}'")
    print(f"Initial State: {current_state}, Head at: {head_pos}, Blank: '{blank_symbol}'")
    print_tape_snapshot(tape, head_pos, current_state, step_count, blank_symbol)

    while step_count < MAX_TM_STEPS:
        current_symbol_read = tape[head_pos] 

        if current_state in autom_dict.get('accepted states', []):
            print(f"\nHALTED and ACCEPTED in state '{current_state}' after {step_count} steps.")
            print_tape_snapshot(tape, head_pos, current_state, "Final", blank_symbol, window=TAPE_WINDOW_SIZE*2)
            return True

        found_transition = False
        for trans in autom_dict.get('transitions', []):
            if trans[0] == current_state and trans[1] == current_symbol_read:
                next_state = trans[2]
                symbol_to_write = trans[3]
                direction = trans[4].upper()

                tape[head_pos] = symbol_to_write 
                
                if direction == 'L':
                    head_pos -= 1
                elif direction == 'R':
                    head_pos += 1
                # 'S'= stay = stai pe loc = nu se schimba head_pos

                current_state = next_state
                found_transition = True
                step_count += 1
                print_tape_snapshot(tape, head_pos, current_state, step_count, blank_symbol)
                break 

        if not found_transition:
            print(f"\nHALTED (no transition found) from state '{current_state}' reading '{current_symbol_read}' at head position {head_pos} after {step_count} steps.")
            print_tape_snapshot(tape, head_pos, current_state, "Final", blank_symbol, window=TAPE_WINDOW_SIZE*2)
            return False 

    print(f"\nHALTED (maximum steps {MAX_TM_STEPS} reached). Current state: '{current_state}'.")
    print_tape_snapshot(tape, head_pos, current_state, "Max Steps", blank_symbol, window=TAPE_WINDOW_SIZE*2)
    return False

def runTuringMachine(autom_dict):
    print("\nIntroduce TM input string (symbols separated by spaces, or empty for empty string):")
    steps = input()
    if not isInputStringValidTM(steps, autom_dict.get('input alphabet', [])):
        return False
    else:
        return startTuringMachineSimulation(steps, autom_dict)

def parseAndValidateTM(autom_dict, tm_fields_list):
    for field in tm_fields_list:
        if field not in autom_dict:
            if field == 'transitions': autom_dict['transitions'] = [] 
            else:
                print(f"Error: Mandatory field '{field}' is missing from the definition.")
                return False
        expected_list_fields = ['states', 'input alphabet', 'tape alphabet', 'transitions', 'accepted states']
        expected_single_item_list_fields = ['blank symbol', 'start state']

        if field in expected_list_fields and not isinstance(autom_dict[field], list):
            print(f"Error: Field '{field}' should be a list. Found: {type(autom_dict[field])}")
            return False
        if field in expected_single_item_list_fields:
            if not isinstance(autom_dict[field], list) or len(autom_dict[field]) != 1:
                print(f"Error: Field '{field}' must contain exactly one item. Found: {autom_dict[field]}")
                return False

    for field_name in ['states', 'input alphabet', 'tape alphabet']:
        if not autom_dict.get(field_name) and field_name == 'states':
            print(f"Error: '{field_name}' cannot be empty.")
            return False
        current_field_values = autom_dict.get(field_name, [])
        if len(current_field_values) != len(set(current_field_values)):
            print(f"Error: Duplicate items found in '{field_name}': {current_field_values}")
            return False

    input_alpha_set = set(autom_dict.get('input alphabet', []))
    tape_alpha_set = set(autom_dict.get('tape alphabet', []))
    blank_sym_list = autom_dict.get('blank symbol', [])
    blank_sym = blank_sym_list[0] if blank_sym_list else None


    if not blank_sym: 
        print("Error: Blank symbol is not defined or has incorrect format.") 
        return False
    if blank_sym not in tape_alpha_set:
        print(f"Error: Blank symbol '{blank_sym}' not in tape alphabet {tape_alpha_set}.")
        return False
    if not input_alpha_set.issubset(tape_alpha_set):
        print(f"Error: Input alphabet {input_alpha_set} is not a subset of tape alphabet {tape_alpha_set}.")
        return False
    if blank_sym in input_alpha_set:
        print(f"Warning: Blank symbol '{blank_sym}' is present in the input alphabet. This is unconventional.")

    start_state_list = autom_dict.get('start state', [])
    start_state = start_state_list[0] if start_state_list else None
    if not start_state or start_state not in autom_dict.get('states', []): # also check if states is defined
        print(f"Error: Start state '{start_state}' not defined or not in defined states {autom_dict.get('states', [])}.")
        return False

    for acc_state in autom_dict.get('accepted states', []):
        if acc_state not in autom_dict.get('states', []):
            print(f"Error: Accepted state '{acc_state}' not in defined states {autom_dict.get('states', [])}.")
            return False

    valid_transitions = []
    for t_idx, trans_tuple in enumerate(autom_dict.get('transitions', [])):
        if checkValidityTMTransition(trans_tuple, autom_dict):
            valid_transitions.append(trans_tuple)
        else:
            print(f"Error: Invalid transition #{t_idx + 1}: {trans_tuple}. Halting validation.")
            return False 
    autom_dict['transitions'] = valid_transitions
    
    return True

# PARTEA PRINCIPALA A CODULUI 
if __name__ == "__main__":
    autom = {} 
    tm_fields = ['states', 'input alphabet', 'tape alphabet', 'blank symbol', 
                 'transitions', 'start state', 'accepted states']
    current_field_idx = 0
    
    try:
        with open('in.txt', 'r') as fin:
            lines = fin.readlines()
    except FileNotFoundError:
        print("Error: 'in.txt' not found. Please create it with the TM definition.")
        exit()

    for line_num, line_content_orig in enumerate(lines):
        line_content_stripped = line_content_orig.strip()

        if not line_content_stripped:  # da skip la liniile complet nule
            continue

        process_as_data = True
        
        # verif daca e un comentariu complet linia
        if line_content_stripped.startswith('#'):
            process_as_data = False # presupune ca linia nu are date (deci nu e procesata ca data relevanta)
            potential_end_marker_text = line_content_stripped[1:].strip().lower()
            is_special_comment_end_marker = False

            if potential_end_marker_text == 'end':
                is_special_comment_end_marker = True
            elif current_field_idx < len(tm_fields) and \
                 potential_end_marker_text == f"{tm_fields[current_field_idx]} end":
                is_special_comment_end_marker = True
            
            if is_special_comment_end_marker:
                current_field_idx += 1
                if current_field_idx > len(tm_fields):
                    print(f"Warning (line {line_num+1}): Too many 'end' markers (comment '{line_content_orig.strip()}').")
                # line was an end marker (disguised as comment), so skip further processing for this line
                continue 
            else:
                # comment line simplu caruia i se da skip
                continue
        
        # nu e comment complet dar oate fi in continuare end-comment, non-comment 'end' sau data
        effective_content = line_content_stripped 
        if '#' in effective_content: # verif daca e end-comment
            effective_content, _ = effective_content.split('#', 1)
            effective_content = effective_content.strip()
        
        if not effective_content: 
            continue

        # verif 'end'
        is_section_end_marker = False
        normalized_effective_content = effective_content.lower()

        if normalized_effective_content == 'end':
            is_section_end_marker = True
        elif current_field_idx < len(tm_fields) and \
             normalized_effective_content == f"{tm_fields[current_field_idx]} end":
            is_section_end_marker = True
        
        if is_section_end_marker:
            current_field_idx += 1
            if current_field_idx > len(tm_fields): # should literally not happen if file is well-formed (ideal)
                print(f"Warning (line {line_num+1}): Too many 'end' markers ('{line_content_orig.strip()}').")
            process_as_data = False # end marker
            continue # skip linia urmatoare dupa procesarea 'end'

        # de aici effective_content e data pt ce field-ul curent
        if process_as_data:
            if current_field_idx >= len(tm_fields):
                if effective_content: 
                     print(f"Warning (line {line_num+1}): Data '{effective_content}' found after all expected sections for line '{line_content_orig.strip()}'.")
                continue

            current_field_name = tm_fields[current_field_idx]

            if current_field_name == 'transitions':
                addTransitionTM(effective_content, autom) 
            else:
                addData(effective_content, current_field_name, autom)
    
    print("--- Parsed Turing Machine Structure ---")
    printAutom(autom)
    print()

    if parseAndValidateTM(autom, tm_fields):
        print("\nTM definition is valid.")
        runTuringMachine(autom)
    else:
        print("\nTM definition has errors. Cannot run simulation.")
