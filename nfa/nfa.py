def printAutom(autom):
    print("Input parsed successfully, given values:")
    print()
    for key in autom:
        print(key, autom[key], sep=': ')
        print()

def extractInput(line):
    l = []
    if ',' in line:
        line = line.replace(' ', '')
        l = line.split(',')
    elif line:
        l.append(line.strip(' '))
    return l

def extractTransition(line):
    line = line.replace(' ', '')
    if line:
        return tuple(line.split(","))

def addData(inpt):
    if fields[contor] not in autom:
        autom[fields[contor]] = extractInput(inpt)
    else:
        autom[fields[contor]].extend(extractInput(inpt))

def addTransition(line):
    if extractTransition(line):
        if fields[contor] not in autom:
            autom[fields[contor]] = [extractTransition(line)]
        else:
            autom[fields[contor]].append(extractTransition(line))

def checkValidity(transition):
    for element in transition:
        if element not in autom['alphabet'] and element not in autom['states']:
            return False
    return True

def isInAlphabet(steps):
    l = steps.split()
    for element in l:
        if element not in autom['alphabet'] and element != 'e':
            return False
    return True

def epsilon_closure(states):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for transition in autom['transitions']:
            if transition[0] == state and transition[1] == 'e':
                if transition[2] not in closure:
                    closure.add(transition[2])
                    stack.append(transition[2])
    return closure

def transitionAccepted(step, currentStates):
    next_states = set()
    for state in currentStates:
        for transition in autom['transitions']:
            if transition[0] == state and transition[1] == step:
                next_states.add(transition[2])
    return next_states

def startCompilingSteps(steps):
    def dfs(currentStates, remainingSteps):
        currentStates = epsilon_closure(currentStates)

        if not remainingSteps:
            return any(state in autom['accepted states'] for state in currentStates)

        step = remainingSteps[0]
        nextStates = set()

        for state in currentStates:
            transitions = transitionAccepted(step, [state])
            for ns in transitions:
                nextStates.update(epsilon_closure([ns]))

        if not nextStates:
            return False

        return dfs(nextStates, remainingSteps[1:])

    inputSteps = steps.split()
    currentStates = [autom['start state'][0]]
    accepted = dfs(currentStates, inputSteps)

    if accepted:
        print("Accepted: at least one path ends in a final state.")
    else:
        print("Rejected: no valid paths lead to a final state.")


def runAutomata():
    print("Introduce automata steps (with spaces in between the inputs, use 'e' for epsilon):")
    steps = input()
    if not isInAlphabet(steps):
        print("Error: input contains invalid characters")
        return False
    else:
        startCompilingSteps(steps)

def parse():
    for key in autom:
        if key == 'transitions':
            for tupl in autom['transitions']:
                if checkValidity(tupl) == False:
                    print('Error: input parsed, unrecognised transition elements')
                    return False
        elif key != 'states' and key != 'alphabet':
            if checkValidity(autom[key]) == False:
                print(f"Error: input parsed, unrecognised {key}")
                return False
    runAutomata()

# build automata
fin = open('in.txt', 'r')
lines = fin.readlines()
autom = {}
fields = ['states', 'alphabet', 'transitions', 'start state', 'accepted states']
contor = 0

for line in lines:
    line = line.strip()
    if 'end' in line:
        contor += 1
    elif contor == 2:
        if '#' in line:
            if line[0] != '#':
                inpt, *_ = line.split('#')
                addTransition(inpt)
        else:
            addTransition(line)
    else:
        if '#' in line:
            if line[0] != '#':
                inpt, *_ = line.split('#')
                addData(inpt)
        else:
            addData(line)
fin.close()

printAutom(autom)
parse()
