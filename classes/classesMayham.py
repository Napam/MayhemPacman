""" written by Joel	
	contains all the classes that are shown in the Pacman game exept the boid class. 
"""
import numpy as np
import pygame as pg
from classes import configMayham as cng
from classes import configBoids as cngBoid
from classes import CLASSES_BOIDS as cb

class MovingObjects:
	""" Class for all the moving objects:
		arguments: 	maxSpeed=10, position=(10,10), mass=10^5, angle=0, speed=1
		methods:	move(damping=0.95, randomMode=0, lagScalar=1) 
					avoidObstacle(obstacle)
	"""
	def __init__(self, position=[10,10], maxSpeed=10, mass=10^5, angle=0, speed=1):

		self.pos = position
		self.angle=angle
		self.speed=speed
		self.vel = self.speed * np.array((
			np.cos(self.angle*np.pi/180),  np.sin(self.angle*np.pi/180)))
		self.maxSpeed = maxSpeed

		self.mass = mass


		
	def move(self, damping=.05, accellerate=False, boundedScreen=True, lagScalar=1):
		""" move an object depending on the objects self.vel
			has a damping motion if the speed is higher then the maxSpeed of the object
			is accellerate is ture the object will accellerate if the speed is lower
			then the max speed.
			boundedScreen: if True the objects is bounded so that it can't go
			outside the screen.
		"""
		if np.linalg.norm(self.vel)>self.maxSpeed/1.5:
			self.vel *= 1-damping
		if np.linalg.norm(self.vel)<self.maxSpeed and accellerate:
			self.vel *= 1+damping

		self.speed = np.linalg.norm(self.vel)
		self.pos = (self.vel + self.pos )#* lagScalar

		# when going outside the screen they have to stop
		if boundedScreen:
			if self.pos[0] > cng.SCREEN_RESOLUTION[0]:
				self.pos[0] = cng.SCREEN_RESOLUTION[0]
			if self.pos[1] > cng.SCREEN_RESOLUTION[1]:
				self.pos[1] = cng.SCREEN_RESOLUTION[1]
			if self.pos[0] < 0:
				self.pos[0] = 0
			if self.pos[1] < 0:
				self.pos[1] = 0

	def gravity(self, celestialBody):
		"""	pulls itself closer to the given celestialBody depending on 
			the mass of both objects
		"""
		scale = 10**5.5
		distance = np.linalg.norm(self.pos - celestialBody.pos)*scale

		if distance > (celestialBody.radius)*scale:
			# normalized direction vector
			direction = [celestialBody.pos[0]-self.pos[0], celestialBody.pos[1]-self.pos[1]]
			direction = direction / np.linalg.norm(direction) 

			G = 10**4
			F = G*self.mass*celestialBody.mass / (distance +50)

			gravityForce = F/self.mass * direction
			self.pos += gravityForce




class DrawnObjects:
	"""	Class for all object that should be plotted.
		arguments: 	color=(0,0,0), position=(100,100), 
					radius=1, width=1, hight=1, angle=0
		methods: 	drawCircle(window)
					drawRectangle(window)
	"""
	def __init__(self, color=(255,255,255), position=[100,100], 
		radius=1, width=1, hight=1, angle=0):
	
		self.surf = pg.Surface((hight,width), flags=pg.SRCALPHA)
		self.surf.set_alpha(0)
		self.color = color
		self.pos = position
		self.radius = radius
		self.width = width
		self.hight = hight
		self.angle = angle


	def drawRectangle(self, window):
		"""Draws a rectangle on a given screen, with the values that is self declared:
			x, y, color, width, hight"""
		self.surf.fill(self.color)

		rotSurf = pg.transform.rotozoom(self.surf, -self.angle  , 1.0)
		rect = self.surf.get_rect()
		rect = rotSurf.get_rect(center=self.pos)
		rect.center = (self.pos)
		window.blit(rotSurf, rect)


	def drawCircle(self, window):
		"""Draws a circle on a given screen, with the values that is self declared:
			x, y, color, radius"""
		pg.draw.circle(window, self.color, [int(self.pos[0]), int(self.pos[1])], self.radius)


