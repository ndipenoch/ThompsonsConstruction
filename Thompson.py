# https://en.wikipedia.org/wiki/Thompson%27s_construction
# https://web.tecnico.ulisboa.pt/~david.matos/w/pt/index.php/Theoretical_Aspects_of_Lexical_Analysis#Building_the_NFA:_Thompson.27s_Algorithm
# https://www.sciencedirect.com/science/article/pii/S0166218X03002993

# Represent a state with two arrows, labelled by label.
# Use None for a label representing "e" arrows.
class state:
  label=None
  edge1=None
  edge2=None

# An NFA is represented by it's initial and accepts states.