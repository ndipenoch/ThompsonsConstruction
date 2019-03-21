# https://en.wikipedia.org/wiki/Thompson%27s_construction
# https://web.tecnico.ulisboa.pt/~david.matos/w/pt/index.php/Theoretical_Aspects_of_Lexical_Analysis#Building_the_NFA:_Thompson.27s_Algorithm
# https://www.sciencedirect.com/science/article/pii/S0166218X03002993

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
      nfa2.accept.edge2 = accept
      # Push new NFA to the state
      newnfa = nfa(initial, accept)
      nfastack.append(newnfa)
    elif c =='+':
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
print(compile("ab.cd.|"))
print(compile("aa.*"))
print(compile("A B * C +"))