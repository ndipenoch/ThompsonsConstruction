# Mark Ndipenoch, 20/03/2013
# Shunting Yard Algorithm
# http://www.oxfordmathcenter.com/drupal7/node/628
# https://www.geeksforgeeks.org/infix-to-postfix-using-different-precedence-values-for-in-stack-and-out-stack/
# https://codeburst.io/conversion-of-infix-expression-to-postfix-expression-using-stack-data-structure-3faf9c212ab8

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

print(shunt("( ( A + B ) - C * ( D / E ) ) + F"))
    