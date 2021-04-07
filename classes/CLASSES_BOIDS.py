""" Written by Joel
	Boid classes used in Pacman pygame. Only the boid class is used.
"""
import pygame as pg
import numpy as np
from classes import configMayham as cng

class MovingObjects():
	""" Class for all the moving objects:
		arguments: 	maxSpeed=10, position=(10,10)
		methods:	move(damping=0.95, randomMode=0, lagScalar=1) 
					avoidObstacle(obstacle)
	"""
	def __init__(self, maxSpeed=10, position=(10,10), vel=[1,1]):
		self.pos = position
		self.angle = np.random.randint(0, 360)
		self.vel = vel
		self.maxSpeed = maxSpeed
		self.collitionRadius = cng.COLLITION_RADIUS

	def move(self, damping=0.95, randomMode=False, lagScalar=1):
		""" move an object depending on the objects self.vel
			if it goes out from the screen it appers on the other side 
			of the screen.
			randomMode: if True the objects appear on a random position
			of the other side of the screen when passing the edge of the 
			screen.
		"""
		# keep the speed at around maxSpeed
		if np.linalg.norm(self.vel) > self.maxSpeed/2:
			self.vel *= 0.95
		else:
			self.vel *=1.05

		# change angle a bit random
		self.angle = (np.rad2deg(np.arctan2(self.vel[1],self.vel[0])))
		self.angle += np.random.normal(0,5)
		self.vel = np.linalg.norm(self.vel) * np.array((
			np.cos(self.angle*np.pi/180),  np.sin(self.angle*np.pi/180)))


		self.pos += self.vel*lagScalar

		# when going outside the screen it appears on the other side
		if cng.RANDOM_MODE == 0:
			if self.pos[0] > cng.SCREEN_RESOLUTION[0]:
				self.pos[0] = 0
			if self.pos[1] > cng.SCREEN_RESOLUTION[1]:
				self.pos[1] = 0
			if self.pos[0] < 0:
				self.pos[0] = cng.SCREEN_RESOLUTION[0]
			if self.pos[1] < 0:
				self.pos[1] = cng.SCREEN_RESOLUTION[1]

		# when going outside the screen it appears on a random 
		# spot on the other side
		if randomMode:
			if self.pos[0] > cng.SCREEN_RESOLUTION[0]:
				self.pos[0] -= cng.SCREEN_RESOLUTION[0]
				self.pos[1] = cng.SCREEN_RESOLUTION[1]*np.random.random(1)
			if self.pos[1] > cng.SCREEN_RESOLUTION[1]:
				self.pos[1] -= cng.SCREEN_RESOLUTION[1]
				self.pos[0] = cng.SCREEN_RESOLUTION[0]*np.random.random(1)
			if self.pos[0] < 0:
				self.pos[0] += cng.SCREEN_RESOLUTION[0]
				self.pos[1] = cng.SCREEN_RESOLUTION[1]*np.random.random(1)
			if self.pos[1] < 0:
				self.pos[1] += cng.SCREEN_RESOLUTION[1]
				self.pos[0] = cng.SCREEN_RESOLUTION[0]*np.random.random(1)

		#self.pos[0], self.pos[1] = int(self.pos[0]), int(self.pos[1])


	def avoidObstacle(self, obstacle):
		"""	Make the object avoid an obsticale object with a 
			pos (position) and radius.
			returns a "newVel" if the object is close enought to have to avoid it.
		"""
		newVel = 0

		# check if the object has collided on the same pixel, this avoide divide by 0 error.
		if self.pos[0] == obstacle.pos[0] and self.pos[1] == obstacle.pos[1]:
			newVel -= 2*self.vel
		# check if the objects are overlapping, if yes a big repell velocity is returned
		elif np.linalg.norm(np.array(self.pos)-np.array(obstacle.pos)) < obstacle.radius:
			newVel += np.linalg.norm(self.vel) * (self.pos-obstacle.pos) /np.linalg.norm(self.pos-obstacle.pos)
		# check if the object is close to colide. if yes a small repell velocity is returned
		else:
			newVel -= 0.3*(self.pos-obstacle.pos) /(-obstacle.radius+np.linalg.norm(self.pos-obstacle.pos)**0.8)
		
		return newVel


