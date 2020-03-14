#Import the needed modules
import random
import math

#A function that checks if the system the game is running on is a calculator or
#a PC. Due to the lack of enums in CASIO's Python interpreter, constant values
#are used instead.
CASIO = 0
PYTHON = 1
def GetSystemType():
	#Try to import a module that isn't available on CASIO calculators. If that
	#succeeds, the program is running on a computer. If it doesn't, it is
	#running on a calculator.
	try:
		import os
		return PYTHON
	except:
		return CASIO

#A function that clears the screen in PCs. There is no error checking. The
#programmer must make sure the game is running on a PC.
def ClearScreen():
	import os
	#On POSIX systems, use the clear command
	if os.name == "posix":
		os.system("clear")
	elif os.name == "nt":
		#On Windows, use the cls command
		os.system("cls")
	#The screen doesn't get cleared in calculators because what is printed to
	#those must fill all the screen lines.

#A function that gets a number from the user in a range. It returns None if the
#number is invalid or not in the range. start and end are integers and the
#limits of the range.
def InputInteger(start : int, end : int):
	#Get input from the user to know the number they chose
	number = input(">")
	#Convert the user input to a number
	try:
		number = int(number)
		#The conversion to an integer was successful. See if the number is in
		#the allowed range for the options.
		if number >= start and number <= end:
			#The number is inside the range. Return it.
			return number
		else:
			#The number isn't in the range. Raise an exception.
			raise Exception()
	except:
		#The number conversion failed or it succeeded but the number wasn't in
		#the valid range. Return None.
		return None

#A function that asks the user to pick one of many options. There is no error
#checking. question must be a string and options must be an array of strings.
#system must be CASIO or PYTHON.
def UserQuestion(question : str, options : list, system : int):
	#Ask the user the question until their input is valid
	while True:
		#In PCs, clear the screen
		if system == PYTHON:
			ClearScreen()
		#Write the question
		print(question)
		#Write all the options
		for i in range(len(options)):
			#Write the option number and the option. 1 is added to the number
			#so that the options don't start as zero like in arrays.
			print(str(i + 1) + " - " + options[i])
		#If we are in a CASIO calculator, fill the remaining lines. Only six
		#out of the seven available lines can be filled with text because the
		#last line has to be used for user input.
		if system == CASIO:
			remaining = 6 - (len(options) + 1)
			for i in range(remaining):
				print("")
		#Ask the user to input a number between 1 and the number of options
		number = InputInteger(1, len(options))
		#If the number is valid, return it minus one because it must be an
		#index of the array
		if number is not None:
			return number - 1
		#The answer is invalid. Continue the loop and ask the user again.

#The possible state of a slot in the board. Due to the lack of enums in CASIO
#calculators, constants are used.
NO_PLAYER = 0
PLAYERX = 1
PLAYERO = 2

#Values needed for the return values of Board.PlayerAlmostWinning. They
#represent rows, columns and diagonals
ROW = 0
COLUMN = 1
DIAGONAL = 2

