import sys, random

import pygame
import pygame.font

from vec import vec
from car import car
from map import map_
	
amount_cars = 5
cur_car = 0

def main():
	# init pygame
	pygame.init()
	black = 0, 0, 0
	red   = 255, 0, 0
	size = width, height = int(1366*0.95), int(768*0.95)
	screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)
	font = pygame.font.Font("arcade.ttf", 12)

	map__ = map_(screen, lambda x: x**3, lines=200)

	cars = [car(vec(width/3, height/2), vec(0, 0), "car.png") for i in range(amount_cars)]
	
	def update_forces(dt, tick):
		# manually moving the car/adding force via engine + fuel
		if cars[cur_car].forward:
			cars[cur_car].move(50.0)
		if cars[cur_car].backward:
			cars[cur_car].move(-50.0)
		if cars[cur_car].right:
			cars[cur_car].rotate(-5)
		if cars[cur_car].left:
			cars[cur_car].rotate(5)
		if cars[cur_car].boosting:
			cars[cur_car].move(100)

		for car in cars:
			car.update(dt, tick) # semi implicit euler integration


	def draw():
		offset_x, offset_y = int(width/2 - cars[cur_car].rect.center[0]), int(height/2 - cars[cur_car].rect.center[1])

		screen.fill(black) # clear screen
		
		# render map
		#map__.render(offset_x, offset_y)
	
		# render cars
		for i, car in enumerate(cars):
			if i != cur_car:
				screen.blit(car.transformed_sprite, (int(car.rect.center[0] - car.rect.width/2 + offset_x), int(car.rect.center[1] - car.rect.height/2 + offset_y)))

		# current car is supposed to be centered
		cars[cur_car].render_rays(screen)
		screen.blit(cars[cur_car].transformed_sprite, (int(width/2 - cars[cur_car].rect.size[0]/2), int(height/2 - cars[cur_car].rect.size[1]/2))) # draw sprites

		# render GUI and HUD
		hud = font.render("force: %s   acceleration: %s   velocity: %s   position: %s" % (cars[cur_car].force, cars[cur_car].acceleration, cars[cur_car].velocity, cars[cur_car].pos), True, red)
		screen.blit(hud, (10, 10))
		
		# swap buffers
		pygame.display.flip() 

	def poll():
		global cur_car
		global amount_cars

		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit()

				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					cars[cur_car].left = True

				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					cars[cur_car].right = True
				
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					cars[cur_car].forward = True

				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					cars[cur_car].backward = True

				if event.key == pygame.K_SPACE:
					cars[cur_car].boosting = True

				if event.key == pygame.K_RSHIFT:
					cars[cur_car].left = False
					cars[cur_car].right = False
					cars[cur_car].backward = False
					cars[cur_car].forward = False
					cur_car = (cur_car + 1) % amount_cars
					
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_a:
					cars[cur_car].left = False

				if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					cars[cur_car].right = False
				
				if event.key == pygame.K_UP or event.key == pygame.K_w:
					cars[cur_car].forward = False

				if event.key == pygame.K_DOWN or event.key == pygame.K_s:
					cars[cur_car].backward = False
	
				if event.key == pygame.K_SPACE:
					cars[cur_car].boosting = False

	clock = pygame.time.Clock()
	dt = 0
	tick = 0
	
	while 1:
		poll()
		draw()
		update_forces(dt/1000, tick)

		tick += 1
		dt = clock.tick(60) # in milliseconds

if __name__ == '__main__':
	main()
