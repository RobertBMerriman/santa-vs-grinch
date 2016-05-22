import pygame, sys
from random import randint
import Transfer
import threading
from pygame.locals import *
from time import sleep

enemy_playerX = 0

sendip = "localhost"
semdport = 8889
listenport = 8888

if __name__ == '__main__':
	'''
	player1 = randint(0, 1)
	if player1 == 0:
		player2 = 1
	else:
		player2 = 0
	'''
	def listen_worker():
		Transfer.listen(listenport)
		while True:
			global enemy_playerX
			string = Transfer.receive()
			
			if "Playerposition:" in string:
				string_list = string.split(":")
				enemy_playerX = int(float(string_list[1]))
			elif "Bomb:" in string:
				string_list = string.split(":")
				bomb_list.append([int(float(string_list[1])), enemy_playerY])
				
			
			
	listen_thread = threading.Thread(target=listen_worker)
	
	pygame.init()
	
	FPS = 30
	fpsClock = pygame.time.Clock()
	
	WIDTH = 480
	HEIGHT = 720
	COLUMN_SPLIT = 4
	ROW_SPLIT = 8
	COLUMN = WIDTH / COLUMN_SPLIT
	ROW = HEIGHT / ROW_SPLIT
	
	
	# Set up window
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Santa Vs Grinch")
	
	# Set up colors
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 0, 255)
	
	# Fill to white
	DISPLAYSURF.fill(WHITE)
	
	# Make player area
	santa_area = pygame.Rect(0, HEIGHT - ROW, WIDTH, ROW)
	grinch_area = pygame.Rect(0, 0, WIDTH, ROW)
	
	# Two backgrounds
	BG = pygame.image.load('snowbg.png')
	BG2 = pygame.image.load('snowbg.png')
	
	# Start screen art
	Intro_BG = pygame.image.load('Intro_background.png')
	Santa_box = pygame.Rect(0, HEIGHT - ROW, WIDTH, ROW)
	Grinch_box = pygame.Rect(0, HEIGHT - ROW, WIDTH, ROW)
	Santa_boxart = pygame.image.load('S_intro.png')
	Grinch_boxart = pygame.image.load('G_intro.png')
	game_over = pygame.image.load('Game_over.png')
	
	# Player and enemy images + bomb image
	santa = pygame.image.load('santa.png')
	grinch = pygame.image.load('grinch.png')
	bomb = pygame.image.load('bomb.png')
	# Player and ememy poses
	santaX = WIDTH / 2 - santa.get_width() / 2
	santaY = HEIGHT - ROW + 5
	grinchX = WIDTH / 2 - grinch.get_width() / 2
	grinchY = 5
	bombSpeed = 10
	bomb_list = [[-50, -50]]
	
	listen_thread.start()
	
	Santa_start = False
	Grinch_start = False
	while Santa_start == False and Grinch_start == False:
		
		DISPLAYSURF.blit(Intro_BG, (0, 0))
		DISPLAYSURF.blit(Santa_boxart, (santaX - 25, santaY - 100))
		DISPLAYSURF.blit(Grinch_boxart, (grinchX - 50, grinchY))
		
		for event in pygame.event.get():
			mouse_x, mouse_y = pygame.mouse.get_pos()
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if mouse_x > santaX - 25 and mouse_x < santaX - 25 + Santa_boxart.get_width() and mouse_y > santaY - 100 and mouse_y < santaY - 100 + Santa_boxart.get_height():
					Santa_start = True
				if mouse_x > grinchX and mouse_x < grinchX - 50 + Grinch_boxart.get_width() and mouse_y > grinchY -50 and mouse_y < grinchY - 50 + Grinch_boxart.get_height():
					Grinch_start = True
		
		pygame.display.update()
		fpsClock.tick(FPS)
		
	if Santa_start == True:
		current_playerX = santaX
		current_playerY = santaY
		current_image = santa
		enemy_playerX = grinchX
		enemy_playerY = grinchY
		enemy_image = grinch
	else:
		current_playerX = santaX
		current_playerY = santaY
		current_image = grinch
		enemy_playerX = grinchX
		enemy_playerY = grinchY
		enemy_image = santa
		
	is_dragged = False
	
	RenderList = []
	Target = None
	Pressed = False
	Down = False
	Released = False
	collision = 0
	
	while True:
		
		DISPLAYSURF.blit(BG, (0, 0))
		
		# Draw player area
		#pygame.draw.rect(DISPLAYSURF, BLACK, santa_area)
		#pygame.draw.rect(DISPLAYSURF, BLACK, grinch_area)
		
		DISPLAYSURF.blit(current_image, (current_playerX, current_playerY))
		DISPLAYSURF.blit(enemy_image, (enemy_playerX, enemy_playerY))
		for b in bomb_list:
			DISPLAYSURF.blit(bomb, (b[0], b[1]))
			if Grinch_start:
				b[1] -= bombSpeed
			else:
				b[1] += bombSpeed
			if Santa_start == False:
				if b[0] > enemy_playerX and b[0] < enemy_playerX + enemy_image.get_width() and b[1] > enemy_playerY and b[1] < enemy_playerY + enemy_image.get_height():
					collision = collision + 1
					if collision == 5:
						while True:
							DISPLAYSURF.blit(Intro_BG, (0, 0))
							DISPLAYSURF.blit(game_over, ((Intro_BG.get_width() / 2) - 200, grinchY + 25))
							for event in pygame.event.get():
								if event.type == QUIT:
									pygame.quit()
									sys.exit()
							pygame.display.update()
							fpsClock.tick(FPS)
		
				if (b[0] + bomb.get_width()) > enemy_playerX and (b[0] + bomb.get_width()) < (enemy_playerX + enemy_image.get_width()) and (b[1] + bomb.get_height()) > enemy_playerY and (b[1] + bomb.get_height()) < (enemy_playerY + enemy_image.get_height()):
					collision = collision + 1
					if collision == 5:
						while True:
							DISPLAYSURF.blit(Intro_BG, (0, 0))
							DISPLAYSURF.blit(game_over, ((Intro_BG.get_width() / 2) - 200, grinchY + 25))
							for event in pygame.event.get():
								if event.type == QUIT:
									pygame.quit()
									sys.exit()
							pygame.display.update()
							fpsClock.tick(FPS)
			if Santa_start == True:
				if b[0] > current_playerX and b[0] < current_playerX + current_image.get_width() and b[1] > current_playerY and b[1] < current_playerY + current_image.get_height():
					collision = collision + 1
					if collision == 5:
						while True:
							DISPLAYSURF.blit(Intro_BG, (0, 0))
							DISPLAYSURF.blit(game_over, ((Intro_BG.get_width() / 2) - 200, grinchY + 25))
							for event in pygame.event.get():
								if event.type == QUIT:
									pygame.quit()
									sys.exit()
							pygame.display.update()
							fpsClock.tick(FPS)
		
				if (b[0] + bomb.get_width()) > current_playerX and (b[0] + bomb.get_width()) < (current_playerX + current_image.get_width()) and (b[1] + bomb.get_height()) > current_playerY and (b[1] + bomb.get_height()) < (current_playerY + current_image.get_height()):
					collision = collision + 1
					if collision == 5:
						while True:
							DISPLAYSURF.blit(Intro_BG, (0, 0))
							DISPLAYSURF.blit(game_over, ((Intro_BG.get_width() / 2) - 200, grinchY + 25))
							for event in pygame.event.get():
								if event.type == QUIT:
									pygame.quit()
									sys.exit()
							pygame.display.update()
							fpsClock.tick(FPS)
		
		pos = pygame.mouse.get_pos()
		'''
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				is_dragged = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				while event.type != pygame.MOUSEBUTTONUP:
					mouse_x ,mouse_y = pygame.mouse.get_pos()
					if mouse_x > current_playerX and mouse_x < current_playerX + current_image.get_width() and mouse_y > current_playerY and mouse_y < current_playerY + current_image.get_height():
						is_dragged = True
						current_playerX = mouse_x - current_image.get_width() / 2
			if event.type == pygame.MOUSEMOTION:
				if is_dragged == True:
					current_playerX = mouse_x - current_image.get_width() / 2
						'''
		for event in pygame.event.get():
			#pos2 = Transfer.receive()
			#print(pos2)
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				Released = False
				Pressed = True
				Down = True
			elif event.type == pygame.MOUSEBUTTONUP:
				Released = True
				Pressed = False
				Down = False
			elif event.type == pygame.KEYDOWN:
				if Grinch_start == True:
					bomb_list.append([current_playerX, current_playerY])
					if Grinch_start == True:
						Transfer.send(sendip, semdport, str("Bomb:" + str(current_playerX)))
									
		if Pressed == True:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			if mouse_x > current_playerX and mouse_x < current_playerX + current_image.get_width() and mouse_y > current_playerY and mouse_y < current_playerY + current_image.get_height():
				current_playerX = mouse_x - current_image.get_width() / 2
				Transfer.send(sendip, semdport, str("Playerposition:" + str(current_playerX)))
					
		if Down and Target != None:
			Target.pos = pos
		if Released:
			Target = None
		
		pygame.display.update()
		fpsClock.tick(FPS)
		
		
#def set_enemy_imageX(pos2):
#	enemy_imageX = pos2		