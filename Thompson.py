# Mark Ndipenoch, 20/03/2013
# Shunting Yard Algorithm
# http://www.oxfordmathcenter.com/drupal7/node/628
# https://www.geeksforgeeks.org/infix-to-postfix-using-different-precedence-values-for-in-stack-and-out-stack/
# https://codeburst.io/conversion-of-infix-expression-to-postfix-expression-using-stack-data-structure-3faf9c212ab8
# https://en.wikipedia.org/wiki/Thompson%27s_construction
# https://web.tecnico.ulisboa.pt/~david.matos/w/pt/index.php/Theoretical_Aspects_of_Lexical_Analysis#Building_the_NFA:_Thompson.27s_Algorithm
# https://www.sciencedirect.com/science/article/pii/S0166218X03002993


def shunt(infix):

  specials = {'^':60,'*':50,'/':50,'%':50,'.':40,'+':45,'-':45,'|':30}

  pofix=""
  stack=""

  for c in infix:
    if c == '(':
        stack= stack+c
    elif c == ')':
        while stack[-1] !='(':
            pofix, stack = pofix + stack[-1], stack[:-1]
        stack = stack[:-1]
    elif c in specials:
	    #If the special character have less precedent than the preceding character in the stack, pop the 
		#preceding characters out of the stack and put it on the pofix, and delete the character in the stack.
        while stack and specials.get(c,0) <= specials.get(stack[-1],0):
            pofix, stack = pofix + stack[-1],stack[:-1]
		#If the special character have the same precedent like the preceding character in the stack, pop the 
		#preceding character out of the stack and put it on the pofix, and delete the character in the stack.
        while stack and specials.get(c,0) == specials.get(stack[-1],0):
            pofix, stack = pofix + stack[-1],stack[:-1]
        stack = stack + c
    else:
        pofix = pofix + c
   
  #At the end pop out all the characters from the stack and put them to pofix starting from the top.
  while stack:
      pofix, stack = pofix+ stack[-1],stack[:-1]
  
  return pofix

# Represent a state with two arrows, labelled by label.
# Use None for a label representing "e" arrows.
class state:
  label = None
  edge1 = None
  edge2 = None

# An NFA is represented by it's initial and accepts states.
class nfa:
  initial = None
  accept = None
  
  def __init__(self, initial,accept):
    self.initial = initial
    self.accept = accept

def compile(pofix):
  nfastack = []

  for c in pofix:
    if c =='.':
      # pop two NFA's off the stack.
      nfa2 = nfastack.pop()
      nfa1 = nfastack.pop()
      # Connect First NFA accept state to the second's initial state.
      nfa1.accept.edge1=nfa2.initial
      # Push NFA to the stack.
      newnfa = nfa(nfa1.initial,nfa2.accept)
      nfastack.append(newnfa)
    elif c =='|':
      # Pop two NFA's off the stack.
      nfa2 = nfastack.pop()
      nfa1 = nfastack.pop()
      #Create a new intial state and connect it to the initial state of the 
      #NFA's pop of from the stack
      initial = state()
      initial.edge1 = nfa1.initial
      initial.edge2 = nfa2.initial
      #Create a new accept state and coonect it to the 2 accpets state of
      # the NFA's poped from the stack.
      accept = state()
      nfa1.accept.edge1 = accept
      nfa2.accept.edge2 = accept
      # Push new NFA to the state
      newnfa = nfa(initial, accept)
      nfastack.append(newnfa)
    elif c =='|':
      # Pop two NFA's off the stack.
      nfa2 = nfastack.pop()
      nfa1 = nfastack.pop()
      #Create a new intial state and connect it to the initial state of the 
      #NFA's pop of from the stack
      initial = state()
      initial.edge1 = nfa1.initial
      initial.edge2 = nfa2.initial
      #Create a new accept state and coonect it to the 2 accpets state of
      # the NFA's poped from the stack.
      accept = state()
      nfa1.accept.edge1 = accept
      nfa2.accept.edge1 = accept
      # Push new NFA to the state
      newnfa = nfa(initial, accept)
      nfastack.append(newnfa)
    elif c =='+':
      # Pop two NFA's off the stack.
      nfa2 = nfastack.pop()
      nfa1 = nfastack.pop()
      #Create a new intial state and connect it to the initial state of the 
      #NFA's pop of from the stack
      initial = state()
      initial.edge1 = nfa1.initial
      initial.edge2 = nfa2.initial
      #Create a new accept state and coonect it to the 2 accpets state of
      # the NFA's poped from the stack.
      accept = state()
      nfa1.accept.edge1 = accept
      nfa2.accept.edge1 = accept
      # Push new NFA to the state
      newnfa = nfa(initial, accept)
      nfastack.append(newnfa)
    elif c =='*':
      # Pop a single NFA from the stack
      nfa1 = nfastack.pop()
      # Create and initial and accept states.
      initial = state()
      accept = state()
      # Join the new initial state to nfa1's initial state and the new accept  state.
      initial.edge1 = nfa1.initial
      initial.edge2 = accept
      # Join the old accept state to the new accept state and nfa1's initila state.
      nfa1.accept.edge1 = nfa1.initial
      nfa1.accept.edge2 = accept
      # Push new NFA to the stack.
      newnfa = nfa(initial,accept)
      nfastack.append(newnfa)
    else:
      # Create new initial and accept states.
      accept = state()
      initial = state()
      # Join the initial state and the accept state using arrow labelled c
      initial.label = c 
      initial.edge1 = accept
      # Push new NFA to the stack.
      newnfa = nfa(initial,accept)
      nfastack.append(newnfa)

  # The nfastack should only hhave a single NFA here
  return nfastack.pop()


def followes(state):
  """Return the set of states that can be reached from state following e arrows"""
  #Create a new set, with state as its only member.
  states = set()
  states.add(state)

  # Check if state has arrows labelled e from it.
  if state.label is None:
    # Check if edge1 is a state
    if state.edge1 is not None:
      # If there's an edge1, follow it.
      states |= followes(state.edge1)
    # check if edge2 is a state.
    if state.edge2 is not None:
      # if there's an edge2 follow it.
      states |= followes(state.edge2)

  # Return the set of states
  return states



def match(infix,string):
  """Matches string to infix regular expression"""

  # Shunt and compile teh regular expression.
  postfix = shunt(infix)
  nfa = compile(postfix)

  # The current set of states and the next set of states.
  current = set()
  next = set()

  # Add the initials state to the current set.
  current |= followes(nfa.initial)

  # Loop throught each character of the string
  for s in string:
    # loop through the current set of states
    for c in current:
      # check if that state is labelled s.
      if c.label == s:
        # Add the edge1 state to the next set.
        next |= followes(c.edge1)
    # Set current to next, and clear out next.
    current = next
    next = set()

  # Check if the accept state is in the set of current states.
  return (nfa.accept in current)


# A few tests.
infixes = ["a.b.c*","a.(b|d).c*","(a.(b|d))*","a.(b.b)*.c"]
strings = ["","abc","abbc","abcc","abad","abbbc"]

for i in infixes:
  for s in strings:
    print(match(i,s),i,s)