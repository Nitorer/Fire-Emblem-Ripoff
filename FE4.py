import pygame
from Sprites import *
from Vars import * # type: ignore
import random
import math
import time
import json
import os 

#Keep the variables in Config.py
#Make a layer that shows how much they can move
#Have the function check every position on the map and then see if the tile is less than mov away, if it is then blit a blue square on it.
#Use a dictionary to store the positions of everything, then use a function to search in the dictionary to see if the x and y are the same



class Game:


	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((960,640))
		self.clock = pygame.time.Clock()
		self.font = pygame.font.Font("gba-fe-dialogue.ttf", 40)
		self.running = True
		self.playing = True

		self.mov_surface = pygame.Surface((960, 640), pygame.SRCALPHA) 


	def new(self):
		#self.playing = True

		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()

		self.selector = Selector(self, Sx, Sy)
		self.lyn = Lyn(self, PositionDict["Lyn"][0], PositionDict["Lyn"][1]) # type: ignore
		self.brigand = Brigand(self, PositionDict["Brig"][0], PositionDict["Brig"][1])


#Finds what character the Selector is on by comparing the Array in the Position Dictionary, and assigns Ly and Lx to the
#selected character 
	def GetCharPosKey(self, x, y):
		value = next((i for i in PositionDict if PositionDict[i] == [x, y]), None)
		print(value)
		return value


	def AssignCharVar(self):
		global Ly, Lx
		CharKey = self.GetCharPosKey(Sx, Sy)
		
		Lx = PositionDict[CharKey][0]
		Ly = PositionDict[CharKey][1]

		print(Lx, Ly)


#Movement 

	def MovLeft(self, x):
		global Sx
		Sx -= 1
		SelectorPos[0] = Sx  

	def MovRight(self, x):
		global Sx
		Sx += 1
		SelectorPos[0] = Sx 

	def MovUp(self, y):
		global Sy
		Sy -= 1
		SelectorPos[1] = Sy

	def MovDown(self, y):
		global Sy
		Sy += 1
		SelectorPos[1] = Sy
			






	#Funtion to limit the amount of spaces a unit can move 
	def MoveLim(self, PrevLy, PrevLx, Lx, Ly):
		Distance = (abs(Lx - PrevLx) + abs(Ly - PrevLy))
		return Distance <= 5

	def DrawMovDistance(self, PrevLy, PrevLx, Mov):
		self.mov_surface.fill((0, 0, 0, 0))  # Clear the surface with transparency
		for x in range(15):
			for y in range(10):
				if (abs(Sx - x)) + (abs(Sy - y)) < Mov + 1:
	                # Draw the movement tile onto the mov_surface
					self.mov_surface.blit(MovTile, (x * 64, y * 64))



	def ClearSurface(self):
		self.mov_surface.fill((0,0,0,0))


	def events(self):
		global Sx, Sy, Lx, Ly, Over, PrevLx, PrevLy, CharKey
		pygame.key.set_repeat(200)
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
				self.playing = False
			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_LEFT:
					if self.MoveLim(PrevLy, PrevLx, Lx-1, Ly): #and self.GetCharPosKey(Sx-1,Sy) == None:
						self.MovLeft(Sx)
						if Sx < 0:
							Sx = 0

						if Over:
							PositionDict[CharKey][0] = Sx
							Lx = PositionDict[CharKey][0]

						print(Sx, Sy)


				if event.key == pygame.K_RIGHT:
					
					if self.MoveLim(PrevLy, PrevLx, Lx+1, Ly): #and self.GetCharPosKey(Sx+1,Sy) == None :
						self.MovRight(Sx)
						if Sx > 14:
							Sx = 14

						if Over:
							PositionDict[CharKey][0] = Sx
							Lx = PositionDict[CharKey][0]					

						print(Sx, Sy)

				if event.key == pygame.K_UP:
					
					if self.MoveLim(PrevLy, PrevLx, Lx, Ly-1): #and self.GetCharPosKey(Sx,Sy-1) == None:
						self.MovUp(Sy)

						if Sy < 0:
							Sy = 0						
						if Over:
							PositionDict[CharKey][1] = Sy
							Ly = PositionDict[CharKey][1]
						
						print(Sx, Sy)
				if event.key == pygame.K_DOWN:
					
					if self.MoveLim(PrevLy, PrevLx, Lx, Ly+1):# and self.GetCharPosKey(Sx,Sy+1) == None:
						self.MovDown(Sy)
						if Sy > 9:
							Sy = 9

						if Over:
							PositionDict[CharKey][1] = Sy
							Ly = PositionDict[CharKey][1]

						print(Sx, Sy)

				if event.key == pygame.K_a:
					CharKey = self.GetCharPosKey(Sx,Sy)
					if CharKey != None:
						self.AssignCharVar()
						Over = not Over
						self.DrawMovDistance(PrevLy,PrevLx,Mov)
						PrevLx = Lx
						PrevLy = Ly
						if Over == False:
							self.ClearSurface()
					
				if event.key == pygame.K_s:
					self.ClearSurface()
					
					PositionDict[CharKey][0] = PrevLx
					PositionDict[CharKey][1] = PrevLy
					Over = False

				if event.key == pygame.K_q:
					self.StatScreen()




	def draw_text(self, text, font, color, surface, x, y):
		textobj = font.render(text, 1, color)
		textrect = textobj.get_rect()
		textrect.topleft = (x, y)
		surface.blit(textobj, textrect)





	def StatScreen(self):

		running = True
		statposX = (405)
		statposY = (105)
		while running:
			self.screen.fill((0,211,0))
			pygame.draw.rect(self.screen,(255,255,0),pygame.Rect(395,95,530,410))
			pygame.draw.rect(self.screen,(96,76,225),pygame.Rect(400,100,520,400))
			#Position then size for rect 



	 
			self.draw_text('Character Screen', self.font, (139,0, 0), self.screen,500, 20)


			with open("Stats.json","r") as f:
				statsDict = json.load(f)
			for stat,value in statsDict["Lyn"]["char_stats"].items():
				self.draw_text(stat + ": " + str(value), self.font, (0,0,0), self.screen, statposX, statposY )

				statposY = statposY + 70
				if statposY >= 480:
					statposY = 105
					statposX = 625
			statposY = 105
			statposX = 405
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
					
			self.screen.blit(LynFaceL, (30,10))
			pygame.display.update()


	def update(self):
		self.all_sprites.update()
		self.new()


	def draw(self):
		self.screen.blit(BACKGROUND, (0, 0))
		# Draw movement tiles surface on the main screen
		self.screen.blit(self.mov_surface, (0, 0))
		self.all_sprites.draw(self.screen)
		self.clock.tick(FPS)
		pygame.display.update()

	def main(self):
		#loop
		while self.playing:
			self.events()
			self.update()
			self.draw()
		self.running = False


g = Game()
g.new()
while g.running:
	g.main()

pygame.quit()