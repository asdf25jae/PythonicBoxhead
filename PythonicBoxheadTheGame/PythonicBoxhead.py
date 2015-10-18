# boxheadTermProjectJaeKang.py #
# Jae Hyung Kang + jkang2 + section B ####
# -*- coding: utf-8 -*- #####

from Tkinter import *
import time, random, copy, os
from newEventBasedAnimationClass import NewEventBasedAnimationClass

# NewEventBasedAnimationClass based off EventBasedAnimationClass
# off course notes
# resizability function code was added by resizableDemo.py
# off course notes as well

def readFile(filename, mode="rt"):
    # rt = "read text"
    with open(filename, mode) as fin:
        return fin.read()

def writeFile(filename, contents, mode="wt"):
    # wt = "write text"
    with open(filename, mode) as fout:
        fout.write(contents)

# THE GIF FILES IN THE FOLDER ARE NECESSARY FOR THE 
# DEMO TO WORK

class Boxhead(NewEventBasedAnimationClass):


	# some parts of this code such as the rocket, mine explosion
	# the idea to draw blood and a line for the uzi bullet
	# was taken from Ben Rothschild and his version of 
	# boxhead with Tkinter
	# no direct code taken from him however
	# his video URL https://www.youtube.com/watch?v=fHDnyeCYdac

	def __init__(self, width=600, height=600): #window is resizable
		self.width = width
		self.height = height
		self.margin = max(self.width/10.0, self.height/10.0)
		self.timerDelay = 100
		self.backgroundColor = 'bisque2'
		self.selectedWeapon = 'Pistol'	
		self.levelOfDifficulty = None
		self.cx = self.width / 2.0
		self.cy = self.height / 2.0
		self.p1x = self.width / 2.0
		self.p1y = self.height / 2.0
		self.pressedKeys = set()
		self.gZombieList = []
		self.rZombieList = []
		self.ammoList = []
		self.weaponList = []
		self.healthBoostList = []
		self.bloodList = []
		self.mineList = []
		self.bBottom = 2*self.margin #back bottom/ back right
		self.bRight = 3/2.0*self.margin #for the back button on high score page
		self.r = 10
		self.mineRadius = 75
		self.attackRadius = 20
		self.devilAttackRadius = 150
		self.moveDistance = 10
		self.shotgunAttackRange = 100
		self.player1Health = 100 #use this to draw health bar
		self.zombieHealth = 100
		self.greyZombieBonus = 100 #points added
		self.redZombieBonus = 250
		self.levelOfDifficulty = None #before selection
		self.lastMove = None
		self.gameStartScreen = True
		self.allOptionsSelectedForStart = False #level of difficulty selected
		self.isGameOver = False
		self.gameWon = False
		self.helpScreen = False
		self.allZombiesDead = False
		self.bulletInAir = False
		self.rocketInAir = False
		self.pauseGame = False
		self.highscoreScreen = False
		self.shouldBeDrawn = True
		self.beginnerHighlighted = False #for highlight in mouse motion
		self.intermediateHighlighted = False
		self.expertHighlighted = False
		self.highscoreHighlighted = False
		self.backHighlighted = False
		self.noAmmo = False
		self.startTimeOfShot = 0 #to make sure that there is a 
		self.endTimeOfShot = 0 # small offset of time between shots 
		self.level = 0
		self.score = 0
		self.highScore = self.getHighScore()
		self.finalLevel = 10 #changed later when difficulty is selected
		self.numberOfWeapons = 5
		self.minAmmoPacks = 0 #min/max # of items that can be added per level
		self.maxAmmoPacks = 2
		self.minHealthBoosts = 0
		self.maxHealthBoosts = 1
		self.minAddedHealth = 20
		self.maxAddedHealth = 60
		self.greyZombieDamageTaken = 25
		self.redZombieDamageTaken = 8
		self.greyZombieDamage = 2
		self.redZombieDamage = 5
		self.rpgRecoilDamage = 20 #when player is too close to rocket explosion
		self.specialCoeff = 8/5.0
		self.pistolRecoveryTime = 0.1
		self.shotgunRecoveryTime = 0.25
		self.mineExplosionTime = 3 #mine explodes after 3 seconds
		self.rpgRecoveryTime = 0.5
		self.pistolFactor = 1 #factor in damage
		self.uziFactor = 1/4.0
		self.shotgunFactor = 4
		self.mineFactor = 6
		self.rpgFactor = 8
		self.weaponIndex = 2 #in weapon list
		self.drawnIndex = 3
		self.ammoIndex = 4
		self.pistolIndex = 0
		self.uziIndex = 1
		self.shotgunIndex = 2
		self.mineIndex = 3
		self.rpgIndex = 4

	def onKeyPressed(self, event):
		weaponList = self.weaponList
		weaponIndex = self.weaponIndex
		drawnIndex = self.drawnIndex
		player1 = self.player1
		selectedWeapon = self.selectedWeapon 
		ammoIndex = self.ammoIndex
		selectedWeaponIndex = self.getWeaponIndex(selectedWeapon)
		if self.weaponList != [] and selectedWeaponIndex != None:
			ammoAmount = self.weaponList[selectedWeaponIndex][ammoIndex]
		if event.keysym not in self.pressedKeys:
			# based off keyEventsDemo.py off course notes
			self.pressedKeys.add(event.keysym)
		if self.isGameOver or self.gameWon:
			if self.score > self.highScore:
				# write score over highscore
				writeFile('boxheadHighscore.txt', str(self.score))
			self.__init__(self.width, self.height) #restart game
		elif self.calledForHelpScreen(event.keysym):
			# bring up help screen
			# this comes before event.keysym == 'p' because
			# this should be able to be called up even if
			# pause screen is on
			self.helpScreen = not self.helpScreen
		elif event.keysym == 'p' or event.keysym == 'P':
			self.pauseGame = not self.pauseGame
		elif not self.pauseGame:
			if event.keysym.isdigit():
				pressedNumber = int(event.keysym)
				if not weaponList[pressedNumber-1][drawnIndex]:
					# if item is not drawn on map or already eaten by player
					# change selected weapon
					self.selectedWeapon = weaponList[pressedNumber-1][weaponIndex]
			elif event.keysym == 'space' and ammoAmount > 0:
				self.startTimeOfShot = time.time()
				self.shoot(self.startTimeOfShot)
				self.weaponList[selectedWeaponIndex][ammoIndex] -= 1 #ammo 
			elif self.isArrowKey(event.keysym):
				self.movePlayer(event.keysym)

	def keyReleased(self, event):
		# based off keyEventsDemo.py off course notes
		if event.keysym in self.pressedKeys:
			self.pressedKeys.remove(event.keysym)

	def onTimerFired(self): 
		tenthSecond = 0.1
		self.checkIfItemsEaten()
		self.checkIfThereIsAmmo()
		if time.time() - self.startTimeOfShot > tenthSecond:
			self.bulletInAir = False
		if self.player1Health <= 0 and not self.gameStartScreen:
			# make it so that Game Over screen is displayed
			self.isGameOver = True
			self.allOptionsSelectedForStart = False
		elif self.levelOfDifficulty != None and not self.allOptionsSelectedForStart:
			# if start screen is on but difficulty hasnt been selected
			selectedLevel = self.levelOfDifficulty
			self.__init__(self.width, self.height)
			self.levelOfDifficulty = selectedLevel
			self.allOptionsSelectedForStart = True
			self.gameStartScreen = False
			self.checkIfScoreIsHighScore()
		if self.noZombies() and self.allOptionsSelectedForStart:
			# every level or when game is started
			self.level += 1
			if self.level > self.finalLevel:
				self.gameWon = True
			else:
				self.bloodList = []
				self.addZombies()
				self.addItems()

	def onMousePressed(self, event):
		# when self.gameStart and not self.allOptionsSelectedForStart
		# make it so that when clicked, the following value is activated
		(selectedX, selectedY) = (event.x, event.y)
		(left, right) = (self.left, self.right)
		(top1, bottom1) = (self.top1, self.bottom1)
		(top2, bottom2) = (self.top2, self.bottom2)
		(top3, bottom3) = (self.top3, self.bottom3)
		(top4, bottom4) = (self.top4, self.bottom4)
		if self.gameStartScreen and not self.allOptionsSelectedForStart:
			if left < selectedX < right:
				if top1 < selectedY < bottom1:
				 	# beginner difficulty selected
				 	self.levelOfDifficulty = 'Beginner'
				elif top2 < selectedY < bottom2:
				 	# intermediate difficulty selected
					self.levelOfDifficulty = 'Intermediate'
				elif top3 < selectedY < bottom3:
					# expert difficulty selected
					self.levelOfDifficulty = 'Expert'
				elif top4 < selectedY < bottom4:
					self.highscoreScreen = True
					self.gameStartScreen = False
		elif self.highscoreScreen:
			if 0 < selectedX < self.bRight and 0 < selectedY < self.bBottom:
				self.gameStartScreen = True
				self.highscoreScreen = False

	def mouseMotion(self, event):
		# use mouseMotion for the start screen
		# when player has to select difficulty
		(selectedX, selectedY) = (event.x, event.y)
		(left, right) = (self.left, self.right)
		(top1, bottom1) = (self.top1, self.bottom1)
		(top2, bottom2) = (self.top2, self.bottom2)
		(top3, bottom3) = (self.top3, self.bottom3)
		(top4, bottom4) = (self.top4, self.bottom4)
		self.setDefaultValuesBack()
		if self.gameStartScreen and not self.allOptionsSelectedForStart:
			# check to see what the player has chosen for difficulty
			# check to see if player has clicked on the help screen
			if left < selectedX < right:
				if top1 < selectedY < bottom1:
				 	# beginner difficulty selected
				 	self.beginnerHighlighted = True
				elif top2 < selectedY < bottom2:
				 	# intermediate difficulty selected
				 	self.intermediateHighlighted = True
				elif top3 < selectedY < bottom3:
					# expert difficulty selected
					self.expertHighlighted = True
				elif top4 < selectedY < bottom4:
					self.highscoreHighlighted = True

	def setDefaultValuesBack(self):
		self.beginnerHighlighted = False
		self.intermediateHighlighted = False
		self.expertHighlighted = False
		self.highscoreHighlighted = False

	def checkIfThereIsAmmo(self):
		selectedWeapon = self.selectedWeapon
		ammoIndex = self.ammoIndex
		selectedWeaponIndex = self.getWeaponIndex(selectedWeapon)
		try:
			if self.weaponList[selectedWeaponIndex][ammoIndex] != 0:
				self.noAmmo = False
			else:
				self.noAmmo = True
		except:
			pass

	def calledForHelpScreen(self, s):
		return s == 'h' or s == 'H'

	def isArrowKey(self, s):
		return s == 'Up' or s == 'Down' or s == 'Left' or s == 'Right'

	def isDiagonalMove(self, a):
		allArrowKeys = set(['Up', 'Down', 'Right', 'Left'])
		if a.issubset(allArrowKeys):
			return True
		else:
			return False

	def movePlayer(self, keysym):
		moveD = self.moveDistance
		pressedKeys = self.pressedKeys
		if (len(pressedKeys) >= 2 and self.isDiagonalMove(pressedKeys)):
			 # at least two keys held on at the same time
			 self.moveDiagonally()
		else:
			if keysym == 'Up' and self.p1y - moveD > 0:
				self.p1y -= moveD
			if keysym == 'Down' and self.p1y + moveD < self.height:
				self.p1y += moveD
			if keysym == 'Right' and self.p1x + moveD < self.width:
				self.p1x += moveD
			if keysym == 'Left' and self.p1x - moveD > 0:
				self.p1x -= moveD
			self.lastMove = keysym
			self.bulletInAir = False

	def doesntMoveOffScreenNE(self, px, py):
		moveD = self.moveDistance
		return py - moveD > 0 and px + moveD < self.width

	def doesntMoveOffScreenNW(self, px, py):
		moveD = self.moveDistance
		return py - moveD > 0 and px - moveD > 0

	def doesntMoveOffScreenSE(self, px, py):
		moveD = self.moveDistance
		return px + moveD < self.width and py + moveD < self.height

	def doesntMoveOffScreenSW(self, px, py):
		moveD = self.moveDistance
		return px - moveD > 0 and py + moveD < self.height

	def moveDiagonally(self):
		(px, py) = (self.p1x, self.p1y)
		moveD = self.moveDistance
		pressedKeys = self.pressedKeys
		if (pressedKeys == set(['Up', 'Right']) and
			 self.doesntMoveOffScreenNE(px, py)):
			# move northeast
			self.p1y -= moveD
			self.p1x += moveD
			self.lastMove = 'NorthEast'
		if (pressedKeys == set(['Up', 'Left']) and 
			self.doesntMoveOffScreenNW(px, py)):
			# move Northwest
			self.p1y -= moveD
			self.p1x -= moveD
			self.lastMove = 'NorthWest'
		if (pressedKeys == set(['Down', 'Right']) and 
			self.doesntMoveOffScreenSE(px, py)):
			# move southeast
			self.p1y += moveD
			self.p1x += moveD
			self.lastMove = 'SouthEast'
		if (pressedKeys == set(['Down', 'Left']) and 
			self.doesntMoveOffScreenSW(px, py)):
			# move southwest
			self.p1y += moveD
			self.p1x -= moveD
			self.lastMove = 'SouthWest'
		self.bulletInAir = False

	def damageGreyZombie(self, gZombie, factor):
		greyZombieDamageTaken = self.greyZombieDamageTaken
		gZombie[2] -= greyZombieDamageTaken*factor

	def deleteGreyZombie(self, zombie):
		zx = zombie[0]
		zy = zombie[1] 
		self.gZombieList.remove(zombie)
		self.bloodList += [[zx, zy]]
		self.score += self.greyZombieBonus

	def damageRedZombie(self, rZombie, factor):
		redZombieDamageTaken = self.redZombieDamageTaken
		rZombie[2] -= redZombieDamageTaken*factor

	def deleteRedZombie(self, zombie):
		zx = zombie[0]
		zy = zombie[1]
		self.rZombieList.remove(zombie)
		self.bloodList += [[zx, zy]]
		self.score += self.redZombieBonus

	def isInNorthWestPath(self, px, py, zx, zy):
		# checks with recursive call to see if
		# zombie is in the northwest diagonal path
		# of player
		r = 2*self.r
		if px < 0 or py < 0:
			# if px or py has gone off screen
			return False
		elif zx - r <= px <= zx + r and zy - r <= py <= zy + r:
			# if px and py are within a certain radius of zx, zy
			return True
		else:
			return self.isInNorthWestPath(px-1, py-1, zx, zy)
			# -1, -1 because northwest

	def isInNorthEastPath(self, px, py, zx, zy):
		r = 2*self.r
		if px > self.width or py < 0:
			return False
		elif zx - r <= px <= zx + r and zy - r <= py <= zy + r:
			return True
		else:
			return self.isInNorthEastPath(px+1, py-1, zx, zy)
			# +1, -1 because northeast

	def isInSouthWestPath(self, px, py, zx, zy):
		r = 2*self.r
		if px < 0 or py > self.height:
			return False
		elif zx - r <= px <= zx + r and zy - r <= py <= zy + r:
			return True
		else:
			return self.isInSouthWestPath(px-1, py+1, zx, zy)
			# -1, +1 because southwest

	def isInSouthEastPath(self, px, py, zx, zy):
		r = 2*self.r
		if px > self.width or py > self.height:
			return False
		elif zx - r <= px <= zx + r and zy - r <= py <= zy + r:
			return True
		else:
			return self.isInSouthEastPath(px+1, py+1, zx, zy)
			# +1, +1 because southeast

	def findClosestZombie(self, x, y, direction):
		# find the single zombie/devil that is closest 
		r = self.r
		closestZombie = [None, None]
		zombieList = self.gZombieList + self.rZombieList
		for zombie in zombieList:
			closestZombieX = closestZombie[0]
			closestZombieY = closestZombie[1]
			zx = zombie[0]
			zy = zombie[1]
			if direction == 'Up':
				if (y - zy > 0 and x - r < zx < x + r and zy > closestZombieY):
					# if zombie is above player, near playerX and 
					# closer to player than previous closestZombie
					closestZombie = [zx, zy]
			elif direction == 'Down':
				if (y - zy < 0 and x - r < zx < x + r):
					if (zy < closestZombieY or closestZombieY == None):
						# or closestZombieY == None because if None then
						# we can assume that zx, zy is the new closest zombie
						closestZombie = [zx, zy]
			elif direction == 'Left':
				if (x - zx > 0 and y - r < zy < y + r and zx > closestZombieX):
					closestZombie = [zx, zy]
			elif direction == 'Right':
				if (x - zx < 0 and y - r < zy < y + r):
					if (zx < closestZombieX or closestZombieX == None):
						closestZombie = [zx, zy]
			elif direction == 'NorthEast':
				if (self.isInNorthEastPath(x, y, zx, zy) and zy > closestZombieY):
					if (zx < closestZombieX or closestZombieX == None):
						closestZombie = [zx, zy]
			elif direction == 'NorthWest':
				if (self.isInNorthWestPath(x, y, zx, zy) and zy > closestZombieY): 
					if (zx < closestZombieX or closestZombieX == None):
						closestZombie = [zx, zy]
			elif direction == 'SouthEast':
				if (self.isInSouthEastPath(x, y, zx, zy) and zx > closestZombieX):
					if zy < closestZombieY or closestZombieY == None:
						closestZombie = [zx, zy]
			elif direction == 'SouthWest':
				if (self.isInSouthWestPath(x, y, zx, zy) and zx > closestZombieX):
					if zy < closestZombieY or closestZombieY == None:
						closestZombie = [zx, zy]
		return closestZombie

	def closestToPlayer(self, x, y, zx, zy, direction):
		(czx, czy) = self.findClosestZombie(x, y, direction)
		return (zx, zy) == (czx, czy)

	def damageZombiesHit(self, x, y, direction, factor):
		# use this to take the health off of zombies that were hit
		# with the bullet
		for gZombie in self.gZombieList:
			zx = gZombie[0]
			zy = gZombie[1]
			if self.closestToPlayer(x, y, zx, zy, direction):
				self.damageGreyZombie(gZombie, factor)
			if gZombie[2] < 0: #gZombieHealth below zero
				# zombie is now dead
				self.deleteGreyZombie(gZombie)
		for rZombie in self.rZombieList:
			zx = rZombie[0]
			zy = rZombie[1]
			if self.closestToPlayer(x, y, zx, zy, direction):
				self.damageRedZombie(rZombie, factor)
			if rZombie[2] < 0:
				self.deleteRedZombie(rZombie)

	def hitByShotgun(self, x, y, zx, zy, direction):
		r = self.shotgunAttackRange/4.0
		if (direction == 'Up' and 
			y - zy > 0 and
			x - r < zx < x + r):
			return True
		if (direction == 'Down' and
			y - zy < 0 and 
			x - r < zx < x + r):
			return True
		if (direction == 'Right' and
			x - zx < 0 and
			y - r < zy < y + r):
			return True
		if (direction == 'Left' and 
			x - zx > 0 and 
			y - r < zy < y + r):
			return True
		if (direction == 'NorthWest' and 
			self.isInNorthWestPath(x, y, zx, zy)):
			return True
		if (direction == 'NorthEast' and 
			self.isInNorthEastPath(x, y, zx, zy)):
			return True
		if (direction == 'SouthEast' and
			self.isInSouthEastPath(x, y, zx, zy)):
			return True
		if (direction == 'SouthWest' and
			self.isInSouthWestPath(x, y, zx, zy)):
			return True
		return False

	def withinShotgunRange(self, x, y, zx, zy, direction):
		shotgunAttackRange = self.shotgunAttackRange
		if direction == 'Up' or direction == 'Down':
			# up and down, so only zy matters
			return abs(y - zy) <= shotgunAttackRange
		elif direction == 'Left' or direction == 'Right':
			# only zx matters cause left and right
			return abs(x - zx) <= shotgunAttackRange
		elif (direction == 'SouthWest' or direction == 'SouthEast' or
			direction == 'NorthWest' or direction == 'NorthEast'):
			return (abs(x - zx) <= shotgunAttackRange and 
				abs(y - zy) <= shotgunAttackRange)
			# if attack was done diagonally then, zx and zy must both
			# be within shotgunAttackRange

	def damageZombiesHitByShotgun(self, x, y, direction, factor):
		# shotgun has a wider range and can hit several targets at once
		for gZombie in self.gZombieList:
			zx = gZombie[0]
			zy = gZombie[1]
			if (self.hitByShotgun(x, y, zx, zy, direction) and 
				self.withinShotgunRange(x, y, zx, zy, direction)):
				self.damageGreyZombie(gZombie, factor)
			if gZombie[2] < 0:
				# gZombie health below zero
				self.deleteGreyZombie(gZombie)
		for rZombie in self.rZombieList:
			zx = rZombie[0]
			zy = rZombie[1]
			if (self.hitByShotgun(x, y, zx, zy, direction) and 
					self.withinShotgunRange(x, y, zx, zy, direction)):
				self.damageRedZombie(rZombie, factor)
			if rZombie[2] < 0:
				self.deleteRedZombie(rZombie)

	def hitByExplosion(self, mx, my, zx, zy):
		# if zombie/monster within mineRadius
		mR = self.mineRadius
		return abs(mx - zx) <= mR and abs(my - zy) <= mR

	def damageZombiesHitByMine(self, mx, my):
		# damages the zombies hit by the mine
		mineFactor = self.mineFactor
		for gZombie in self.gZombieList:
			zx = gZombie[0]
			zy = gZombie[1]
			if self.hitByExplosion(mx, my, zx, zy):
				self.damageGreyZombie(gZombie, mineFactor)
			if gZombie[2] < 0: # if health below zero
				self.deleteGreyZombie(gZombie)
		for rZombie in self.rZombieList:
			zx = rZombie[0]
			zy = rZombie[1]
			if self.hitByExplosion(mx, my, zx, zy):
				self.damageRedZombie(rZombie, mineFactor)
			if rZombie[2] < 0: # if health below zero
				self.deleteRedZombie(rZombie)

	def damageZombiesHitByRPG(self, czx, czy, direction):
		rpgFactor = self.rpgFactor
		for gZombie in self.gZombieList:
			zx = gZombie[0]
			zy = gZombie[1]
			if self.hitByExplosion(czx, czy, zx, zy):
				self.damageGreyZombie(gZombie, rpgFactor)
			if gZombie[2] < 0: #gZombieHealth below zero
				# zombie is now dead
				self.deleteGreyZombie(gZombie)
		for rZombie in self.rZombieList:
			zx = rZombie[0]
			zy = rZombie[1]
			if self.hitByExplosion(czx, czy, zx, zy):
				self.damageRedZombie(rZombie, rpgFactor)
			if rZombie[2] < 0:
				self.deleteRedZombie(rZombie)

	def getWeaponIndex(self, weapon):
		if weapon == 'Pistol':
			return self.pistolIndex
		elif weapon == 'Uzi':
			return self.uziIndex
		elif weapon == 'Shotgun':
			return self.shotgunIndex
		elif weapon == 'Mine':
			return self.mineIndex
		elif weapon == 'RPG':
			return self.rpgIndex

	def getEndNW(self, px, py): 
		#EndOfShot so line can be drawn
		# for uzi shot NorthWestward
		if px > py:
			return (px-py, 0)
		elif px < py:
			return (0, py-px)
		else:
			# if px == py, then end of shot is (0, 0)
			return (0, 0)

	def getEndNE(self, px, py):
		# uzi shot NorthEastward
		(width, height) = (self.width, self.height)
		avgOfWH = (width+height)/2.0
		if py == 0 or px == width:
			return (px, py)
		elif px + py < avgOfWH:
			return (px+py, 0)
		elif px + py > avgOfWH:
			return (width, py-width+px)
		else:
			return (0, px+py)

	def getEndSW(self, px, py):
		(width, height) = (self.width, self.height)
		avgOfWH = (width+height)/2.0
		if px == 0 or py == height:
			return (px, py)
		elif px + py > avgOfWH:
			return (px-height+py, height)
		elif px + py < avgOfWH:
			return (0, px+py)
		else:
			return (0, height)

	def getEndSE(self, px, py):
		if px > py:
			return (self.width, self.width-px+py)
		elif py > px:
			return (self.height-py+px, self.height)
		else:
			return (self.width, self.height)

	def shoot(self, timeOfShot):
		selectedWeapon = self.selectedWeapon
		if selectedWeapon == 'Pistol':
			self.shootPistol()
		elif selectedWeapon == 'Uzi':
			self.shootUzi()
		elif selectedWeapon == 'Shotgun':
			self.shootShotgun()
		elif selectedWeapon == 'Mine':
			self.placeMine(timeOfShot)
		elif selectedWeapon == 'RPG':
			self.shootRPG()

	def shootPistol(self):
		# for now pistol shooting animation]
		# make it so that the bullet is just a line
		# that stays for a tenth of a second
		(px, py) = (self.p1x, self.p1y)
		pistolRecoveryTime = self.pistolRecoveryTime
		pistolFactor = self.pistolFactor
		if time.time() - self.endTimeOfShot > pistolRecoveryTime:
			(bx, by, bulletDirection) = (px, py, self.lastMove)
			self.bulletInAir = True
			self.damageZombiesHit(bx, by, bulletDirection, pistolFactor)
			self.endTimeOfShot = time.time()
			# endTimeOfShot is always taken so that we make sure
			# that there is a certiain buffer of time
			# before player can shoot again
			# just like in real life ;)

	def shootUzi(self):
		# put in reloading feature
		specialCoeff = self.specialCoeff
		uziFactor = self.uziFactor
		(px, py) = (self.p1x, self.p1y)
		r = self.r
		halfR = r/2.0
		doubleR = 2*r
		# tipOfGunX, tipOfGunY are the x y coords of the tip of the gun
		# when character is faced a certain way
		# specialCoeff is 5/8.0, a coefficient i found that works 
		if self.lastMove == 'Up':
			(tipOfGunX, tipOfGunY)  = (px + r, py - doubleR)
			(endOfShotX, endOfShotY) = (px + r, 0)
		if self.lastMove == 'Down':
			(tipOfGunX, tipOfGunY) = (px - r, py + r)
			(endOfShotX, endOfShotY) = (px - r, self.height)
		if self.lastMove == 'Left':
			(tipOfGunX, tipOfGunY) = (px - doubleR, py - r)
			(endOfShotX, endOfShotY) = (0, py - r)
		if self.lastMove == 'Right':
			(tipOfGunX, tipOfGunY) = (px + r, py)
			(endOfShotX, endOfShotY) = (self.width, py)
		if self.lastMove == 'NorthEast':
			(tipOfGunX, tipOfGunY) = (px + specialCoeff*r, py - r)
			(endOfShotX, endOfShotY) = self.getEndNE(tipOfGunX, tipOfGunY)	
		if self.lastMove == 'NorthWest':
			(tipOfGunX, tipOfGunY) = (px - r, py - doubleR)
			(endOfShotX, endOfShotY) = self.getEndNW(tipOfGunX, tipOfGunY)
		if self.lastMove == 'SouthEast':
			(tipOfGunX, tipOfGunY) = (px + r, py + r)
			(endOfShotX, endOfShotY) = self.getEndSE(tipOfGunX, tipOfGunY)
		if self.lastMove == 'SouthWest':
			(tipOfGunX, tipOfGunY) = (px - specialCoeff*r, py + halfR)
			(endOfShotX, endOfShotY) = self.getEndSW(tipOfGunX, tipOfGunY)
		self.canvas.create_line(tipOfGunX, tipOfGunY, endOfShotX,
								endOfShotY)
		# draw the uzi line from tip of gun to the end of the shot
		(bx, by, bulletDirection) = (px, py, self.lastMove)
		self.bulletInAir = True
		self.damageZombiesHit(bx, by, bulletDirection, uziFactor)
		self.endTimeOfShot = time.time()

	def shootShotgun(self):
		# shoot an invisible shot that does
		# a ton of damage in a short range
		# kills grey zombie in two hit
		# kills red Zombie in 4 hits
		shotgunFactor = self.shotgunFactor
		shotgunRecoveryTime = self.shotgunRecoveryTime
		(px, py) = (self.p1x, self.p1y)
		if time.time() - self.endTimeOfShot > shotgunRecoveryTime:
			(bx, by, bulletDirection) = (px, py, self.lastMove)
			self.bulletInAir = True
			self.damageZombiesHitByShotgun(bx, by, bulletDirection,
							 shotgunFactor)
			self.endTimeOfShot = time.time()

	def placeMine(self, timeOfDrop):
		# place a mine on playerx and playery
		# (player coordinates)
		# that will explode after 3 seconds
		lastMove = self.lastMove
		(mx, my) = (self.p1x, self.p1y)
		self.mineList += [[mx, my, timeOfDrop]]

	def drawMines(self):
		mineList = self.mineList
		mineExplosionTime = self.mineExplosionTime
		mineImage = self.image_mine
		for mine in mineList:
			mineX = mine[0]
			mineY = mine[1]
			timeOfDrop = mine[2]
			if time.time() - timeOfDrop >= mineExplosionTime:
				# if 3 seconds has passed
				self.damageZombiesHitByMine(mineX, mineY)
				self.mineList.remove(mine)
				self.drawExplosion(mineX, mineY)
			else:
				self.canvas.create_image(mineX, mineY, image=mineImage)
				# draw the mine


	def drawExplosion(self, mineX, mineY):
		#  draw an Orange circle that appears
		# after the mine explodes, or rpg hits the closest zombie
		mR = self.mineRadius
		self.canvas.create_oval(mineX-mR, mineY-mR, 
							mineX+mR, mineY+mR, fill='orange red', 
							outline='black')

	def shootRPG(self): 
		# no visuals except the explosion that happens, at the first 
		# zombie/monster it hits
		(px, py) = (self.p1x, self.p1y)
		rpgRecoveryTime = self.rpgRecoveryTime
		rpgFactor = self.rpgFactor
		rpgR = self.mineRadius
		(czx, czy) = self.findClosestZombie(px, py, self.lastMove)
		if time.time() - self.endTimeOfShot >= rpgRecoveryTime:
			(bx, by, bulletDirection) = (px, py, self.lastMove)
			self.damageZombiesHitByRPG(czx, czy, self.lastMove)
			self.rocketInAir = True
			self.endTimeOfShot = time.time()
			(self.czx, self.czy) = (czx, czy)
		if abs(czx - px) <= rpgR and abs(czy - py) <= rpgR:
			# if player is too close and is within the explosion 
			# then player takes some recoil damage
			self.player1Health -= self.rpgRecoilDamage

	def drawRocketExplosions(self):
		rocketInAir = self.rocketInAir
		if rocketInAir:
			try:
				# see if there is a closestZombie
				(czx, czy) = (self.czx, self.czy)
				self.drawExplosion(czx, czy)
				self.rocketInAir = False
			except:
				# if not
				pass

	def noZombies(self):
		return self.gZombieList == [] and self.rZombieList == []

	def determineNewWeapon(self):
		levelTier = self.level / (self.finalLevel/self.numberOfWeapons)
		# Tier 0 gives a Pistol # Tier 1 gives an Uzi # Tier 2 Shotgun
		# Tier 3 Mine # Tier 4 RPG
		TierZero = 0
		TierOne = 1
		TierTwo = 2
		TierThree = 3
		TierFour = 4
		if levelTier == TierZero:
			# give pistol if not already in list
			return 'Pistol'
		elif levelTier == TierOne:
			return 'Uzi'
		elif levelTier == TierTwo: 
			return 'Shotgun'
		elif levelTier == TierThree:
			return 'Mine'
		elif levelTier == TierFour:
			return 'RPG'

	def addAmmo(self, weapon):
		# adds a certain amount of ammo
		# depending on selectedWeapon
		if weapon == 'Pistol':
			return 50
		elif weapon == 'Uzi':
			return 200
		elif weapon == 'Shotgun':
			return 50
		elif weapon == 'Mine':
			return 20
		elif weapon == 'RPG':
			return 25

	def placeItem(self, weapon):
		# return [random x coord, random y coord, weapon, bool value, ammo#]
		width = self.width
		height = self.height
		r = self.r
		weaponX = random.randint(r, width-r)
		weaponY = random.randint(r, height-r)
		ammoAmount = self.addAmmo(weapon)
		shouldBeDrawn = self.shouldBeDrawn
		return [weaponX, weaponY, weapon, shouldBeDrawn, ammoAmount]

	def addItems(self):
		self.addWeaponItems()
		self.addAmmoItems()
		self.addHealthBoostItems()

	def addWeaponItems(self):
		weaponList = self.weaponList
		newWeapon = self.determineNewWeapon()
		if len(weaponList) != 0:
			# if there are weapons already in list
			lastWeapon = len(weaponList) - 1
			if not newWeapon in weaponList[lastWeapon]:
				self.weaponList += [self.placeItem(newWeapon)]
		else:
			# add the pistol, which is a default item
			# not to be drawn, because player has it at level1
			# and should not have to pick it up to use it
			self.weaponList += [self.placeItem(newWeapon)]
			firstItem = 0
			drawnIndex = self.drawnIndex
			self.weaponList[firstItem][drawnIndex] = False

	def addAmmoItems(self):
		r = self.r
		selectedWeapon = self.selectedWeapon
		newlyAddedAmmo = self.addAmmo(selectedWeapon)
		shouldBeDrawn = self.shouldBeDrawn
		(minAmmoPacks, maxAmmoPacks) = (self.minAmmoPacks, self.maxAmmoPacks)
		numberOfNewAmmoPacks = random.randint(minAmmoPacks, maxAmmoPacks)
		# randomly chosen number 
		for ammoPack in xrange(numberOfNewAmmoPacks):
			ammoX = random.randint(r, self.width-r)
			ammoY = random.randint(r, self.height-r)
			self.ammoList += [[ammoX, ammoY]]

	def addHealthBoostItems(self):
		r = self.r
		minHealthBoosts = self.minHealthBoosts
		maxHealthBoosts = self.maxHealthBoosts
		numberOfHealthBoosts = random.randint(minHealthBoosts, maxHealthBoosts)
		# again randomly chosen
		minAddedHealth = self.minAddedHealth
		maxAddedHealth =  self.maxAddedHealth
		for healthBoost in xrange(numberOfHealthBoosts):
			healthX = random.randint(r, self.width-r)
			healthY = random.randint(r, self.height-r)
			addedHealth = random.randint(minAddedHealth, maxAddedHealth)
			# added health is random as well
			self.healthBoostList += [[healthX, healthY, addedHealth]]

	def playerTouchesItem(self, ix, iy, px, py):
		r = 2*self.r #touch Radius
		if ix-r <= px <= ix+r and iy-r <= py <= iy+r:
			return True
		else:
			return False

	def checkIfItemsEaten(self):
		# checked under onTimerFired
		# this obviously checks if p1x and p1y collide
		# with weaponX and weaponY to see
		# if the items have been 
		weaponList = self.weaponList
		p1x = self.p1x
		p1y = self.p1y
		drawnIndex = self.drawnIndex
		selectedWeapon = self.selectedWeapon
		ammoIndex = self.ammoIndex
		selectedWeaponIndex = self.getWeaponIndex(selectedWeapon)
		for weapon in weaponList:
			# check if the item coordinates
			# collide with p1x and p1y
			weaponX = weapon[0]
			weaponY = weapon[1]
			if self.playerTouchesItem(weaponX, weaponY, p1x, p1y):
				weapon[drawnIndex] = False #so shouldBeDrawn is False
		for ammo in self.ammoList:
			ammoX = ammo[0]
			ammoY = ammo[1]
			newAmmo = self.addAmmo(selectedWeapon)
			if self.playerTouchesItem(ammoX, ammoY, p1x, p1y):
				self.weaponList[selectedWeaponIndex][ammoIndex] += newAmmo
				self.ammoList.remove(ammo)
		for healthBoost in self.healthBoostList:
			healthX = healthBoost[0]
			healthY = healthBoost[1]
			addedHealth = healthBoost[2]
			if self.playerTouchesItem(healthX, healthY, p1x, p1y):
				self.player1Health += addedHealth
				if self.player1Health > 100:
					# if playerHealth is above 100 after eating
					self.player1Health = 100
				self.healthBoostList.remove(healthBoost)

	def drawNewWeaponItems(self):
		# draw the New WeaponItems on screen
		# new weapon items are always RED
		weaponList = self.weaponList
		r = self.r
		count = 0
		for weapon in weaponList:
			count += 1
			if count == 1:
				continue #because pistol is not drawn
				# and instead, is the default weapon
			shouldBeDrawn = weapon[3]
			weaponX = weapon[0]
			weaponY = weapon[1]
			if shouldBeDrawn:
				self.canvas.create_rectangle(weaponX-r, weaponY-r,
							weaponX+r, weaponY+r, fill='red')

	def drawAmmo(self):
		# where the ammo is drawn onto the map 
		# adds a certain amount of ammo depending on selectedWeapon
		# to whatever player is holding
		ammoList = self.ammoList
		r = self.r
		for ammo in ammoList:
			ammoX = ammo[0]
			ammoY = ammo[1]
			self.canvas.create_rectangle(ammoX-r, ammoY-r, 
							ammoX+r, ammoY+r, fill='black')

	def drawHealthBoosts(self):
		# items that when picked up, 
		# health is reboosted
		healthBoostList = self.healthBoostList
		r = self.r
		for healthBoost in healthBoostList:
			healthX = healthBoost[0]
			healthY = healthBoost[1]
			self.canvas.create_rectangle(healthX-r, healthY-r, 
							healthX+r, healthY+r, fill='green')

	def drawItems(self):
		# draw all Items on screen
		self.drawNewWeaponItems() # red boxes
		self.drawAmmo() # black boxes
		self.drawHealthBoosts() # green boxes

	def determineByDifficulty(self):
		levelOfDifficulty = self.levelOfDifficulty
		if levelOfDifficulty == 'Beginner':
			self.finalLevel = 10 # max level
			return (1, 3) 
		elif levelOfDifficulty == 'Intermediate':
			self.finalLevel = 15 # max level
			return (2, 2)
		elif levelOfDifficulty == 'Expert':
			self.finalLevel = 20 # max level
			return (3, 1)
		# first return value is the power to which greyZombies are produced
		# second return value is the divisor or the number of levels
		# for every red Zombie or devil produced

	def addZombies(self):
		level = self.level
		r = self.r
		zombieHealth = self.zombieHealth
		(gZombiePower, rZombieDivisor) = self.determineByDifficulty()
		for gZombie in xrange(level**gZombiePower):
			gZombieXCoord = random.randint(r, self.width-r)
			gZombieYCoord = random.randint(r, self.height-r)
			self.gZombieList += [[gZombieXCoord, gZombieYCoord, zombieHealth, None]]
			# direction is None because we don't know what direction it
			# moves in yet
		for rZombie in xrange(level/rZombieDivisor):
			rZombieXCoord = random.randint(r, self.width-r)
			rZombieYCoord = random.randint(r, self.height-r)
			self.rZombieList += [[rZombieXCoord, rZombieYCoord, zombieHealth, None]]

	def drawGreyZombie(self, gzx, gzy, direction):
		# here we obviously draw the grey zombies
		# with its image
		zombieImage = self.determineGreyZombieImage(direction)
		self.canvas.create_image(gzx, gzy, image=zombieImage)

	def drawRedZombie(self, rzx, rzy, direction):
		# same with devil or red zombie we call it here
		zombieImage = self.determineRedZombieImage(direction)
		self.canvas.create_image(rzx, rzy, image=zombieImage)

	def drawBlood(self):
		bloodList = self.bloodList
		bloodImage = self.image_blood
		for deadZombie in bloodList:
			zx = deadZombie[0]
			zy = deadZombie[1]
			self.canvas.create_image(zx, zy, image=bloodImage)

	def drawZombies(self):
		# draw the zombies depending on the level
		level = self.level
		greyZombie = GreyZombie(self.canvas)
		redZombie = RedZombie(self.canvas)
		for gZombie in self.gZombieList:
			gzx = gZombie[0]
			gzy = gZombie[1]
			direction = gZombie[3] #direction zombie moves in
			self.drawGreyZombie(gzx, gzy, direction)
		for rZombie in self.rZombieList:
			rzx = rZombie[0]
			rzy = rZombie[1]
			direction = rZombie[3]
			self.drawRedZombie(rzx, rzy, direction)

	def zombiesAttack(self):
		greyZombie = self.greyZombie
		redZombie = self.redZombie
		gZombieList = self.gZombieList
		rZombieList = self.rZombieList
		attackR = self.attackRadius
		devilAttackR = self.devilAttackRadius
		for gIndex in xrange(len(gZombieList)):
			gzx = gZombieList[gIndex][0]
			gzy = gZombieList[gIndex][1]
			gZombieHealth = gZombieList[gIndex][2]
			self.gZombieList[gIndex] = greyZombie.moveTowardsPlayer(gzx, gzy,
										 self.p1x, self.p1y, gZombieHealth,
										 greyZombie.color)
			# change x, y coordinates of gZombie and direction
			if abs(gzx - self.p1x) < attackR and abs(gzy - self.p1y) < attackR:
				# zombie attacks player
				self.player1Health -= self.greyZombieDamage
		for rIndex in xrange(len(rZombieList)):
			rzx = rZombieList[rIndex][0]
			rzy = rZombieList[rIndex][1]
			rZombieHealth = rZombieList[rIndex][2]
			self.rZombieList[rIndex] = redZombie.moveTowardsPlayer(rzx, rzy,
									 	self.p1x, self.p1y, rZombieHealth,
									 	redZombie.color)
			if abs(rzx - self.p1x) < attackR and abs(rzy - self.p1y) < attackR:
				# red zombie or devil attacks player
				self.player1Health -= self.redZombieDamage

	def drawZombiesHealthBar(self):
		# draw the health bars of each zombie
		greyZombie = GreyZombie(self.canvas)
		redZombie = RedZombie(self.canvas)
		for gZombie in self.gZombieList:
			gzx = gZombie[0]
			gzy = gZombie[1]
			gZombieHealth = gZombie[2]
			greyZombie.drawHealthBar(gzx, gzy, gZombieHealth)
		for rZombie in self.rZombieList:
			# draw the health bars of the red Zombies 
			rzx = rZombie[0]
			rzy = rZombie[1]
			rZombieHealth = rZombie[2]
			redZombie.drawHealthBar(rzx, rzy, rZombieHealth)

	def displayGameScreen(self):
		# display level, score and whatever
		level = self.level
		score = self.score
		# level on top right
		# score on top left
		cx = self.cx
		width = self.width
		height = self.height
		margin = max(self.width/15.0, self.height/15.0)
		selectedWeaponIndex = self.getWeaponIndex(self.selectedWeapon)
		ammoIndex = self.ammoIndex
		levelText = 'Level: %d' % level
		scoreText = 'Score: %d' % score
		weaponText = 'Weapon: %s' % self.selectedWeapon
		helpText = 'Press h for help'
		ammoText = 'Ammo: %d' % self.weaponList[selectedWeaponIndex][ammoIndex]
		self.canvas.create_text(width-margin, margin,
						text=levelText, font='Helvetica 15 bold')
		# shows level in top right
		self.canvas.create_text(2*margin, margin, 
						text=scoreText, font='Helvetica 15 bold')
		# shows current score in top left
		self.canvas.create_text(2*margin, height-margin, text=weaponText,
							font='Helvetica 15 bold')
		# shows selected weapon in bottom left
		self.canvas.create_text(width-margin, height-margin, text=ammoText,
							font='Helvetica 15 bold')
		# shows ammo in bottom right
		self.canvas.create_text(cx, margin, text=helpText, 
						font='Helvetica 15 bold')
		# at top, says press h for help

	def displayPauseScreen(self):
		cx = self.cx
		cy = self.cy
		pauseScreenText = 'Game Paused\nPress P to resume'
		self.canvas.create_text(cx, cy/2.0, text=pauseScreenText,
						font='Arial 20 bold')

	def drawStartScreen(self):
		# draw the start screen when self.isGameOver
		(cx, cy) = (self.cx, self.cy)
		(width, height) = (self.width, self.height)
		halfCY = cy/2.0
		fiveEighthsCY = cy*5/8.0
		eighthHeight = cy/8.0
		startScreenText = '''BOXHEAD''' 
		smallerText = 'Pick a level of difficulty to begin'
		# difficulty level
		self.canvas.create_text(cx, halfCY,
								text=startScreenText,
								font='Arial 30 bold')
		self.canvas.create_text(cx, fiveEighthsCY, 
								text=smallerText, 
								font='Arial 12 bold')
		cyCoeff = 3/8.0
		self.left = left = cx/2.0 #left and right are always same 
		self.top1 = top1 = cyCoeff*height
		self.right = right = cx*3/2.0
		self.bottom1 = bottom1 = top1 + eighthHeight
		# three separate difficulty levels to choose from
		# beginner, intermediate, expert
		self.top2 = top2 = cy
		self.bottom2 = bottom2 = top2 + eighthHeight
		self.canvas.create_rectangle(left, top1, right, bottom1, outline='black', 
						width=3) # beginner box
		(beginnerX, beginnerY) = ((left+right)/2.0, (top1+bottom1)/2.0)
		self.canvas.create_rectangle(left, top2, right, bottom2, outline='black',
							width=3) #intermediate box
		self.top3 = top3 = cy + 2*eighthHeight
		self.bottom3 = bottom3 =  top3 + eighthHeight
		self.top4 = top4 = cy + 4*eighthHeight
		self.bottom4 = bottom4 = top4 + eighthHeight
		intermediateY = (top2+bottom2)/2.0
		self.canvas.create_rectangle(left, top3, right, bottom3, outline='black', 
							width=3) # expert box
		self.canvas.create_rectangle(left, top4, right, bottom4, outline='black',
							width=3) #view high score box
		expertY = (top3+bottom3)/2.0
		highscoreY = (top4+bottom4)/2.0
		# write the text in the boxes
		self.canvas.create_text(beginnerX, beginnerY, text='Beginner',
						 font='Arial 12 bold', fill='red')
		self.canvas.create_text(beginnerX, intermediateY, text='Intermediate', 
						font='Arial 12 bold', fill="red")
		self.canvas.create_text(beginnerX, expertY, text='Expert', 
						font='Arial 12 bold', fill='red')
		self.canvas.create_text(beginnerX, highscoreY, text='View High Score',
							font='Arial 12 bold', fill='red')

	def displayGameOverScreen(self):
		cx = self.cx
		cy = self.cy
		gameOverText = '''GAME OVER
Final score: %d\n Press any button to switch to Start screen''' % self.score
		self.canvas.create_text(cx, cy,
					text=gameOverText, font='Helvetica 20 bold')

	def displayGameWonScreen(self):
		# screen that is displayed when game is won.
		# different from the game over screen
		gameWonText = '''Congratulations!!!
You have beaten the game.
Your final score is %d
Press any button to switch back to the start screen''' % self.score

	def drawHighScoreScreen(self):
		# screen accessible in game start screen
		# that will show high score
		margin = max(self.width/10.0, self.height/10.0)
		highScore = self.highScore
		cx = self.cx
		cy = self.cy
		(self.bBottom, self.bRight) = (2*margin, margin*3/2.0)
		if self.highscoreScreen:
			# writing high score in the middle
			self.canvas.create_text(cx, cy/2.0, text='High Score:')
			self.canvas.create_text(cx, cy, text=highScore, font='Arial 15 bold')
			self.canvas.create_rectangle(0, 0, self.bBottom,
							self.bRight, outline='black',
							width=3)
			self.canvas.create_text(margin, margin*3/4.0, text='Back', 
							font='Arial 12 bold') # back button to start screen

	def determineImage(self, direction):
		# determines the image that must be drawn
		# for the player
		if direction == 'NorthWest':
			return self.image_pMoveNW
		elif direction == 'NorthEast':
			return self.image_pMoveNE
		elif direction == 'SouthEast':
			return self.iamge_pMoveSE
		elif direction == 'SouthWest':
			return self.image_pMoveSW
		elif direction == None or direction == 'Down':
			return self.image_pMoveDown
		elif direction == 'Up':
			return self.image_pMoveUp
		elif direction == 'Left':
			return self.image_pMoveLeft
		elif direction == 'Right':
			return self.image_pMoveRight

	def determineGreyZombieImage(self, direction):
		# here we give the image depending on the direction
		# or the change in the zombies x and y coordinates
		if direction == None or direction == 'South':
			return self.image_gZomMoveDown
		elif direction == 'North':
			return self.image_gZomMoveUp
		elif direction == 'East':
			return self.image_gZomMoveRight
		elif direction == 'West':
			return self.image_gZomMoveLeft
		elif direction == 'NorthWest':
			return self.image_gZomMoveNW
		elif direction == 'NorthEast':
			return self.image_gZomMoveNE
		elif direction == 'SouthEast':
			return self.image_gZomMoveSE
		elif direction == 'SouthWest':
			return self.image_gZomMoveSW

	def determineRedZombieImage(self, direction):
		# same as determineGreyZombieImage only with
		# red Zombie images
		if direction == None or direction == 'South':
			return self.image_rZomMoveDown
		elif direction == 'North':
			return self.image_rZomMoveUp
		elif direction == 'East':
			return self.image_rZomMoveRight
		elif direction == 'West':
			return self.image_rZomMoveLeft
		elif direction == 'NorthWest':
			return self.image_rZomMoveNW
		elif direction == 'NorthEast':
			return self.image_rZomMoveNE
		elif direction == 'SouthEast':
			return self.image_rZomMoveSE
		elif direction == 'SouthWest':
			return self.image_rZomMoveSW

	def showNoAmmoScreen(self):
		# when player has no ammo, a flashing no ammo notification
		noAmmoX = self.p1x
		noAmmoY = self.p1y - 4*self.r
		if self.noAmmo:
			self.canvas.create_text(noAmmoX, noAmmoY, text='No Ammo!!', 
							font='Helvetica 10', fill='red')

	def drawHelpScreen(self):
		helpScreenText = '''Key Commands: 
Arrow keys: move
Space bar: shoot 
Number keys: switch weapons
P: pause
H: help

Items:
Green: Health boosts 
Black: Ammo
Red: New weapons

Tips: Mines explode after 3 seconds
Stay away from RPG explosions'''
		hx = self.cx
		hyCoeff = 3/2.0
		hy = self.cy*hyCoeff
		if self.helpScreen:
			self.canvas.create_text(hx, hy, text=helpScreenText,
						font='Helvetica 18 bold')

	def drawPlayer1(self):
		px = self.p1x
		py = self.p1y
		direction = self.lastMove
		image = self.determineImage(direction)
		self.canvas.create_image(px, py, image=image)

	def drawBackground(self):
		width = self.width
		height = self.height
		(cx, cy) = (self.cx, self.cy)
		(creditX, creditY) = (cx*8/5.0, cy*9/5.0)
		creditText = '''Developed and Designed by Jae Kang
For 15-112 @ Carnegie Mellon'''
		r = self.r
		backgroundColor = self.backgroundColor
		self.canvas.create_rectangle(0-r, 0-r, 
			width+r, height+r, fill=backgroundColor)
		self.canvas.create_text(creditX, creditY, text=creditText,
							font='Helvetica 10 bold')

	def drawGameWonScreen(self):
		# when game has been won
		cx = self.cx
		cy = self.cy
		creditX = cx
		creditY = cy*9/5.0
		gameWonText = '''Congratulations!!!
You have beaten the game.
Your final score is %d''' % self.score
		self.canvas.create_text(cx, cy, text=gameWonText, 
						font='Arial 40 bold')


	def highlightSelection(self):
		(left, right) = (self.left, self.right)
		(top1, bottom1) = (self.top1, self.bottom1)
		(top2, bottom2) = (self.top2, self.bottom2)
		(top3, bottom3) = (self.top3, self.bottom3)
		(top4, bottom4) = (self.top4, self.bottom4)
		(bRight, bBottom) = (self.bRight, self.bBottom)
		beginnerHighlighted = self.beginnerHighlighted
		intermediateHighlighted = self.intermediateHighlighted
		expertHighlighted = self.expertHighlighted
		highscoreHighlighted = self.highscoreHighlighted
		if beginnerHighlighted:
		 	self.canvas.create_rectangle(left, top1, right, bottom1, 
					outline='cyan') #highlight beginner box
		elif intermediateHighlighted:
		 	self.canvas.create_rectangle(left, top2, right, bottom2, 
					outline='cyan') #highlight interm box
		elif expertHighlighted:
		 	self.canvas.create_rectangle(left, top3, right, bottom3, 
					outline='cyan') #highlight expert box
		elif highscoreHighlighted:
		 	self.canvas.create_rectangle(left, top4, right, bottom4,
		 				outline='cyan') #highlight high score box

	def getHighScore(self):
		try:
			highScore = int(readFile('boxheadHighscore.txt'))
			return highScore
		except:
			# if file doesn't exist 
			highScore = 0
			return highScore

	def checkIfScoreIsHighScore(self):
		if self.score > self.highScore:
			# if current score higher than prev high score
			# write over file
			writeFile('boxheadHighscore.txt', str(self.score))

	def initAnimation(self):
		self.root.bind('<Motion>', self.mouseMotion)
		self.greyZombie = GreyZombie(self.canvas)
		self.redZombie = RedZombie(self.canvas)
		self.player1 = Player1(self.canvas)
		self.image_mine = PhotoImage(file='boxhead_Mine.gif')
		self.image_blood = PhotoImage(file='boxheadBlood.gif')
		self.image_pMoveNW = PhotoImage(file='boxheadCharacter_moveNorthWest.gif')
		self.image_pMoveNE = PhotoImage(file='boxheadCharacter_moveNorthEast.gif')
		self.image_pMoveSW = PhotoImage(file='boxheadCharacter_moveSouthWest.gif')
		self.iamge_pMoveSE = PhotoImage(file='boxheadCharacter_moveSouthEast.gif')
		self.image_pMoveDown = PhotoImage(file='boxheadCharacter_moveDown.gif')
		self.image_pMoveUp = PhotoImage(file='boxheadCharacter_moveUp.gif')
		self.image_pMoveRight = PhotoImage(file='boxheadCharacter_moveRight.gif')
		self.image_pMoveLeft = PhotoImage(file='boxheadCharacter_moveLeft.gif')
		self.image_gZomMoveDown = PhotoImage(file='greyZombie_moveDown.gif')
		self.image_gZomMoveUp = PhotoImage(file='greyZombie_moveUp.gif')
		self.image_gZomMoveRight = PhotoImage(file='greyZombie_moveRight.gif')
		self.image_gZomMoveLeft = PhotoImage(file='greyZombie_moveLeft.gif')
		self.image_gZomMoveNW = PhotoImage(file='greyZombie_moveNorthWest.gif')
		self.image_gZomMoveSW = PhotoImage(file='greyZombie_moveSouthWest.gif')
		self.image_gZomMoveNE = PhotoImage(file='greyZombie_moveNorthEast.gif')
		self.image_gZomMoveSE = PhotoImage(file='greyZombie_moveSouthEast.gif')
		self.image_rZomMoveUp = PhotoImage(file='redZombie_moveUp.gif')
		self.image_rZomMoveDown = PhotoImage(file='redZombie_moveDown.gif')
		self.image_rZomMoveRight = PhotoImage(file='redZombie_moveRight.gif')
		self.image_rZomMoveLeft = PhotoImage(file='redZombie_moveLeft.gif')
		self.image_rZomMoveNW = PhotoImage(file='redZombie_moveNorthWest.gif')
		self.image_rZomMoveNE = PhotoImage(file='redZombie_moveNorthEast.gif')
		self.image_rZomMoveSW = PhotoImage(file='redZombie_moveSouthWest.gif')
		self.image_rZomMoveSE = PhotoImage(file='redZombie_moveSouthEast.gif')

	def redrawAll(self):
		self.canvas.delete(ALL)
		self.drawBackground()
		if self.gameStartScreen:
			# start screen
			self.drawStartScreen()
			self.highlightSelection()
		elif self.highscoreScreen:
			self.drawHighScoreScreen()
		elif self.gameWon:
			self.drawGameWonScreen()
		elif not self.isGameOver and self.allOptionsSelectedForStart:
			self.drawHelpScreen()
			self.showNoAmmoScreen()
			self.drawBlood()
			self.drawItems()
			self.drawMines()
			self.drawRocketExplosions()
			self.drawZombies() 
			self.drawZombiesHealthBar()
			self.displayGameScreen()
			self.drawPlayer1()
			self.player1.drawHealthBar(self.player1Health,
							 self.p1x, self.p1y)
			if self.pauseGame:
				self.displayPauseScreen()
			else:
				# if not pause, zombies may move
				# and bullets may be drawn
				self.zombiesAttack()
				if self.bulletInAir:
					self.shoot(self.startTimeOfShot)
		else:
			self.displayGameOverScreen()

