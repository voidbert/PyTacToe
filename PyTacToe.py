import random
import math

#A functions that gets user input and converts it into an integer. It returns
#None if the number is invalid
def InputInteger():
	#Get the user input
	val = input(">")
	#Convert the input to an integer
	try:
		val = int(val)
		#Return the value
		return val
	except:
		#Unable to convert string to integer. Return None
		return None

#Represents the device in which the program is being run.
#Because enums aren't supported in Casio's Python, constants are used.
CASIO = 0
PYTHON = 1

#Analyse if the program is running on a computer or a calculator
System = PYTHON
try:
	#Try to import the "os" module. If we were able to do that, we're running
	#on a computer
	import os
except:
	#Unable to import the "os" module. Because it doesn't exist on Casio
	#calculators, we can assume that the program is running in one of them.
	System = CASIO

#A function that clears the screen based on the current system
def Clear():
	if System == PYTHON:
		#Clear the screen depending on the operating system
		if os.name == "nt":
			#Use the Windows "cls" command to clear the console
			os.system("cls")
		else:
			#Use the POSIX "clear" command to clear the console
			os.system("clear")
	else:
		#On calculators, print 8 empty lines because there's no way to clear
		#the screen
		for i in range(8):
			print("")

#The information in a place in the board
NO_PLAYER = 0
PLAYERX = 1
PLAYERO = 2

#Create the game board
Board = [
	[NO_PLAYER, NO_PLAYER, NO_PLAYER],
	[NO_PLAYER, NO_PLAYER, NO_PLAYER],
	[NO_PLAYER, NO_PLAYER, NO_PLAYER]
]

#A function that renders the board to the console
def RenderBoard():
	#Render every line
	for i in range(3):
		line = ""
		#Render every piece slot in the line
		for j in range(3):
			#Add the character of the piece depending on the player there
			if Board[i][j] == NO_PLAYER:
				#Print the slot number
				line += str(i * 3 + j + 1)
			elif Board[i][j] == PLAYERO:
				line += "O"
			elif Board[i][j] == PLAYERX:
				line += "X"
			#Unless this is the edge of the board, draw the division between
			#pieces
			if j != 2:
				line +=	"|"
		print(line)
		#Unless this is the edge of the board, draw the division between lines
		if i != 2:
			print("-----")

#A function that checks if any player has won
def PlayerWon():
	#Check if any of the players won
	for i in range(1, 3):
		#Check if a row is filled up
		for j in range(0, 3):
			if Board[j] == [i, i, i]:
				#The row is filled. Return that this player won
				return i
		#Check if a column is filled up
		for j in range(0, 3):
			if Board[0][j] == i and Board[1][j] == i and Board[2][j] == i:
				#The column is filled
				return i
		#Check if any of the corners is done
		if Board[1][1] == i and ((Board[0][0] == i and Board[2][2] == i) or \
		(Board[2][0] == i and Board[0][2] == i)):
			#The player won
			return i
	#Check if the board is full and nobody won
	for i in range(0, 3):
		for j in range(0, 3):
			if Board[i][j] == NO_PLAYER:
				#There's an empty slot. The game hasn't ended yet.
				return -1
	#It's a tie
	return NO_PLAYER

#A function that checks if a player is going to win
ROW = 0
COLUMN = 1
DIAGONAL = 2
def PlayerAlmostWinning(player):
	#Check if a row is almost filled up
	for i in range(0, 3):
		count = 0
		for j in range(0, 3):
			if Board[i][j] == player:
				count += 1
			elif Board[i][j] != NO_PLAYER:
				count = -10
		if count == 2:
			#Two pieces filled. Return this	row
			return [ROW, i]
	#Check if a column is almost filled up
	for i in range(0, 3):
		count = 0
		for j in range(0, 3):
			if Board[j][i] == player:
				count += 1
			elif Board[j][i] != NO_PLAYER:
				count = -10
		if count == 2:
			#Two pieces filled. Return this	column
			return [COLUMN, i]
	#Check if diagonals are almost filled up
	count = 0
	for i in range(0, 3):
		if Board[i][i] == player:
			count += 1
		elif Board[i][i] != NO_PLAYER:
			count = -10	
	if count == 2:
		return [DIAGONAL, 0]
	count = 0
	for i in range(0, 3):
		if Board[2 - i][i] == player:
			count += 1
		elif Board[2 - i][i] != NO_PLAYER:
			count = -10
	if count == 2:
		return [DIAGONAL, 1]			

