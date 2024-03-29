# Mark Ndipenoch, 20/03/2013
# Shunting Yard Algorithm
# http://www.oxfordmathcenter.com/drupal7/node/628
# https://www.geeksforgeeks.org/infix-to-postfix-using-different-precedence-values-for-in-stack-and-out-stack/
# https://codeburst.io/conversion-of-infix-expression-to-postfix-expression-using-stack-data-structure-3faf9c212ab8
# https://en.wikipedia.org/wiki/Thompson%27s_construction
# https://web.tecnico.ulisboa.pt/~david.matos/w/pt/index.php/Theoretical_Aspects_of_Lexical_Analysis#Building_the_NFA:_Thompson.27s_Algorithm
# https://www.sciencedirect.com/science/article/pii/S0166218X03002993

#Import tkinter library for GUI
import tkinter
from tkinter import filedialog
from tkinter import *

"""Start of shunting"""
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

#Matching starts
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
      #Pipe | is Union, it matches one or the other.
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
    elif c =='?':
      # Question mark ?,matches zero or one.
      # Pop a single NFA from the stack
      nfa1 = nfastack.pop()
      # Create and initial and accept states.
      initial = state()
      accept = state()
      # Join the new initial state to nfa1's initial state and the new accept  state.
      initial.edge1 = nfa1.initial
      initial.edge2 = accept
      # Join the old accept state to the new accept state.
      nfa1.accept.edge2 = accept
      # Push new NFA to the stack.
      newnfa = nfa(initial,accept)
      nfastack.append(newnfa)
    elif c =='+':
       # plus + matches one or more
       # Pop a single NFA from the stack
      nfa1 = nfastack.pop()
      # Join the accept state to the initila state.
      nfa1.accept.edge1 = nfa1.initial
      newnfa = nfa(initial,accept)
      nfastack.append(newnfa)
    elif c =='*':
      #Kleen star * matches a sequence of zero or more
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

  # Shunt and compile the regular expression.
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

#Print tests to the console
for i in infixes:
  for s in strings:
    print(match(i,s),i,s)

"""Start of GUI"""
#Submit Func
def submit_Func():
  #store the infix file string to the entered_text variable and remove the commas ","".
  #store the file string to the entered_text1 variable and remove the commas ",".
  entered_text=textEntry.get()
  entered_text1=textEntry1.get()
  infix_split = entered_text.split(',')
  string_split = entered_text1.split(',')

  for i in infix_split:
    for s in string_split:
      try:
        result=match(i,s)
        if result==0:
          result="False"+"\r\n"
        elif result==1:
          result="True"+"\r\n"
      except:
        result="Infix Field Must be Filled!"+"\r\n"
      #Print error message to the output box
      editArea.insert(END,result)

#Validate Func
def validate_Func():
   #store the infix file string to the entered_text variable and remove the commas ","".
  #store the file string to the entered_text1 variable and remove the commas ",".
  try:
    entered_text=InfixFilecontents
    entered_text1=StringFilecontents
    infix_split = entered_text.split(',')
    string_split = entered_text1.split(',')

    for i in infix_split:
      for s in string_split:
        try:
          result=match(i,s)
          if result==0:
            result="False"+"\r\n"
          elif result==1:
            result="True"+"\r\n"
        except:
          result="The Infix File is Empty!"+"\r\n"
        #Print result in the output box
        editArea.insert(END,result)
  except:
    result="You Must select An Infix And String Files!"+"\r\n"
  #Print error mesaage to the output box
  editArea.insert(END,result)


window = Tk()

window.title("Thompson Algorithm G00352031")
#Lenght and width of the window
window.geometry("600x600")
window.configure(background="black")
#Label
Label (window, text="Enter Infix Seperated By Commas:",bg="black",fg="Orange",font="non 12 bold").grid(row=1,column=0,sticky=W)

#Label
Label (window, text="Select An Infix File:",bg="black",fg="Orange",font="non 12 bold").grid(row=1,column=1)

#Entry TextField
textEntry= Entry(window,width=45,bg="white")
textEntry.grid(row=2,column=0,sticky=W)

#Select an Infix file function to read from,and txt as a default file
def select_Infix():
  #Declare InfixFilecontents as a global variable
  global InfixFilecontents
  window.filename1 =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("jpeg files","*.jpg"),("all files","*.*")))
  f_Infix=open(window.filename1, "r")
  if f_Infix.mode == 'r':
    InfixFilecontents =f_Infix.read()

  
#Select Infix String button
selectInfix= Button(window, text="Select InFix File",bg="Green",fg="Orange",width=12,command=select_Infix).grid(row=2,column=1)

#Label
Label (window, text="Enter Strings Seperated By Commas:",bg="black",fg="Orange",font="non 12 bold").grid(row=3,column=0,sticky=W)

#Label
Label (window, text="Select String File:",bg="black",fg="Orange",font="non 12 bold").grid(row=3,column=1)

#Entry TextField
textEntry1= Entry(window,width=45,bg="white")
textEntry1.grid(row=4,column=0,sticky=W)

#Select a String  file to read from and txt as the default file type
def select_String():
  #Declare StringFilecontents as a global variable.
  global StringFilecontents
  window.filename2 =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("jpeg files","*.jpg"),("all files","*.*")))
  f_String=open(window.filename2, "r")
  if f_String.mode == 'r':
    StringFilecontents =f_String.read()


#Select Sring button
selectString= Button(window, text="Select String File",bg="Green",fg="Orange",width=12,command=select_String).grid(row=4,column=1)

#Submit Button
subBtn= Button(window, text="SUBMIT",bg="Green",fg="Orange",width=6,command=submit_Func).grid(row=5,column=0,sticky=W)

#Validate Button
vdBtn= Button(window, text="VALIDATE",bg="Orange",fg="Red",width=8,command=validate_Func).grid(row=5,column=1)

#Label
Label (window, text="See Your Output Below.",bg="black",fg="Orange",font="non 12 bold").grid(row=6,column=0,sticky=W)

#Text box with scrollbar
#Code to do the scroll bar gotten from stack over flow
#https://stackoverflow.com/questions/17657212/how-to-code-the-tkinter-scrolledtext-module
output = Frame(window,width=80, height=80,bg = 'blue',
                  borderwidth=1, relief="sunken")
scrollbar = Scrollbar(output) 
editArea = Text(output, width=70, height=25, wrap="word",
                   yscrollcommand=scrollbar.set,
                   borderwidth=0, highlightthickness=0,background="Gray",fg="Blue")
scrollbar.config(command=editArea.yview)
scrollbar.pack(side="right", fill="y")
editArea.pack(side="left", fill="both", expand=True)
output.place(x=10,y=30)
output.grid(row=7,column=0,columnspan=2,sticky=W)


#Exit func
def close_window():
  window.destroy()
  exit()
#Exit Button
exitBtn= Button(window, text="EXIT",bg="Red",fg="Orange",width=4,command=close_window).grid(row=20,column=0,sticky=E)
app=Frame(window)

#Clear func
#Clear the output box at the start
def clear_output():
  editArea.delete(0.0,END)

#Clear output Textbox button
clearBtn= Button(window, text="CLEAR",bg="Green",fg="Orange",width=6,command=clear_output).grid(row=20,column=0,sticky=W)

#Save to file Func
def save_to_file():
  file = open("Output.txt", "w")
  file.write(editArea.get(1.0,END)) 
  file.close()
#Clear output Textbox button
saveBtn= Button(window, text="SAVE",bg="Orange",fg="Red",width=4,command=save_to_file).grid(row=20,column=0)

#The main loop
window.mainloop()



