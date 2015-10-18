# codeArtifacts jknag2 deliverable1.py #####
# Jae Hyung Kang + jkang2 + section B ####
# -*- coding: utf-8 -*- #####

from Tkinter import *
import time, random, copy
from eventBasedAnimationClass import EventBasedAnimationClass

startTime = time.time()

# 200 to 400 lines of decent code demonstrating proficiency in
# Tkinter and other modules or problems required to 
# make this game

# random module required to randomly place zombies on the map

# beginner, intermediate and expert levels of difficulty
# levels go until 20 (more zombies and new weapons appear every level)

# below is somewhat of a working demo with the moving hero in the middle

class Boxhead(EventBasedAnimationClass):

	def __init__(self, width=500, height=500):
		self.width = width
		self.height = height
		self.timerDelay = 1000
		self.cx = self.width / 2.0
		self.cy = self.height / 2.0
		self.p1x = self.width / 2.0
		self.p1y = self.height / 2.0
		self.r = 10
		self.moveDistance = 10
		self.isGameOver = True
		self.singlePlayerMode = True
		self.twoPlayerMode = False
		self.level = 0
		self.allZombiesDead = False
		self.lastMove = None
		self.bulletInAir = False
		self.startScreenText = '''Welcome to Boxhead.
Press any button to begin''' 

	def onKeyPressed(self, event):
		moveD = self.moveDistance
		if self.isGameOver:
			# make that any button pressed does whatever
			self.isGameOver = False
		else:
			if event.keysym == 'space':
				print 'shoot bullet!!!'
				# shooting animation incomplete
				self.shootBullet()
			elif event.keysym == 'Up':
				# move box up
				self.p1y -= moveD
				self.lastMove = event.keysym
			elif event.keysym == 'Down':
				# move box down
				self.p1y += moveD
				self.lastMove = event.keysym
			elif event.keysym == 'Right':
				self.p1x += moveD
				self.lastMove = event.keysym
			elif event.keysym == 'Left':
				self.p1x -= moveD
				self.lastMove = event.keysym


	def shootBullet(self):
		# for now pistol shooting animation
		self.bx = self.cx
		self.by = self.cy
		print 'bx, by', (self.bx, self.by)
		r = self.r
		print 'self.lastMove', self.lastMove
		if self.lastMove == 'Up':
			self.canvas.create_line(self.bx, self.by, self.bx,
									self.by-r)
			self.bulletInAir = True
			print 'bulletInAir', self.bulletInAir
			self.by -= r
			print 'self.by', self.by
		elif self.lastMove == 'Down':
			self.canvas.create_line(self.bx, self.by, self.bx,
									self.by+r)
			self.bulletInAir = True
			self.by += r
		elif self.lastMove == 'Left':
			self.canvas.create_line(self.bx, self.by,
									self.bx+r, self.by)
			self.bulletInAir = True
			self.bx += r
		elif self.lastMove == 'Right':
			self.canvas.create_line(self.bx, self.by,
									self.bx-r, self.by)
			self.bulletInAir = True
			self.bx -= r


	def bulletOnCanvas(self):
		bx = self.bx
		by = self.by
		if 0 < bx < self.width and 0 < by < self.height:
			return True
		else:
			return False

	def onTimerFired(self): 
		if not self.bulletOnCanvas:
			self.bulletInAir = False
		elif self.bulletInAir:
			self.shootBullet()

	def confirmZombiesAliveOrDead(self):
		pass

	def drawZombies(self):
		# draw the zombies depending on the level
		level = self.level
		greyZombie = GreyZombie(self.canvas)
		redZombie = RedZombie(self.canvas)
		for gZombie in xrange(2**(level+1)):
			greyZombie.drawZombie(greyZombie.color)
		for rZombie in xrange(level%4):
			redZombie.drawZombie(redZombie.color)

	def drawStartScreen(self):
		# draw the start screen when self.isGameOver
		cx = self.cx
		cy = self.cy
		#basic start screen for now
		# later there will be options to choose from 
		# like difficulty of AI or different maps
		self.canvas.create_text(cx, cy,
								text=self.startScreenText,
								font='Arial 20 bold')

	def redrawAll(self):
		self.canvas.delete(ALL)
		if self.isGameOver:
			# start screen
			self.drawStartScreen()
		if not self.isGameOver:
			if self.singlePlayerMode:
				player1 = Player1(self.canvas)
				player1.drawPlayer(self.p1x, self.p1y)
				# self.drawZombies() 
			elif self.twoPlayerMode:
				# not yet
				pass