class Pacman(MovingObjects, DrawnObjects):
	""" Class for Pacman, a predetor that chases after boids and eats them. 
		He can shoot at other Pacmans and ghost if he miss the shot becomes a boid.
		He can collide with other objects.
		inherret: 	DrawnObjects, MovingObjects
		arguments: 	maxSpeed = 10, color=(0,0,0), radius=1, 
					width=1, hight=1, position=(10,10), mass=4*10^4
		methods: 	eat(boidList, sound)
					drawPacman(window)
					crash(object_pos, object_radius)
					crashMsPacman(MsPacman)
					drive(keysPressed, up, down, left, right, shoot)
					shootBoid(keys, window, shootKey, sound, lagScalar)
	"""
	def __init__(self, maxSpeed=10, color=(255,255,255), radius=1, 
		width=1, hight=1, angle=0, position=(50,50), mass=4*10^4):
		DrawnObjects.__init__(self, color, position, radius, width, hight, angle)
		MovingObjects.__init__(self, position,  maxSpeed, mass)
		
		self.life = cng.PACMAN_LIFE
		self.love = cng.PACMAN_love
		self.loveMax = cng.PACMAN_love
		self.boidsInBelly = cng.PACMAN_BOIDS_IN_BELLY
		self.pacmanIndex = 0
		self.dead = False
		self.wins = 0
		self.loveCooldown = 0
		self.shotCooldown = 0
		self.bulletList = np.array(())
		self.bulletsPosition = np.array([])

		pacmansImg1 = [		
			pg.image.load('images/pacman1.png'),
			pg.image.load('images/pacman2.png'),
			pg.image.load('images/pacman3.png'),
			pg.image.load('images/pacman4.png'),
			pg.image.load('images/pacman5.png'),
			pg.image.load('images/pacman4.png'),
			pg.image.load('images/pacman3.png'),
			pg.image.load('images/pacman2.png'),
			pg.image.load('images/pacman1.png')]

		pacmansImg2 = [		
			pg.image.load('images/pacman1orange.png'),
			pg.image.load('images/pacman2orange.png'),
			pg.image.load('images/pacman3orange.png'),
			pg.image.load('images/pacman4orange.png'),
			pg.image.load('images/pacman5orange.png'),
			pg.image.load('images/pacman4orange.png'),
			pg.image.load('images/pacman3orange.png'),
			pg.image.load('images/pacman2orange.png'),
			pg.image.load('images/pacman1orange.png')]

		self.pacmansImg = [pacmansImg1,pacmansImg2]

	def eat(self, boidList, sound):
		""" if the distance between the boid and pacman the boid is deleted 
			from the list. The list is then returned
			arguments: 	boidlist
		"""
		eaten = np.array(())

		for i,b in enumerate(boidList):
			if np.linalg.norm(b.pos-self.pos) < b.radius+self.radius:
				eaten = np.append(eaten, i)
				if self.boidsInBelly<cng.PACMAN_BELLY_SIZE:
					self.boidsInBelly += 1
					sound.play()
		return np.delete(boidList, eaten)

	def drawPacman(self, window, player=0):
		""" draws a figure of Pacman on the screen
			arguments:	window
		"""
		pacman = pg.transform.rotozoom(self.pacmansImg[player][int(self.pacmanIndex/2)],  -self.angle, 0.08)
		
		rect = self.surf.get_rect()
		rect = pacman.get_rect(center= self.pos)
		rect.center = (self.pos)
		window.blit(pacman, rect)
		
		self.pacmanIndex+=1 
		self.pacmanIndex %= 17

	def crash(self, object_pos, object_radius):
		""" check if pacman is colliding with given position and radius """
		collide = False
		distance = np.linalg.norm(self.pos - object_pos)
		
		if distance < self.radius+object_radius:
			collide = True
		
		return collide

	def crashGhost(self, ghost):
		""" check if pacman is at ghost if True remove 1 life/frame """
		hitGhost = self.crash(ghost.pos, ghost.radius)
		if hitGhost:
			self.life -= 1
			if self.life<0:
				self.life=0

	def crashMsPacman(self, MsPacman):
		""" check if pacman is at ghost if True refill love 
			if full of love refill life until full 
		"""
		snuggle = self.crash(MsPacman.pos, MsPacman.radius)
		if snuggle and self.love<self.loveMax:
			self.love += int(np.random.random(1) + cng.RELOVE_RATE)

		# get life if full on love
		elif snuggle and self.love==self.loveMax and self.life<cng.PACMAN_LIFE:
			self.life += int(np.random.random(1) + cng.HEAL_RATE)

	def drive(self, keysPressed, up, down, left, right, shoot):
		""" move pacman with input from the user, uses love when driving"""
		self.angle = (np.rad2deg(np.arctan2(self.vel[1],self.vel[0])))
		self.speed = np.linalg.norm(self.vel)
		drive = False

		if keysPressed[up]:
			drive = True
			self.speed += .5
		if keysPressed[down]:
			self.speed *= .9
			drive = True
		if keysPressed[left]:
			self.angle -= 5
			drive = True
		if keysPressed[right]:
			self.angle += 5
			drive = True

		self.vel = self.speed * np.array((
			np.cos(self.angle*np.pi/180),  np.sin(self.angle*np.pi/180)))

		# use love when driving
		if self.loveCooldown>0:
			self.loveCooldown -= 1
		if self.loveCooldown ==0 and drive:
			#take damgae if out of love
			if self.love==0:
				self.life -= 3
				self.loveCooldown = cng.COOLDOWN_USE_love//2
				return


			self.love -=1
			self.loveCooldown = cng.COOLDOWN_USE_love

	def shootBoid(self, keys, window, shootKey, sound, lagScalar):
		""" adds bullets to bulletList when shooting and 
		remove after certain time and becomes a boid. """

		# reset lists
		self.bulletsPosition = np.array((-100, -100))
		deadBullets = np.array(())
		newBoid = False
		boidPosition = [100,100]

		if self.shotCooldown > 0:
				self.shotCooldown -=1

		# shoot and add bullet to bulletList
		if keys[shootKey] and self.shotCooldown == 0 and self.boidsInBelly>0:
			self.boidsInBelly -= 1 
			self.bulletList = np.append(self.bulletList, Bullet( radius=5,
				position = np.copy(self.pos), angle = np.copy(self.angle),
				color = np.copy(self.color), speed = np.copy(self.speed)+30))
			self.shotCooldown = cng.COOLDOWN_SHOOT
			sound.play()

		# remove bullets after certain time, move and draw bullets 
		# save position of all bullets in array: bulletsPosition
		for i, bullet in enumerate(self.bulletList):
			bullet.lifeSpann -=1
			if bullet.lifeSpann <0:
				deadBullets = np.append(deadBullets, i)
				newBoid, boidPosition = True, bullet.pos

			bullet.move(boundedScreen=False, lagScalar=lagScalar)
			if self.color[1]<245:
				bullet.color += (0,255//cng.COOLDOWN_BULLET_TRAVEL,0)
			if self.color[0]<245:
				bullet.color += (255//cng.COOLDOWN_BULLET_TRAVEL,0,0)
			bullet.drawCircle(window)
		
		# useful for use outside method	
			self.bulletsPosition = np.row_stack((self.bulletsPosition, bullet.pos))
		
		boidVel = 0
		if len(deadBullets) >0:
			boidVel = self.bulletList[deadBullets.astype(int)][0].vel

		self.bulletList = np.delete(self.bulletList, deadBullets)	

		return newBoid, boidPosition, boidVel


class Bullet(MovingObjects, DrawnObjects):
	"""	Class for all bullets.
		inherret: 	DrawnObjects, MovingObjects
		arguments: 	maxSpeed=0, color=(255,255,255), radius=3, 
		width=1, hight=1, angle=0, position=(50,50), mass=4*10^22, speed=1
	"""
	def __init__(self, maxSpeed=0, color=(255,255,255), radius=3, 
		width=1, hight=1, angle=0, position=(50,50), mass=4*10^22, speed=1):
		DrawnObjects.__init__(self, color, position, radius, width, hight, angle)
		MovingObjects.__init__(self, position,  maxSpeed, mass, angle, speed)
		self.speed = speed
		self.vel = self.speed*np.array((
			np.cos(self.angle*np.pi/180),  np.sin(self.angle*np.pi/180)))
		self.lifeSpann = cng.COOLDOWN_BULLET_TRAVEL


class Ghost(MovingObjects, DrawnObjects):
	""" Class A ghost that has a mass for gravity and can be drawn and move 
		towards a given position 
			arguments: 	color=(0,0,255), position=[100,100], 
		radius=150, width=1, hight=1, angle=0, mass=7.3476*10**22
			methods:	drawGhost(window, i) 
						findPacman(pacmanPos)
		"""

	def __init__(self, color=(0,0,255), position=[100,100], 
		radius=150, width=1, hight=1, angle=0, mass=7.3476*10**22):
			DrawnObjects.__init__(self, color, position, radius, width, hight, angle)
			self.mass = mass	
			self.life = cng.GHOST_LIFE
			self.dead = True
			self.ghostsImg = [	pg.image.load('images/ghost1.png'),
							pg.image.load('images/ghost2.png'),
							pg.image.load('images/ghost3.png'),
							pg.image.load('images/ghost4.png')] 


	def drawGhost(self, window, i):
		""" draws a ghost with a color depending on the argument i [0->3].
			arguments: window, i
		"""
		#print(self.life)
		if self.life >0:
			ghost = pg.transform.rotozoom(self.ghostsImg[i],  0, 0.2)

			rect = self.surf.get_rect()
			rect = ghost.get_rect(center= self.pos)
			rect.center = (self.pos)
			
			window.blit(ghost, rect)

	def findPacman(self, pacmanPos):
		""" returns normalized vetor from ghost to pacman
			arguments: pacmanPos
		"""
		distance = np.linalg.norm(pacmanPos-self.pos)

		
		self.ghostIndex %= 360
		movement = (pacmanPos-self.pos)/distance
		self.angle = (np.rad2deg(np.arctan2(self.vel[1],self.vel[0])))
		self.angle += 15*np.sin(self.ghostIndex)
		self.vel = np.linalg.norm(self.vel) * np.array((
			np.cos(self.angle*np.pi/180),  np.sin(self.angle*np.pi/180)))

		return movement


class MsPacman(MovingObjects, DrawnObjects):
	""" Class MsPacman. 
		inherret: 	DrawnObjects, MovingObjects
		arguments: 	maxSpeed=10, color=(255,255,0), radius=1, 
			width=1, hight=1, angle=0, position=(50,50), mass=7.3476*10**22
		methods: moveMsPacman(lagScalar)
				drawMsPacman(window, pacmanList)
				spawnBoid(boidList)
	"""
	def __init__(self, maxSpeed=10, color=(255,255,0), radius=1, 
		width=1, hight=1, angle=0, position=(50,50), mass=7.3476*10**22):
		self.distance = cng.MsPacman_ORBIT_RATIUS
		self.mass = mass
		DrawnObjects.__init__(self, color, position, radius, width, hight, angle)
		self.addBoidCooldwon = 12
		self.life = 1
		self.flip=True
		self.msPacmanImg = pg.image.load('images/msPacman.png').convert_alpha()


	def moveMsPacman(self, lagScalar):
		""" move around the screen in a circle with some wiggly movment added to it """
		self.pos = [self.distance*np.cos(self.angle)+cng.SCREEN_RESOLUTION[0]//2,
			cng.SCREEN_RESOLUTION[1]//2+self.distance*np.sin(self.angle)]
		self.angle += .01*lagScalar
		self.distance += 2*np.cos(2.9*self.angle)

	def drawMsPacman(self, window, pacmanList):
		""" draws msPacman on a given window, she will always be facing 
			the closest pacman in the given pacmanList.
		"""
		#finds the vector to the closest Pacman
		vecToPacman1 = np.array(pacmanList[0].pos) - np.array(self.pos)
		vecToPacman2 = np.array(pacmanList[1].pos) - np.array(self.pos)

		distance1 = np.linalg.norm(vecToPacman1)
		distance2 = np.linalg.norm(vecToPacman2)

		if distance1 < distance2:
			vecToPacman = vecToPacman1
		else:
			vecToPacman = vecToPacman2


		angleToPacman = np.rad2deg(np.arctan2(vecToPacman[1], vecToPacman[0]))
		msPacman = self.msPacmanImg

		# make sure that msPacman in not uppside down and looking at pacman
		if vecToPacman[0] < 0:
			msPacman = pg.transform.flip(self.msPacmanImg, 0, 1)
		msPacman = pg.transform.rotozoom(msPacman,  -angleToPacman, .3)
		
		rect = self.surf.get_rect()
		rect = msPacman.get_rect(center= self.pos)
		rect.center = (self.pos)
		
		window.blit(msPacman, rect)

	def spawnBoid(self, boidList):
		""" adds a boid to the given list at msPacmans position """
		self.addBoidCooldwon -=1
		
		if len(boidList)<cng.MAX_NUM_BOIDS and self.addBoidCooldwon<0:
			boidList = np.append(boidList, cb.Boids(*cngBoid.BOID_SPEC, self.pos))
			self.addBoidCooldwon = cng.MS_PACMAN_ADDS_BOID_COOLDOWN
		return boidList