#Due to the lack of enums, single and multiplayer numbers
SINGLE_PLAYER = 1
MULTI_PLAYER = 2

#Know if the user wants single or multiplayer. Keep doing that if the user gets
#it wrong.
Players = -1
while True:
	#Clear the screen and ask the user
	Clear()
	print("Choose a mode:\n1 - Singleplayer\n2 - Multiplayer\n\n\n")
	#Get the user's response
	Players = InputInteger()
	#Check if the value is valid
	if Players == SINGLE_PLAYER or Players == MULTI_PLAYER:
		#It is. Break out of the loop
		break

#The difficulties of the AI
EASY = 1
MEDIUM = 2
HARD = 3

#If the user chose singleplayer, tell them to choose a player
Player = -1
Difficulty = -1
if Players == SINGLE_PLAYER:
	#Know if the user wants	to play as the ball or as the cross
	while True:
		#Clear the screen and ask the user
		Clear()
		print("Choose a player:\n1 - X\n2 - O\n\n\n")
		#Get the user's response
		Player = InputInteger()
		#Check if the value is valid
		if Player == PLAYERX or Player == PLAYERO:
			#It is. Break out of the loop
			break

	#Choose the difficulty of the AI
	while True:
		#Clear the screen and ask the user
		Clear()
		print("Choose the difficulty:\n1 - Easy\n2 - Medium\n3 - Hard\n\n")
		#Get the user's response
		Difficulty = InputInteger()
		#Check if the value is valid
		if Difficulty == EASY or Difficulty == MEDIUM or Difficulty == HARD:
			#It is. Break out of the loop
			break

#Pick the first player to play
Current = random.randint(1, 2)

#The functions that run the game's AI
def EasyAI():
	#Pick a random place where to place the piece. Create a list of empty slots
	free = []
	for i in range(0, 3):
		for j in range(0, 3):
			if Board[i][j] == NO_PLAYER:
				free.append([i, j])

	#Count the possible lines, columns and diagonals that can branch out of a
	#piece. Keep track of the lowest impossibility count and create the final
	#array.
	lowest = 10
	final = []
	for i in range(0, len(free)):
		impossible = 0
		#Check if there are no enemy pieces in the same row
		for j in range(0, 3):
			if Board[free[i][0]][j] != NO_PLAYER and \
				Board[free[i][0]][j] != Current:
				impossible += 1
				break
		#Check if there are no enemy pieces in the same column
		for j in range(0, 3):
			if Board[j][free[i][1]] != NO_PLAYER and \
				Board[j][free[i][1]] != Current:
				impossible += 1
				break
		#Check if there are enemy pieces in the same diagonal. First, check if
		#the piece is in a diagonal
		if free[i][0] == free[i][1]:
			#First diagonal. Check if there are no enemy pieces.
			for j in range(0, 3):
				if Board[j][j] != NO_PLAYER and Board[j][j] != Current:
					impossible += 1
					break
		else:
			#No diagonal possibility
			impossible += 1
		if free[i][0] == 2 - free[i][1]:
			#Second diagonal. Check if there are no enemy pieces.
				for j in range(0, 3):
					if Board[j][2 - j] != NO_PLAYER and \
						Board[j][2 - j] != Current:
						impossible += 1
						break
		else:
			#No diagonal possibility
			impossible += 1
		#Update the lowest impossibility	
		if impossible < lowest:
			lowest = impossible
			final = []
			final.append(free[i])
		elif impossible == lowest:
			final.append(free[i])
	#Pick a random place
	place = final[random.randrange(0, len(final))]
	#Place a piece there
	Board[place[0]][place[1]] = Current