class Player1(Boxhead):

	def __init__(self, canvas):
		Boxhead.__init__(self)
		self.canvas = canvas
		self.r = 10
		self.timerDelay = 250
		self.moveDistance = 10

	def drawPlayer(self, px, py):
		r = self.r
		self.canvas.create_rectangle(px-r, py-r, px+r, py+r, fill='green')
		# for now the players and the zombies will be represented as boxes
		# in this case, our player1 is a green box

class Zombie(Boxhead):

	def __init__(self, canvas):
		Boxhead.__init__(self)

	def placeZombie(self):
		self.zx = random.randint(0, self.width - self.r)
		self.zy = random.randint(0, self.height - self.r)

	def drawZombie(self, color):
		self.placeZombie()
		(zx, zy) = (self.zx, self.zy)
		print '(zx, zy)', (zx, zy)
		r = self.r
		self.canvas.create_rectangle(zx-r, zy-r, zx+r, zy+r,
									fill=color)

class GreyZombie(Zombie):
	# the weakest zombies but the most common

	def __init__(self, canvas):
		Zombie.__init__(self, canvas)
		self.canvas = canvas
		self.color = 'grey'
	

class RedZombie(Zombie):
	# stronger zombie

	def __init__(self, canvas):
		Zombie.__init__(self, canvas)
		self.canvas = canvas
		self.color = 'red'

def playBoxhead():
	boxheadGame = Boxhead()
	boxheadGame.run()

playBoxhead()

# #############################################
###############################################
# below is OOP code from previous hw that
# demonstrates my proficiency with event based programming
# and OOP

from basicAnimationClass import BasicAnimationClass

class FarmGame(BasicAnimationClass):
	
	def __init__(self, rows, cols):
		margin = 70
		cellSize = 30
		canvasWidth = 2*margin + cols*cellSize
		canvasHeight = 2*margin + rows*cellSize
		super(FarmGame, self).__init__(canvasWidth, canvasHeight)
		(self.rows, self.cols) = (rows, cols)
		self.width = canvasWidth
		self.height = canvasHeight
		self.helpScreenOn = False
		self.emptyColor = 'green3'
		self.field = self.generateField()
		self.margin = margin
		self.cellSize = cellSize
		self.cellWidth = 4 #width of the lines of the cell
		self.accountBalance = 0
		self.selectedRow = 0
		self.selectedCol = 0
		self.appleList = []
		self.riceList = []
		self.cropList = []
		self.textColor = 'blue'
		self.text = """ Press H for help screen
Use Arrow Keys to move around field
Press A to plant an Apple crop
Press R to plant a rice crop
Press V to harvest selected crops
"""
		self.additionalText = """Your crops change color two times before
they can be fully harvested!
Also make sure to use the select tool when trying to harvest!"""

	def generateField(self):
		field = []
		rows = self.rows
		cols = self.cols
		for row in xrange(rows):
			field.append([])
			for col in xrange(cols):
				field[row] += [self.emptyColor]
		return field

	def onTimerFired(self):
		field = self.field
		appleList = self.appleList
		riceList = self.riceList
		for apple in appleList:
			if time.time() - apple.startTime > apple.harvestTime:
				# if harvest time passed, change color
				field[apple.row][apple.col] = apple.harvestColor
			elif time.time() - apple.startTime >= (apple.harvestTime / 2.0):
				# half passed? mid color
				field[apple.row][apple.col] = apple.midColor
		for rice in riceList:
			# etc
			if time.time() - rice.startTime > rice.harvestTime:
				field[rice.row][rice.col] = rice.harvestColor
			elif time.time() - rice.startTime >= rice.harvestTime / 2.0:
				field[rice.row][rice.col] = rice.midColor
		self.cropList = self.appleList + self.riceList

	def isHarvested(self, crop):
		if time.time() - crop.startTime > crop.harvestTime:
			# if the time passed is larger than crop harvest time
			return True
		else:
			return False

	def harvestCrop(self, row, col):
		field = self.field
		cropList = self.cropList
		(selectedRow, selectedCol) = (self.selectedRow, self.selectedCol)
		riceList = self.riceList
		appleList = self.appleList
		for crop in cropList:
			if crop.row == selectedRow and crop.col == selectedCol:
				if self.isHarvested(crop):
					field[selectedRow][selectedCol] = self.emptyColor
					self.accountBalance += crop.sellingPrice
					self.cropList.remove(crop) #remove from crop list
					# and either appleList or riceList 
					if type(crop) == Apple:
						self.appleList.remove(crop)
					else:
						self.riceList.remove(crop)


print 'endTime =', time.time() - startTime, 'seconds'