""" car module. """

import logging
from math import cos
from math import sin
from math import acos

import pygame

from vec import vec

class car:
	def __init__(self, pos, force=vec(0, 0), sprite_path="car.png"):
		self.pos = pos
		self.force = force
		self.mass = 0.01 # in kg
		self.acceleration = vec(0, 0)
		self.velocity = vec(0, 0)
		self.score = 0
		
		self.sprite = pygame.image.load(sprite_path) # sprite 
		self.transformed_sprite = pygame.image.load(sprite_path)
		self.rect = self.sprite.get_rect()
		self.rect.x = int(pos.x)
		self.rect.y = int(pos.y)
		self.dir = vec(1, 0)
		self.prevdir = vec(1, 0)
		self.angle = 0
		self.forward = False
		self.backward = False
		self.left = False
		self.right = False
		self.boosting = False
		self.rays = []

		self.tick = 0 # reset this to 0 every time you apply a new force

	def air_resistance(self):
		self.force = self.force.add(self.force.scale(-0.05))
		
	def move(self, force):
		self.force = self.force.add(self.dir.scale(force)) 

	def update(self, dt, tick):
		# rotate car sprite to the direction it is facing:
		old_center = self.rect.center
		self.transformed_sprite = pygame.transform.rotate(self.sprite, self.angle)
		self.rect = self.transformed_sprite.get_rect()
		self.rect.center = old_center

		self.raycast()

		# F = m * a
		# v = a * t
		# s = v * t
		self.air_resistance() # consider air resistance each time, otherwise car won't come to a stop
		self.acceleration = self.force.scale(1/self.mass)
		self.velocity = self.acceleration.scale(dt)
		self.pos = self.pos.add(self.velocity.scale(dt))
		
		self.rect.center = (self.pos.x, self.pos.y)

	def rotate(self, angle):
		self.angle += angle
		rad = self.angle * 3.1415/180
		self.dir = vec(cos(-rad), sin(-rad))

	def render_rays(self, surface):
		width, height = surface.get_size()
		start = (int(width/2), int(height/2))

		pygame.draw.line(surface, (0, 0, 50), start, (start[0]+self.dir.x*500, start[1]+self.dir.y*500), 5)
		pygame.draw.line(surface, (0, 0, 50), start, (start[0]-self.dir.x*500, start[1]-self.dir.y*500), 5)

		x_rotated = self.dir.rotate(-3.1415/2).scale(500)
		pygame.draw.line(surface, (0, 0, 50), start, (start[0]+x_rotated.x, start[1]+x_rotated.y), 5)
		
		x_rotated = self.dir.rotate(3.1415/2).scale(500)
		pygame.draw.line(surface, (0, 0, 50), start, (start[0]+x_rotated.x, start[1]+x_rotated.y), 5)
		
		x_rotated = self.dir.rotate(3.1415/4).scale(500)
		pygame.draw.line(surface, (0, 0, 50), start, (start[0]-x_rotated.x, start[1]-x_rotated.y), 5)
		
		x_rotated = self.dir.rotate(-3.1415/4).scale(500)
		pygame.draw.line(surface, (0, 0, 50), start, (start[0]-x_rotated.x, start[1]-x_rotated.y), 5)
		
		x_rotated = self.dir.rotate(3.1415/4).scale(500)
		pygame.draw.line(surface, (0, 0, 50), start, (start[0]+x_rotated.x, start[1]+x_rotated.y), 5)
		
		x_rotated = self.dir.rotate(-3.1415/4).scale(500)
		pygame.draw.line(surface, (0, 0, 50), start, (start[0]+x_rotated.x, start[1]+x_rotated.y), 5)


	def raycast(self):
		start = (self.pos.x, self.pos.y)

		
		end_front = vec(start[0]+self.dir.x*500, start[1]+self.dir.y*500)
		
		x_rotated = self.dir.rotate(-3.1415/2).scale(500)
		end_front_left = vec(start[0]+x_rotated.x, start[1]+x_rotated.y)
		
		x_rotated = self.dir.rotate(3.1415/2).scale(500)
		end_front_right = vec(start[0]+x_rotated.x, start[1]+x_rotated.y)


		end_back = vec(start[0]-self.dir.x*500, start[1]-self.dir.y*500)
		
		x_rotated = self.dir.rotate(3.1415/4).scale(500)
		end_back_left = vec(start[0]-x_rotated.x, start[1]-x_rotated.y)

		x_rotated = self.dir.rotate(-3.1415/4).scale(500)
		end_back_right = vec(start[0]-x_rotated.x, start[1]-x_rotated.y)

		
		x_rotated = self.dir.rotate(3.1415/4).scale(500)
		r1 = vec(start[0]+x_rotated.x, start[1]+x_rotated.y)

		x_rotated = self.dir.rotate(-3.1415/4).scale(500)
		r2 = vec(start[0]+x_rotated.x, start[1]+x_rotated.y)
		
		self.rays = [end_front, end_front_left, end_front_right, end_back, end_back_left, end_back_right, r1, r2]
				
	def collision(self):
		return False