class DrawnObjects():
	"""	Class for all object that should be plotted.
		arguments: 	color=(0,0,0), position=(100,100), 
					radius=1, width=1, hight=1, angle=0
		methods: 	drawCircle(window)
					drawRectangle(window)
	"""
	def __init__(self, color=(0,0,0), position=(100,100), radius=1, 
		width=1, hight=1, angle=0):

		self.surf = pg.Surface((hight, width),flags=pg.SRCALPHA)
		self.surf.set_alpha(0)
		self.color =color
		self.pos = position
		self.radius = radius
		self.width = width
		self.hight = hight
		self.angle = angle


	def drawCircle(self, window):
		"""Draws a circle on a given screen, with the values that is self declared:
			x, y, color, radius"""
		self.pos = np.array(self.pos)
		pg.draw.circle(window, self.color, self.pos.astype(int), self.radius)


	def drawRectangle(self, window):
		"""Draws a rectangle on a given screen, with the values that is self declared:
			x, y, color, width, hight"""
		self.surf.fill(self.color)

		rotSurf = pg.transform.rotozoom(self.surf, -self.angle +90 , 1.0)
		rect = self.surf.get_rect()
		rect = rotSurf.get_rect(center= self.pos)
		rect.center = (self.pos)
		window.blit(rotSurf, rect)

		
class Boids(DrawnObjects, MovingObjects):
	"""	Class for all boids, they can flock together, avoide obstacles 
		and predators.
		
		inherret: 	DrawnObjects, MovingObjects
		arguments: 	maxSpeed=5,  color=(0,0,0), radius=1, 
					width=1, hight=1, position=(10,10)
		methods: 	avoid(closeFlock)
					velocity(flock)
					centering(flock)
	"""
	def __init__(self, maxSpeed=5,  color=(0,0,0), radius=1, 
		width=1, hight=1, position=(10,10), vel=[1,1]):
		DrawnObjects.__init__(self, color, position, radius, width, hight)
		MovingObjects.__init__(self, maxSpeed, position, vel)
		
		self.flockRadius = cng.FLOCK_RADIUS
		self.predatorRadius = cng.PREADATOR_RADIUS
		

	def avoid(self, closeFlock):
		""" avoide other closeby boids in the closeFlock
			argument: closeFlock
		"""
		newVel = 0

		for i in closeFlock:
			# check if they are on the same pixel
			if self.pos[0] == i.pos[0] and self.pos[1] == i.pos[1]:
				newVel -= 2*self.vel
				print('collition!')
			# repell from all the boids in the flock, more for closer boids
			else:
				newVel += 0.2*(self.pos-i.pos) /(np.linalg.norm(self.pos-i.pos)**0.8)
		
		return newVel
	

	def velocity(self, flock):
		""" matches the velocity of the average velocity in the flock
			arguments: 	flock
		"""
		flockVel = np.array([0.,0.])
		for  b in flock:
			flockVel += b.vel
		flockVel /= len(flock)

		# 1/4 of the flock vel and 3/4 of its ovn vel
		# had some error with this occationally while playing :(
		try:
			return (flockVel + 3*self.vel)/4 - self.vel
		except: 
			return flockVel

	def centering(self, flock):
		""" moves a bit to the center of the flock 
			arguments: 	flock
		"""	
		center = np.array([0.,0.])
		for b in flock:
			center += b.pos
		center /= len(flock)

		center = -0.2*(self.pos-center)/np.linalg.norm(self.pos-center)

		return center


