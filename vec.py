""" vec2 module. """

from math import sqrt
from math import cos
from math import sin
	
class vec:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __repr__(self):
		return "(%.0f, %.0f)" % (self.x, self.y)

	def add(self, v):
		return vec(self.x+v.x, self.y+v.y)

	def sub(self, v):
		return vec(self.x-v.x, self.y-v.y)

	def scale(self, s):
		return vec(self.x*s, self.y*s)

	def scalexy(self, v):
		return vec(self.x*v.x, self.y*v.y)

	def dot(self, v):
		return self.x*v.x + self.y*v.y

	# euuclidean distance
	def eucd(self, v):
		return sqrt((self.x - v.x)**2 + (self.y - v.y)**2)

	def len(self):
		return sqrt(self.dot(self))

	# normalized vector
	def norm(self):
		return self.scale(1/self.len())

	def rotate(self, rad):
		return vec(self.x*cos(-rad) - self.y*sin(-rad), self.x*sin(-rad) + self.y*cos(-rad))