#A class that defines a game board
class Board:
	Slots = []
	
	#The constructor of a new board
	def __init__(self):
		#Initialize a board with nine slots
		self.Slots = [NO_PLAYER] * 9

	#A function that renders the board to the console
	def Render(self):
		#Print every line
		for i in range(3):
			#The string that will be printed
			text = ""
			for j in range(3):
				#Add the current slot to the string that will be printed based
				#on the player (or lack of) there
				if self.Slots[i * 3 + j] == NO_PLAYER:
					text += str(i * 3 + j + 1)
				elif self.Slots[i * 3 + j] == PLAYERX:
					text += "X"
				else:
					text += "O"
				#Unless this is the edge of the board, write a separator
				if j != 2:
					text += "|"
			#Print the line
			print(text)
			#Unless this is the edge of the board, write a separator
			if i != 2:
				print("-----")

	#Checks if a player won the game or if it is a tie. NO_PLAYER is returned
	#if it's a tie and None is returned if the game hasn't ended yet.
	def PlayerWon(self):
		#Check if either X or O won
		for player in [PLAYERX, PLAYERO]:
			#Check if a row is filled with the player's pieces
			for j in range(0, 9, 3):
				if self.Slots[j] == self.Slots[j + 1] == self.Slots[j + 2] == \
					player:
					#The player filled this row. Return saying that they won
					return player
			#Check if a column is filled with the player's pieces
			for j in range(3):
				if self.Slots[j] == self.Slots[j + 3] == self.Slots[j + 6] == \
					player:
					#The player filled this column. Return saying that they won
					return player
			#Check if the diagonals are filled with the player's pieces
			if self.Slots[4] == player and (self.Slots[0] == self.Slots[8] == \
				player or self.Slots[2] == self.Slots[6] == player):
				#One of the diagonals is filled. Return saying that the player
				#won.
				return player
		#No match found. If the board is full, return that it's a tie.
		for i in range(9):
			if self.Slots[i] == NO_PLAYER:
				#There is an empty slot. It isn't a tie.
				return None
		#It's a tie.
		return NO_PLAYER

	#A function that returns the list of places in the board with no player on
	#them.
	def EmptyPlaces(self):
		#Create the list that will be returned
		ret = []
		#Loop through every piece in the board to find the ones without a
		#player on them
		for i in range(len(self.Slots)):
			if self.Slots[i] == NO_PLAYER:
				#There aren't players in the current place. Add it to the list.
				ret.append(i)
		#Return the list of places
		return ret

	#A function that checks if a player is almost winning (one piece away from
	#doing it). It returns an array. The first element is whether there is an
	#almost winning ROW, COLUMN or DIAGONAL. None is returned when the player
	#isn't a piece away from victory.
	def PlayerAlmostWinning(self, player : int):
		#Check if any of the rows has 2 pieces from the player and no piece
		#from the other player
		for i in range(3):
			#The number of pieces from the player
			count = 0
			#The location an empty place in this row
			empty = -1
			for j in range(3):
				#Check for player pieces and enemy pieces
				if self.Slots[i * 3 + j] == player:
					#This is a piece from the player. Count it.
					count += 1
				elif self.Slots[i * 3 + j] == InversePlayer(player):
					#This is a piece from the enemy. This row can't be
					#completed. Set count to -1. That way, it won't get to 2
					#and this row won't be a place the player can win at.
					count = -1
				else:
					#This place isn't filled. Take note of it.
					empty = i * 3 + j
			#Check if the row has 2 player pieces and no enemy pieces
			if count == 2:
				#It does. Return this row and the place missing
				return [ROW, empty]
		#Check if any of the columns has 2 pieces from the player and no piece
		#from the other player
		i = 0
		for j in range(3):
			#The number of pieces from the player
			count = 0
			#The location an empty place in this column
			empty = -1
			for i in range(3):
				#Check for player pieces and enemy pieces
				if self.Slots[i * 3 + j] == player:
					#This is a piece from the player. Count it.
					count += 1
				elif self.Slots[i * 3 + j] == InversePlayer(player):
					#This is a piece from the enemy. This column can't be
					#completed. Set count to -1. That way, it won't get to 2
					#and this column won't be a place the player can win at.
					count = -1
				else:
					#This place isn't filled. Take note of it.
					empty = i * 3 + j
			#Check if the column has 2 player pieces and no enemy pieces
			if count == 2:
				#It does. Return this row and the place missing
				return [COLUMN, empty]
		#Check if the first diagonal (left to right, top to bottom) is a place
		#where the player is a move away from winning at
		i = 0
		#The number of pieces from the player
		count = 0
		#The location an empty place in this diagonal
		empty = -1
		for i in range(3):
			#Check for player pieces and enemy pieces
			if self.Slots[i * 3 + i] == player:
				#This is a piece from the player. Count it.
				count += 1
			elif self.Slots[i * 3 + i] == InversePlayer(player):
				#This is a piece from the enemy. This diagonal can't be
				#completed. Set count to -1. That way, it won't get to 2
				#and this diagonal won't be a place the player can win at.
				count = -1
			else:
				#This place isn't filled. Take note of it.
				empty = i * 3 + i
		#Check if the diagonal has 2 player pieces and no enemy pieces
		if count == 2:
			#It does. Return this row and the place missing
			return [DIAGONAL, empty]
		#Check if the second diagonal (left to right, bottom to top) is a place
		#where the player is a move away from winning at
		i = 0
		#The number of pieces from the player
		count = 0
		for i in range(3):
			#Check for player pieces and enemy pieces
			if self.Slots[(i + 1) * 3 - i - 1] == player:
				#This is a piece from the player. Count it.
				count += 1
			elif self.Slots[(i + 1) * 3 - i - 1] == InversePlayer(player):
				#This is a piece from the enemy. This diagonal can't be
				#completed. Set count to -1. That way, it won't get to 2
				#and this diagonal won't be a place the player can win at.
				count = -1
			else:
				#This place isn't filled. Take note of it.
				empty = (i + 1) * 3 - i - 1
		#Check if the diagonal has 2 player pieces and no enemy pieces
		if count == 2:
			#It does. Return this row and the place missing
			return [DIAGONAL, empty]
		return None

#If the user is playing single or multi player. These are constants due to the
#lack of enums in CASIO's Python interpreter
SINGLEPLAYER = 0
MULTIPLAYER = 1

#The difficulties of the AI
EASY = 0
MEDIUM = 1
HARD = 2

