#A file that removes comments in Python scripts. This is useful to reduce the
#size of the game file to save space on the calculator. Empty lines are also
#removed but comments after code aren't. Example:
#print("Hello, world") #This comment isn't removed

#Imported the needed sys module
import sys

#The function that writes the help message and informs the user about the usage
#of this script
def PrintHelpMessage():
	print("Script usage:")
	print("Use \"python\" on Windows and \"python3\" on Linux")
	print("python3 CommentRemover.py [script name] [output file]")

#Check if the number of command-line arguments is right. Two arguments are
#expected (plus one because the python script name is in the arguments).
if len(sys.argv) != 3:
	#If there are two arguments and the second one is "--help", show the
	#message that shows how to use this script and exit the script
	if len(sys.argv) == 2 and sys.argv[1] == "--help":
		PrintHelpMessage()
		exit()
	else:
		#The number of arguments is wrong. Show the help message and exit the
		#program.
		print("Invalid script usage\n")
		PrintHelpMessage()
		exit()

#Try to open the input file
lines = []
try:
	f = open(sys.argv[1], "r")
	#Read every line of the file
	lines = f.readlines()
	#Close the file
	f.close()
except:
	#Error opening the input file. Warn the user and exit the program.
	print("Error opening the input file. Aborting . . .")
	exit()

#Try to open the output file to write to it
try:
	f = open(sys.argv[2], "w")
except:
	#Failed to open the output file. Warn the use and exit the script.
	print("Error opening the output file. Aborting . . .")
	exit()

#Remove he comments for every line in the file
for i in range(len(lines)):
	#Remove the spaces and tabs in the beginning and end of the line
	t = lines[i].strip()
	#If the line isn't empty and the first character after the spaces and tabs
	#isn't a "#" (this line is not a comment), add this line to the file
	if len(t) >= 1:
		if t[0] != "#":
			f.write(lines[i])
#Close the file
f.close()