class Player1(Boxhead):

	def __init__(self, canvas):
		Boxhead.__init__(self)
		self.canvas = canvas
		self.r = 10
		self.timerDelay = 250
		self.moveDistance = 10

	def drawHealthBar(self, health, px, py):
		# draw the health bar that should be above the player at all times
		# following wherever the player goes.
		r = self.r
		healthPercentage = health / 100.0
		topYCoeff = 5/2.0
		rightXCoeff = 2
		bottomYCoeff = 1/2.0
		left = px - r
		top = py - topYCoeff*r
		right = left + rightXCoeff*r
		bottom = top + bottomYCoeff*r
		healthBarRight = left + (rightXCoeff*r)*healthPercentage
		# utilize health
		self.canvas.create_rectangle(left, top, right, bottom, 
									outline='black')
		self.canvas.create_rectangle(left, top, healthBarRight, bottom,
									fill='green')

class Zombie(Boxhead):

	def __init__(self, canvas):
		Boxhead.__init__(self)
		self.greyStepDistance = 0.5
		self.redStepDistance = 1
		self.zombieHealth = 100
		self.movedLeft = False
		self.movedRight = False
		self.movedUp = False
		self.movedDown = False
		# bool values needed to see if zombie is
		# moving diagonally and to draw it when necessary

	def moveLeftRight(self, cx, cy, zx, zy, color):
		if color == 'grey':
			stepD = self.greyStepDistance
		elif color == 'red':
			stepD = self.redStepDistance
		# stepD depends on whether grey or red zombie
		# red zombies move twice as fast
		if zx - cx > 0:
			zx -= stepD #move left
			self.movedLeft = True
		elif zx - cx < 0: 
			zx += stepD # move right
			self.movedRight = True
		return zx, zy

	def moveUpDown(self, cx, cy, zx, zy, color):
		if color == 'grey':
			stepD = self.greyStepDistance
		elif color == 'red':
			stepD = self.redStepDistance
		if zy - cy > 0:
			zy -= stepD #moved Up
			self.movedUp = True
		elif zy - cy < 0:
			zy += stepD # moved Down
			self.movedDown = True
		return zx, zy

	def setMovedValuesBack(self):
		self.movedLeft = False
		self.movedRight = False
		self.movedUp = False
		self.movedDown = False

	def determineDirection(self):
		# direction needed to draw zombie depending on the direction
		if self.movedLeft == True and self.movedUp == True:
			return 'NorthWest'
		if self.movedLeft == True and self.movedDown == True:
			return 'SouthWest'
		if self.movedRight == True and self.movedUp == True:
			return 'NorthEast'
		if self.movedRight == True and self.movedDown == True:
			return 'SouthEast'
		if self.movedRight == True:
			return 'East'
		if self.movedLeft == True:
			return 'West'
		if self.movedUp == True:
			return 'North'
		if self.movedDown == True:
			return 'South'

	def moveTowardsPlayer(self, zx, zy, cx, cy, zHealth, color):
		r = self.r
		self.setMovedValuesBack() #set everything to false
		if zx - cx != 0:
			(zx, zy) = self.moveLeftRight(cx, cy, zx, zy, color)
		if zy - cy != 0:
			(zx, zy) = self.moveUpDown(cx, cy, zx, zy, color)
		direction = self.determineDirection()
		return [zx, zy, zHealth, direction]

	def drawHealthBar(self, zx, zy, health):
		# draw health bar around all the zombies as well
		r = self.r
		healthPercentage = health / 100.0
		topYCoeff = 5/2.0
		rightXCoeff = 2
		bottomYCoeff = 1/2.0
		left = zx - r
		top = zy - topYCoeff*r
		right = left + rightXCoeff*r
		bottom = top + bottomYCoeff*r
		healthBarRight = left + (rightXCoeff*r)*healthPercentage
		# utilize health
		self.canvas.create_rectangle(left, top, right, bottom, 
									outline='black')
		self.canvas.create_rectangle(left, top, healthBarRight, bottom,
									fill='green')

class GreyZombie(Zombie):
	# the weakest zombies but the most common

	def __init__(self, canvas):
		Zombie.__init__(self, canvas)
		self.canvas = canvas
		self.color = 'grey'
	
class RedZombie(Zombie):
	# stronger zombie
	# devil actually

	def __init__(self, canvas):
		Zombie.__init__(self, canvas)
		self.canvas = canvas
		self.color = 'red'

def playBoxhead():
	boxheadGame = Boxhead()
	boxheadGame.run()

def testBoxhead():
	boxhead = Boxhead()
	print 'Testing Boxhead class...',
	assert boxhead.isArrowKey('Up') == True
	assert boxhead.isArrowKey('Down') == True
	assert boxhead.isArrowKey('Left') == True
	assert boxhead.isArrowKey('a') == False
	assert boxhead.isDiagonalMove(set(['Up', 'Left'])) == True
	assert boxhead.isDiagonalMove(set([12, 'Up'])) == False
	assert boxhead.addAmmo('Pistol') == 50
	assert boxhead.addAmmo('Uzi') == 200
	assert boxhead.addAmmo('RPG') == 25
	print 'Passed!'


if __name__ == '__main__':
	testBoxhead()
	playBoxhead()

# #############################################
###############################################