class Pacman(DrawnObjects, MovingObjects):
	""" Class for Pacman, a predetor that chases after boids and eats them. 
		it can avoide obstacles such as ghosts and msPacman.

		inherret: 	DrawnObjects, MovingObjects
		arguments: 	maxSpeed = 10, color=(0,0,0), radius=1, 
					width=1, hight=1, position=(10,10)
		methods: 	findFood(boidList)
					eat(boidList)
					drawPacman(window)
	"""
	def __init__(self, maxSpeed = 10, color=(0,0,0), radius=1, width=1, hight=1, position=(10,10)):
		DrawnObjects.__init__(self, color, position, radius, width, hight)
		MovingObjects.__init__(self, maxSpeed, position)
		self.pacmanIndex = 0
		self.pacmansImg = [	pg.image.load('images/pacman1.png'),
							pg.image.load('images/pacman2.png'),
							pg.image.load('images/pacman3.png'),
							pg.image.load('images/pacman4.png'),
							pg.image.load('images/pacman5.png'),
							pg.image.load('images/pacman4.png'),
							pg.image.load('images/pacman3.png'),
							pg.image.load('images/pacman2.png'),
							pg.image.load('images/pacman1.png')]


	def findFood(self, boidList):
		""" returns normalized vetor from pacman to closest boid"""
		distance = np.zeros(len(boidList))

		# find closest boid to pacman in the list
		for i,b in enumerate(boidList):
			distance[i] = np.linalg.norm(b.pos-self.pos)
		closestBoid = np.argmin(distance)

		# calc vector towards closest boid with lenght increasing the close they are
		movement = .3*(boidList[closestBoid].pos-self.pos)/distance[i]
		if distance[closestBoid] < cng.PACMAN_SIGHT:
			movement += 10*(boidList[closestBoid].pos-self.pos)/(distance[i]**1.5)

		return movement


	def eat(self, boidList):
		""" if the distance between the boid and pacman the boid is deleted 
			from the list. The list is then returned
			arguments: 	boidlist
		"""
		eaten = np.array(())

		for i,b in enumerate(boidList):
			if np.linalg.norm(b.pos-self.pos) < b.radius+self.radius:
				eaten = np.append(eaten, i)

		return eaten


	def drawPacman(self, window):
		""" draws a figure of Pacman on the screen
			arguments:	window
		"""
		pacman = pg.transform.rotozoom(self.pacmansImg[int(self.pacmanIndex/2)],  -self.angle, 0.1)
		
		rect = self.surf.get_rect()
		rect = pacman.get_rect(center= self.pos)
		rect.center = (self.pos)
		window.blit(pacman, rect)
		
		self.pacmanIndex+=1 
		self.pacmanIndex %= 17


	def noEdgeCrossing(self):
		""" keeps Pacman from exeting the screen. 
			But with enought speed he can go anyway.
		"""
		if self.pos[0] > cng.SCREEN_WIDTH - 50:
			self.vel += [-2, 0]
		if self.pos[1] > cng.SCREEN_HIGHT - 50:
			self.vel += [0, -2]

		if self.pos[0] < 0 + 50:
			self.vel += [2, 0]
		if self.pos[1] < 0 + 50:
			self.vel += [0, 2]


class Ghost(DrawnObjects, MovingObjects):
	""" Class for Ghosts, a predetor that chases after Pacman. 
		it does NOT avoide obstacles.

		inherret: 	DrawnObjects, MovingObjects
		arguments: 	maxSpeed = 10, color=(0,0,0), radius=1, 
					width=1, hight=1, position=(10,10)
		methods: 	findPacman(self, pacmanPos)
					drawGhost(self, window, i) 
					where i is the # of picture in the self.ghostsImg array
	"""
	def __init__(self, maxSpeed = 10, color=(0,0,0), radius=1, width=1, hight=1, position=(10,10)):
		DrawnObjects.__init__(self, color, position, radius, width, hight)
		MovingObjects.__init__(self, maxSpeed, position)
		self.ghostIndex = 0 
		self.ghostsImg = [	pg.image.load('images/ghost1.png'),
							pg.image.load('images/ghost2.png'),
							pg.image.load('images/ghost3.png'),
							pg.image.load('images/ghost4.png')] 


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


	def drawGhost(self, window, i):
		""" draws a ghost with a color depending on the argument i [0->3].
			arguments: window, i
		"""
		ghost = pg.transform.rotozoom(self.ghostsImg[i],  0, 0.07)
		
		if self.vel[0]<0:
			ghost = pg.transform.flip(ghost, 1, 0)

		rect = self.surf.get_rect()
		rect = ghost.get_rect(center= self.pos)
		rect.center = (self.pos)
		
		window.blit(ghost, rect)

class Obstacle(DrawnObjects):
	""" Class for Obstacles that other classes can avoide if told to. 

		inherret: 	DrawnObjects
		arguments: 	color=(0,0,0), radius=1, 
					width=1, hight=1, position=(10,10)
		methods: 	drawMsPacman(window)
	"""
	def __init__(self, color=(0,0,0), radius=1, width=1, hight=1, position=(10,10)):
		DrawnObjects.__init__(self, color, np.array(position), radius, width, hight)
		self.msPacmanImg = pg.image.load('images/msPacman.png').convert_alpha()
		self.flip=True

	def drawMsPacman(self, window, pacmanPos):
		""" draws msPacman
			arguments: window
		"""

		vecToPacman = pacmanPos-self.pos
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



