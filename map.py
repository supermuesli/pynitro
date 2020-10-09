""" Map editor module. """

import pygame

import random

class map_:
	def __init__(self, surface, line_func, lines=500):
		self.surface = surface
		self.width = self.surface.get_size()[0]
		self.height = self.surface.get_size()[1]
		self.line_func = line_func
		self.lines = []

		start_1 = (0, 0)
		end_1   = (0, 1000)
		self.lines += [(start_1, end_1)]
		start_1 = (800, 0)
		end_1   = (800, 1000)
		self.lines += [(start_1, end_1)]

		for i in range(1, lines):
			# line 1 (red)
			start = (self.lines[i-2][0][0], self.lines[i-2][0][1])
			end   = (self.lines[i-2][1][0] + 100, self.lines[i-2][1][1] + 100)
			self.lines += [(start, end)]
			print(start, end)
			
			# line 2 (green), should be perpendicular to line 1 (red)
			start = (start[0] + 100, start[1])
			end   = (end[0] + 100, end[1] + 100)
			self.lines += [(start, end)]

	def render(self, offset_x, offset_y):
		for i, line in enumerate(self.lines):
			color = (255, 0, 0) if i % 2 == 0 else (0, 255, 0)
			pygame.draw.line(self.surface, color, (line[0][0] + offset_x, line[0][1] + offset_y), (line[1][0] + offset_x, line[1][1] + offset_y), 10)
	