def MediumAICore():
	#Check if the player is going to win in the next play
	winning = PlayerAlmostWinning(Current)
	if winning is not None:
		#The AI is going to win. Place the piece.
		if winning[0] == ROW:
			#Fill the row with pieces (because two of them are filled by the
			#AI, it will be only placing a piece)
			Board[winning[1]][0] = Current
			Board[winning[1]][1] = Current
			Board[winning[1]][2] = Current
		elif winning[0] == COLUMN:
			#Fill the colum with pieces (because two of them are filled by the
			#AI, it will be only placing a piece)
			Board[0][winning[1]] = Current
			Board[1][winning[1]] = Current
			Board[2][winning[1]] = Current
		elif winning[1] == 0:
			#Fill the first diagonal
			Board[0][0] = Current
			Board[1][1] = Current
			Board[2][2] = Current
		elif winning[1] == 1:
			#Fill the second diagonal
			Board[0][2] = Current
			Board[1][1] = Current
			Board[2][0] = Current
	else:
		#Know if the other player is about to win
		if Current == PLAYERX:
			winning = PlayerAlmostWinning(PLAYERO)
		else:
			winning = PlayerAlmostWinning(PLAYERX)
		#If the other player is almost winning, block their move
		if winning is not None:
			#The player is almost winning. Fill the empty place
			if winning[0] == ROW:
				#Fill the empty space in the almost winning row
				for i in range(0, 3):
					if Board[winning[1]][i] == NO_PLAYER:
						Board[winning[1]][i] = Current
			elif winning[0] == COLUMN:
				#Fill the empty space in the almost winning column
				for i in range(0, 3):
					if Board[i][winning[1]] == NO_PLAYER:
						Board[i][winning[1]] = Current
			elif winning[1] == 0:
				#Fill the empty space in the first diagonal
				for i in range(0, 3):
					if Board[i][i] == NO_PLAYER:
						Board[i][i] = Current
			elif winning[1] == 1:
				#Fill the empty space in the second diagonal
				for i in range(0, 3):
					if Board[2 - i][i] == NO_PLAYER:
						Board[2 - i][i] = Current	
		else:
			#No mandatory move executed
			return 0

def MediumAI():
	#Check and execute mandatory moves (quick wins or loss prevention)
	if MediumAICore() == 0:
		#No mandatory moves. Place a piece in a random place
		EasyAI()

PlayCount = 0
PlayHard = True

def HardAI(IsFirst):
	global PlayHard
	#Check and execute mandatory moves (quick wins or loss prevention)
	if MediumAICore() == 0:
		#No mandatory moves. Run the hard AI
		if IsFirst and PlayHard:
			if PlayCount == 0:
				Board[2][2] = Current
			elif PlayCount == 2:
				if Board[1][1] != NO_PLAYER:
					PlayHard = False
					EasyAI()
				elif Board[0][0] != NO_PLAYER or Board[1][0] != NO_PLAYER or \
					Board[0][2] != NO_PLAYER or Board[1][2] != NO_PLAYER:
					Board[2][0] = Current
				elif Board[2][0] != NO_PLAYER or Board[2][1] != NO_PLAYER \
					or Board[0][1] != NO_PLAYER:
					Board[0][2] = Current
			elif PlayCount == 4:
				if Board[2][0] == Current:
					if Board[0][0] != NO_PLAYER or Board[1][0] != NO_PLAYER:
						Board[0][2] = Current
					else:
						Board[0][0] = Current
				else:
					if Board[0][1] != NO_PLAYER:
						Board[2][0] = Current
					else:
						Board[0][0] = Current
		else:
			#We're not the first player so we can't use the corner strategy.
			#Play like normal
			EasyAI()

#Start the game loop
AIFirst = False
while True:
	#Clear the screen
	Clear()

	#Check if a player won the game
	winner = PlayerWon()
	if winner != -1:
		#Write that the player won
		if winner == PLAYERX:
			print("Player X won")
		elif winner == PLAYERO:
			print("Player O won")
		else:
			print("It's a tie")
		#Render the winning board
		RenderBoard()
		#Stop the game
		break
	
	#Render the board
	RenderBoard()
	#If the user is the one playing (always true in multiplayer)
	if Players == MULTI_PLAYER or Current == Player:
		#Ask the user where to place the piece
		if Current == PLAYERX:
			print("Piece from X at:")
		else:
			print("Piece from O at:")
		val = InputInteger()
		#Check if the integer is valid and if the slot is empty
		if val is not None and val >= 1 and val <= 9 and \
		Board[math.floor((val - 1) / 3)][(val - 1) % 3] == NO_PLAYER:
			#Add the piece
			Board[math.floor((val - 1) / 3)][(val - 1) % 3] = Current
			#Change the current player
			if Current == 1:
				Current = 2
				PlayCount += 1
			else:
				Current = 1
				PlayCount += 1
	else:
		#Run different AIs depending on the difficulty
		if Difficulty == EASY:
			EasyAI()
		elif Difficulty == MEDIUM:
			MediumAI()
		elif Difficulty == HARD:
			if PlayCount == 0:
				AIFirst = True
			HardAI(AIFirst)
		#Pass control onto the next player
		if Current == PLAYERX:
				Current = PLAYERO
				PlayCount += 1
		else:
			Current = PLAYERX
			PlayCount += 1