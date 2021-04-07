""" written by Joel	
	contains the main loop for the Pacman game. 
"""
import numpy as np
import pygame as pg
from classes import configMayham as cng
from classes import classesMayham as cm
from classes import CLASSES_BOIDS as cb
from classes import configBoids as cngBoid
from states import state
import time

class Game(state.state):
	""" A class that runs the game"""

	def __init__(self, manager=None, window=None):
		super().__init__(manager, window)
		# set up inits
		pg.init()
		if window==None:
			self.window = pg.display.set_mode(cng.SCREEN_RESOLUTION, pg.FULLSCREEN)
		else:
			self.window = window
		self.runGame = True
		self.clock = pg.time.Clock()
		self._sounds()

		#run the game
		#self.run()


	def run(self, score=[0,0]):
		""" where all the shit is happening"""
		self.soundList[0].play()
		self.score = score
		self.lagScalar = 1
		ghost = cm.Ghost(*cng.GHOST_SPECS)
		MsPacman = cm.MsPacman(*cng.MsPacman_SPECS)
		pacmansList = [cm.Pacman(*cng.PACMAN_SPECS_1), cm.Pacman(*cng.PACMAN_SPECS_2)]
		bulletList = np.array(())
		boidList = np.array(())
		
		# game loop run one time each frame
		while self._active:
			self.update_user_input()
			self.keys = pg.key.get_pressed()
			self._event()
			self.window.fill(cng.BACKGROUND_COLOR)
			self._textDisplay(pacmansList)
			self.clock.tick(cng.FPS)
			if self.clock.get_fps() > 0:
				self.lagScalar = cng.FPS/self.clock.get_fps()
			else:
				self.lagScalar = 1

			ghost.drawGhost(self.window, 3)

			MsPacman.moveMsPacman(self.lagScalar)
			MsPacman.drawMsPacman(self.window, pacmansList)

			# move pacman with key board inputs
			pacmansList[0].drive(self.keys, *cng.KEYS_PLAYER_1)
			pacmansList[1].drive(self.keys, *cng.KEYS_PLAYER_2)

			# pacman shoots boids
			newBoid1, boidPosition1, boidVel1 = pacmansList[0].shootBoid(
				self.keys, self.window, cng.KEYS_PLAYER_1[-1], self.soundList[6], self.lagScalar)
			newBoid2, boidPosition2, boidVel2 = pacmansList[1].shootBoid(
				self.keys, self.window, cng.KEYS_PLAYER_2[-1], self.soundList[6], self.lagScalar)

			# add boids from shots and msPacman
			boidList = self._addBoid(newBoid1, boidPosition1, boidVel1, boidList)
			boidList = self._addBoid(newBoid2, boidPosition2, boidVel2, boidList)
			boidList = MsPacman.spawnBoid(boidList)

			for i, boid in enumerate(boidList):
				boid.drawCircle(self.window)
			self._moveBoids(boidList, pacmansList, ghost)

			# checks if pacman and ghost gets hit by opponents shots
			self._takingFire(pacmansList)
			self._shootingGhost(pacmansList, ghost, MsPacman)

			for i, pacman in enumerate(pacmansList):
				pacman.move(lagScalar=self.lagScalar)
				pacman.gravity(MsPacman)
				pacman.gravity(ghost)

				pacman.drawPacman(self.window, i)
				
				if len(boidList):
					boidList = pacman.eat(boidList, self.soundList[3])
				
				# colliding
				pacman.crashGhost(ghost)
				pacman.crashMsPacman(MsPacman)
			
				self._victory(pacman, pacmansList, i)
	
			pg.display.update()
		return self.MANAGER.get_state('main_menu')

	def _event(self):
		""" checks if the simulation should still be running """
		# Closes the simulation if escape is pressed
		if self.keys[pg.K_ESCAPE]:
			self.runGame = False

		#Make sure that pygame quits if python quits.
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.runGame = False

	def _takingFire(self, allPacmans):
		""" check if the bullets shot hits the opponents, can´t hit yourself
			if hit the pacman takes damage
			Check if the bullets hits ghost
		"""
		hits = 0
		for i, pacman in enumerate(allPacmans):
			opponent = allPacmans[i-1]

			#check if there is any bullets out there, 1 bullet in list by defult
			if opponent.bulletsPosition.shape[0]>2:
				distance = np.linalg.norm(opponent.bulletsPosition - pacman.pos, axis=1)
				bulletThatHit = np.where(distance<pacman.radius)[0]
				hits = len(bulletThatHit)
				if len(bulletThatHit):
					opponent.bulletList = np.delete(opponent.bulletList, bulletThatHit-1)
					pacman.life -= hits*cng.DMG_BULLETS
					self.soundList[2].play()

			if pacman.life<0:
				pacman.life=0

	def _shootingGhost(self, allPacmans, ghost, MsPacman):
		""" check if the bullets hits ghost """
		for i, pacman in enumerate(allPacmans):
			#check if there is any bullets out there, 1 bullet in list by defult
			if pacman.bulletsPosition.shape[0]>2:
				distance = np.linalg.norm(pacman.bulletsPosition - ghost.pos, axis=1)
				bulletThatHit = np.where(distance<ghost.radius)[0]
				if len(bulletThatHit):
					pacman.bulletList = np.delete(pacman.bulletList, bulletThatHit-1)
					ghost.life -= cng.DMG_BULLETS

		if ghost.life<0:
			MsPacman.distance *= .98
			if ghost.dead:
				ghost.dead = False
				ghost.mass *= 4

	def _text(self, words, color, size, position):
		""" returns a texts in a rendered font and a position so it can be blitted later"""
		font = pg.font.Font('chintzy.ttf', size)
		fontRendered = font.render(words, 1 , color)
		return fontRendered, position

	def _textDisplay(self, pacmansList):
		""" display text with boids, love and life for each player """
		pacman1 = pacmansList[0]
		pacman2 = pacmansList[1]
		
		#player 1
		self.lifeText1, self.lifePos1 = self._text('Life: %d' 
			%pacman1.life,  (255-2*pacman1.life,2*pacman1.life,0), *cng.TEXT_LIFE_SIZE_POS_PLAYER1 )
		self.loveText1, self.lovePos1 = self._text('Love: %d' 
			%pacman1.love,  (255-2*pacman1.love,2*pacman1.love,0), *cng.TEXT_LOVE_SIZE_POS_PLAYER1 )
		self.boidText1, self.boidPos1 = self._text('Boids: %d' %pacman1.boidsInBelly,  
			(255-250*pacman1.boidsInBelly//cng.PACMAN_BELLY_SIZE, 
				250*pacman1.boidsInBelly//cng.PACMAN_BELLY_SIZE, 0), *cng.TEXT_BOIDS_SIZE_POS_PLAYER1 )
		
		self.window.blit(self.boidText1, self.boidPos1)
		self.window.blit(self.lifeText1, self.lifePos1)
		self.window.blit(self.loveText1, self.lovePos1)
		
		# player 2
		self.lifeText2, self.lifePos2 = self._text('Life: %d' 
			%pacman2.life,  (255-2*pacman2.life,2*pacman2.life,0), *cng.TEXT_LIFE_SIZE_POS_PLAYER2 )
		self.loveText2, self.lovePos2 = self._text('Love: %d' 
			%pacman2.love,  (255-2*pacman2.love,2*pacman2.love,0), *cng.TEXT_LOVE_SIZE_POS_PLAYER2 )
		self.boidText2, self.boidPos2 = self._text('Boids: %d' %pacman2.boidsInBelly,  
			(255-250*pacman2.boidsInBelly//cng.PACMAN_BELLY_SIZE, 
				250*pacman2.boidsInBelly//cng.PACMAN_BELLY_SIZE, 0), *cng.TEXT_BOIDS_SIZE_POS_PLAYER2 )
		
		self.scoreText, self.scorePos = self._text('%d - %d' 
			%(self.score[0],self.score[1]),  *cng.TEXT_SCORE_COLOR_SIZE_POS )

		self.window.blit(self.boidText2, self.boidPos2)
		self.window.blit(self.lifeText2, self.lifePos2)
		self.window.blit(self.loveText2, self.lovePos2)
		self.window.blit(self.scoreText, self.scorePos)

	def _sounds(self):
		""" make a list with all the soundeffects: self.soundList """
		self.soundList = [	pg.mixer.Sound('sound/beginning.wav'),
							pg.mixer.Sound('sound/chomp.wav'),
							pg.mixer.Sound('sound/eatfruit.wav'),
							pg.mixer.Sound('sound/nom_sound.wav'),
							pg.mixer.Sound('sound/extrapac.wav'),
							pg.mixer.Sound('sound/intermission.wav'),
							pg.mixer.Sound('sound/pew_sound.wav') ]

	def _addBoid(self, add, pos, vel, boidList):
		""" adds a boid with attributes given to the list given"""
		if add and len(boidList)<cng.MAX_NUM_BOIDS:
			boidList = np.append(boidList, cb.Boids(*cngBoid.BOID_SPEC, pos, vel=vel))
		return boidList

	def _moveBoids(self, boidList, obstacleList, pacman):
		""" Does all the calculations for the boids to move
			arguments: boidList, obstacleList, pacman
		"""
		# cecks for each boid on the screen
		for b in boidList:
			collitionList = np.array(())
			flockList = np.array(())

			# checks if there is enought boids to make a flock
			if len(boidList) > cngBoid.MIN_BOIDFLOCK:
				for i in boidList:
					if b==i:
						continue
					else:
						distance = b.pos -i.pos
						distance = np.linalg.norm(distance)

						# create list for boids close to the current boid tested.
						if distance < b.collitionRadius:
							collitionList = np.append(collitionList, i)
						if distance < b.flockRadius:
							flockList = np.append(flockList, i)
						
		# reset extra velocity for boids, from boid rules
			b0, b1, b2, b3, b4 = 0,0,0,0,0
			b0 = self._avoidObstacleList(obstacleList, b)
			
			if len(collitionList):
				b1 = b.avoid(collitionList)
			if len(flockList) >cngBoid.MIN_BOIDFLOCK:
				b2 = b.velocity(flockList)
				b3 = b.centering(flockList)
			
			# avoid pacman
			if np.linalg.norm(b.pos-pacman.pos)	< b.predatorRadius:
				b4 = (b.pos-pacman.pos) /(np.linalg.norm(b.pos-pacman.pos)**0.8)
			
			# update vel for boid
			b.vel = np.array(b.vel)
			b.vel = b.vel+(.5*b0 +10*b1 + b2 + b3 + 0.1*b4)*self.lagScalar
			b.speed = np.linalg.norm(b.vel)
			b.angle = np.rad2deg(np.arctan2(b.vel[1],b.vel[0]))
			
			b.move(randomMode=0, lagScalar=self.lagScalar)

	def _victory(self, pacman, pacmansList, i):
		""" if someone dies display text and let them restart game with enter key 
			adds score to the winning player
		"""
		if pacman.life <=0 or pacman.dead:
			if not pacman.dead:
				self.soundList[5].play()	
				self.score[i] +=1
			pacman.dead=True
			self._victoryText, self._victoryPos = self._text('Player %d wins!' %int(-i+2),  *cng.TEXT_WIN_COLOR_SIZE_POS)
			self.retryText, self.retryPos = self._text('Press Enter to play again',  *cng.TEXT_RETRY_COLOR_SIZE_POS)
			self.window.blit(self._victoryText, self._victoryPos)
			self.window.blit(self.retryText, self.retryPos)

			if self.keys[pg.K_RETURN]:
				self.run(self.score)

	def _avoidObstacleList(self, obstacleList, movingObject):
		""" checks if a list of moving objects should avoid a 
			list of still obstacles 
		"""
		a0 = 0
		if len(obstacleList):
			for o in obstacleList:			
				if np.linalg.norm(np.array(movingObject.pos)-np.array(o.pos)) < movingObject.collitionRadius+o.radius:
					a0 += movingObject.avoidObstacle(o)
							
				else:
					a0 += 0

		return a0
