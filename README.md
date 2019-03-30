# ThompsonsConstruction
Graph Theory Project
Once you lunch Python a GUI window will pop up.
You will have 2 alternatives, to either enter your inputs via entry boxes or read them from a file using file choosers/selectors.
Your input strings should be separated by commas ",", there's a label to tell you that.

If you decide to use the entry boxes, then the Infix field is mandatory or else you get an error message displayed in the output
box saying "Infix Field Must be Filled!".
After entry your input in both Infix and String fields, click on the button "SUBMIT" and your output will be display in the output box.

If you decide to read the Input from files, then you have to click on both the "Select InFix File" and "Select String File" buttons.
Upon clicking each of these buttons a file selector window will pop out to allow you to choose a file from your directory. The default 
file format is set up as ".txt" but you can change it to all file types.

Once you select both files, you can then click on the button "VALIDATE" and your out put will be displayed in the output box.

If you don't select any file and click on the validate button the error message "You Must select An Infix And String Files!" will be displayed in the output box.

If you select both files and the Infix file is empty, you will see this error message "The Infix File is Empty!" in the output box.

The strings in both files must be separated by commas ",".

Also, you can hard code the inputs directly in the code and the output will be displayed in the console window.

The results or output are shown/displayed in the output box(Text Area) which has a vertical scroll bar functionality.
The scroll bar will appear once the text have gone pass the height of the text area.
Also, you can print the output to a file upon clicking the "SAVE" button. This file is found in the project folder and is call Output.txt.

At the bottom just after the the text area are three buttons:
- "CLEAR" to clear the output text area.
- "SAVE"  to save or write your output to a file.
- "EXIT" to exit the application gracefully.


When the project was first given I didn't know exactly what to do.
I watched and followed every video posted by the lecturer weekly.
Then after the first video directly related to the project, I started getting an idea of what to do but it was only on the 20th March that I started coding up the solutions.
The lecturers videos, were very clear, easy to understand and follow. That help me to understand the project better.

I did some research on-line, to see how this can be done in other programming languages, what are they use for, what other operators can I add to my solution, what are the advantages and disadvantages of 
Thompson's algorithm.

I got a good understanding on how to code the solution and could easily add any operator once I know what the operator does.

I also did some research on Shunting Yard algorithm, I added other operators and some with the same precedence and handle them in the code accordingly.

I ran a few tests on both the Shunting Yard and Thompson algorithms to make sure the work and produce the same outcome as on documents found on-line.

I also did some matching tests to match test my program.

I designed a GUI from tkinter which is a standard Python library.
I wanted to present my project as an application which is user friendly, and self explanatory with easy tools/functionalities to use.

The biggest issues I face during the life cycle of this project are :
 -Trying go get the meaning of other operators other like "$", "^". I found a few on-line but they were just comments and not official documents, So I didn't use them.
 - How to declare a variable as static or global, I found the solution on-line by using the keyword "global".
  


