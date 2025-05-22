def lineLenght(string):
    ln = 0
    for character in string:
        if character != ' ':
            ln += 1
    return ln

def findLineIndex(lines):
    i = 0
    for line in lines:
        if line[0] != '#':
            return i
        i += 1

def loadMatrix(fn):
    fin = open(fn, 'r')
    lines = fin.readlines()
    a = []
    i = findLineIndex(lines)
    # print(i)
    # o sa presupun ca primul tip de comentariu este facut DOAR la inceput de linie
    for line in lines:
        line = line.strip()
        if line[0] != '#': #considerat comentariu la inceput de linie
            if lineLenght(lines[i].strip()) != lineLenght(line):
                print('not a matrix')
                return False
            line = line.split()
            a.append(line)
    return a

def saveMatrix(a, fn):
    fout = open (fn, 'w')
    for line in a:
        for element in line:
            fout.write(element)
            fout.write(" ")
        fout.write("\n")
    
a = loadMatrix('in.txt')
print(a)
# saveMatrix(a, 'out.txt')

#%%
# citim un automat
# avem mai multe sectiuni:
# starile
# alfabetul = sigma
# transitions = delta
# lista de tripleti!verifica starile si inputul --> da eroare 
# muttimea starii de start
# starea finala

def printAutom(autom):
    print("Input parsed succesfully, given values:")
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
        l = ()
        l = line.split(",")
        return l

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
    else:
        return True
    
def isInAlphabet(steps):
    l = steps.split()
    for element in l:
        if element not in autom['alphabet']:
            return False
    return True

def transitionAccepted(step, currentState):
    for transition in autom['transitions']:
        if currentState == transition[0]:
            if step == transition[1]:
                return True
    return False

def nextStep(step, currentState):
    for transition in autom['transitions']:
        if currentState == transition[0]:
            if step == transition[1]:
                return transition[2]

def startCompilingSteps(steps):
    currentState = autom['start state'][0]
    for step in steps.split():
        if transitionAccepted(step, currentState):
            print(f'Step {currentState} --({step})--> {nextStep(step, currentState)} accepted')
            currentState = nextStep(step, currentState)
        else:
            print(f"Error: transition {currentState} --({step})--> undefined")
            return False
    if currentState in autom['accepted states']:
        print(f'Final state: {currentState} accepted')
    else:
        print(f'Final state: {currentState} NOT accepted')

def runAutomata():
    print("Introduce automata steps (with spaces in between the letters):")
    steps = input()
    if not isInAlphabet(steps):
        print("Error: input contains invalid characters")
        return False
    else:
        startCompilingSteps(steps)
    
    
def parse():
    for key in autom:
        if key == 'transitions':
            for tupl in autom['transitions']: # transitions need to be separated!!
                if checkValidity(tupl) == False:
                    print('Error: input parsed, unrecognised transition elements')
                    return False
        elif key != 'states' and key != 'alphabet':
            if checkValidity(autom[key]) == False:
                print(f"Error: input parsed, unrecognised {key}")
                return False
    runAutomata()

# build automata
fin = open('resources/in.txt', 'r')
lines = fin.readlines()
autom = {}
fields = ['states', 'alphabet', 'transitions', 'start state', 'accepted states']
contor = 0;

for line in lines:
    line = line.strip()
    if 'end' in line:
        contor += 1
    elif contor == 2:
        if '#' in line:
            if line[0] != '#':
                inpt, mesaj = line.split('#');
                addTransition(inpt)
        else:
            addTransition(line)
    else:
        if '#' in line:
            if line[0] != '#':
                inpt, mesaj = line.split('#');
                addData(inpt)
        else:
            addData(line)
fin.close()

printAutom(autom)

parse()
    

        