#A function that returns the other player. If the player fed is PLAYERX,
#PLAYERO will be returned and vice-versa.
def InversePlayer(player : int):
	if player == PLAYERX:
		return PLAYERO
	else:
		return PLAYERX

#The functions responsible for running the singleplayer AI.
#Takes in the game board and the AI player
def EasyAI(board : Board, current : int):
	#The AI in easy mode only picks a random place where to put its piece. Find
	#all empty spaces
	empty = board.EmptyPlaces()
	#Place a piece in a random empty place
	board.Slots[empty[random.randrange(len(empty))]] = current

def MediumAI(board : Board, current : int):
	#Check if the AI is one step away from winning
	win = board.PlayerAlmostWinning(current)
	if win is not None:
		#The player is one step away from winning. Fill the remaining piece.
		board.Slots[win[1]] = current
	else:
		#The AI isn't a step away from winning. Check if the other player is.
		win = board.PlayerAlmostWinning(InversePlayer(current))
		if win is not None:
			#The other player is one step away from winning. Block their move
			#by placing a piece.
			board.Slots[win[1]] = current
		else:
			#There is nothing to complete or block. Play as easy AI.
			EasyAI(board, current)

#This AI isn't that good by itself. It is used in HardAI(). This function
#also takes in the number of times the AI has played.
def AdvancedMediumAI(board : Board, current : int, count : int):
	#Check if the AI is one step away from winning.
	win = board.PlayerAlmostWinning(current)
	if win is not None:
		#The player is one step away from winning. Fill the remaining piece.
		board.Slots[win[1]] = current
	else:
		#The AI isn't a step away from winning. Check if the other player is.
		win = board.PlayerAlmostWinning(InversePlayer(current))
		if win is not None:
			#The other player is one step away from winning. Block their move
			#by placing a piece.
			board.Slots[win[1]] = current
		else:
			#There is nothing to complete or block. If the AI is playing first
			#and this is the second turn, place a piece in the opposite corner.
			if count == 1:
				board.Slots[0] = current
				return

			#Get all places where it is possible to place a piece at.
			empty = board.EmptyPlaces()
			#Calculate the number of possible winning outcomes of a piece.
			final = []
			lowest = 100
			for i in range(len(empty)):
				#The number of impossibilities for this piece.
				impossibilities = 0
				#Check if the row the piece is at has no pieces from the enemy
				#player. Get the beginning of the row.
				begginning = (empty[i] // 3) * 3
				for j in range(begginning, begginning + 3):
					if board.Slots[j] == InversePlayer(current):
						#There's a piece from the other player. This row is
						#impossible.
						impossibilities += 1
				#Do the same for columns. I found no formula for calculating
				#the start of a column so if elses are used.
				if empty[i] < 3:
					begginning = empty[i]
				elif empty[i] < 6:
					begginning = empty[i] - 3
				else:
					begginning = empty[i] - 6
				for j in range(begginning, begginning + 7, 3):
					if board.Slots[j] == InversePlayer(current):
						#There's a piece from the other player. This column is
						#impossible.
						impossibilities += 1
				#Check if this place is in the first diagonal
				if empty[i] == 0 or empty[i] == 4 or empty[i] == 8:
					#It is. Check if there isn't an enemy piece in the first
					#diagonal.
					if board.Slots[0] == InversePlayer(current) or \
						board.Slots[4] == InversePlayer(current) or \
						board.Slots[8] == InversePlayer(current):
						#This diagonal has an enemy piece.
						impossibilities += 1
				else:
					#This place isn't in the first diagonal. Filling the first
					#diagonal would be impossible.
					impossibilities += 1
				#Check if this place is in the second diagonal
				if empty[i] == 2 or empty[i] == 4 or empty[i] == 6:
					#It is. Check if there isn't an enemy piece in the this
					#diagonal.
					if board.Slots[2] == InversePlayer(current) or \
						board.Slots[4] == InversePlayer(current) or \
						board.Slots[6] == InversePlayer(current):
						#This diagonal has an enemy piece.
						impossibilities += 1
				else:
					#This place isn't in the second diagonal. Filling the
					#second diagonal would be impossible.
					impossibilities += 1
				#If this piece has less impossibilities than previous pieces,
				#remove those from the list and mark this as the lowest
				#impossibility
				if impossibilities < lowest:
					final = []
					lowest = impossibilities
				if impossibilities == lowest:
					#If this is the lowest impossibility, add it to the list
					final.append(empty[i])
			#Place a piece in a random empty place
			board.Slots[final[random.randrange(len(final))]] = current

#HardAI also takes in whether the AI player is the first or not and the number
#of times it has played
def HardAI(board : Board, current : int, IsFirst : bool, count : int):
	if IsFirst:
		#Check if the AI is one step away from winning.
		win = board.PlayerAlmostWinning(current)
		if win is not None:
			#The player is one step away from winning. Fill the remaining piece
			board.Slots[win[1]] = current
		else:
			#The AI isn't a step away from winning. Check if the other player
			#is
			win = board.PlayerAlmostWinning(InversePlayer(current))
			if win is not None:
				#The other player is one step away from winning. Block their
				#move by placing a piece.
				board.Slots[win[1]] = current
			else:
				#The AI is the first to play and there's nothing to block or
				#complete. Use the corner strategy. Try to place a piece in a
				#corner.
				if count != 0:
					#This is the second or third turn. Place the next piece
					#differently depending on where the place the enemy placed
					#its piece
					if board.Slots[4] == InversePlayer(current):
						#The enemy played in the middle of the board. It's
						#impossible to do the corner strategy so, play as
						#advanced medium AI from now on.
						AdvancedMediumAI(board, current, count)
					#If the other player places a piece in certain places,
					#pick the bottom-left corner
					elif board.Slots[0] == InversePlayer(current) or \
						board.Slots[1] == InversePlayer(current) or \
						board.Slots[2] == InversePlayer(current) or \
						board.Slots[3] == InversePlayer(current) or \
						board.Slots[5] == InversePlayer(current):
						if count == 2:
							#This is the third play. Place the other corner
							#based on the enemy pieces.
							if board.Slots[0] == InversePlayer(current) or\
								board.Slots[3] == InversePlayer(current):
								board.Slots[2] = current
							else:
								board.Slots[0] = current
						else:
							#This is the second turn. Play like so.
							board.Slots[6] = current
					else:
						#Place the other piece on the top-right corner. This
						#only happens when a piece is played at 8 (7 in the
						#code)
						board.Slots[2] = current
				else:
					#Place a piece in the corner because this is the 2nd turn.
					board.Slots[8] = current
	else:
		#If the AI isn't the first player, the corner strategy cannot be used.
		#Play like an improved medium AI. Use -1 to inform that the AI isn't
		#the first playing.
		AdvancedMediumAI(board, current, -1)

#The entry-point of the program
def Main():
	#Get the system type to know if the screen should be cleared
	system = GetSystemType()
	#Ask the user whether to play in single or multi player
	mode = UserQuestion("Choose the mode:", [ "Singleplayer", "Multiplayer" ] \
		, system)
	#In singleplayer, ask for the player and the difficulty
	if mode == SINGLEPLAYER:
		player = UserQuestion("Choose the player", [ "X", "O" ], system) + 1
		difficulty = UserQuestion("Choose the difficulty:", [ "Easy", "Medium"\
			, "Hard"], system)
	#Pick a random player to start
	FirstPlayer = random.randint(PLAYERX, PLAYERO)
	current = FirstPlayer
	#Create a board
	board = Board()
	#Keep track of the number of times the AI has played
	PlayCount = 0
	#Start the game loop
	while True:
		#If the game ended (win or tie), show it and end the game loop
		won = board.PlayerWon()
		if won is not None:
			#In PCs, clear the screen
			if system == PYTHON:
				ClearScreen()
			board.Render()
			#Print a different message depending on who won (or it it's a tie)
			if won == NO_PLAYER:
				print("It's a tie")
			elif won == PLAYERX:
				print("Player X won")
			else:
				print("PLAYER O won")
			break
		#The game hasn't ended yet. Continue the game loop

		#In singleplayer, check if it's the AI playing so that the board
		#doesn't get rendered unnecessarily.
		if mode == SINGLEPLAYER and current == InversePlayer(player):
			#Let the AI play. Call a different AI function based on the
			#difficulty
			if difficulty == EASY:
				EasyAI(board, current)
			elif difficulty == MEDIUM:
				MediumAI(board, current)
			else:
				HardAI(board, current, FirstPlayer == current, PlayCount)
				PlayCount += 1
			#Advance to the next player
			current = InversePlayer(current)
		else:
			#In PCs, clear the screen for every player move
			if system == PYTHON:
				ClearScreen()

			#It's the user playing. Render the board and ask where to place the
			#piece.
			board.Render()
			#Ask the user where to place the piece based on the current player
			if current == PLAYERX:
				print("Piece from X at:")
			else:
				print("Piece from O at:")
			place = InputInteger(1, 9)
			#If the integer is valid and the slot isn't already used, place a
			#piece and switch to the next player
			if place is not None and board.Slots[place - 1] == NO_PLAYER:
				#Remove one from the index because arrays start at 0
				board.Slots[place - 1] = current
				current = InversePlayer(current)


#If this script is being run and not included, run the main function. Because
#CASIO calculators don't support __name__, always run the Main function in
#calculators.
if __name__ == "__main__" or GetSystemType() == CASIO:
	Main()