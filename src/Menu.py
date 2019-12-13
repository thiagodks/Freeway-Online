from pygame.locals import *
from pygame_functions import *
from random import randint
import sys
import pygame
from time import sleep

class Menu:

	def __init__(self):
		pygame.init()
		self.info = pygame.display.Info()
		# self.width = self.info.current_w
		# self.height = self.info.current_h
		self.width = 1024
		self.height = 600

		screenSize(self.width,self.height)
		self.display_G = pygame.display.set_mode((self.width, self.height),  pygame.HWSURFACE)
		# self.display_G = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
		pygame.display.set_caption('Freeway')
		pygame.mixer.init()
		MUSIC_END = pygame.USEREVENT+1

		self.fonte = pygame.font.SysFont("comicsansms", 50)
		self.background = pygame.image.load("../Sprites/background2.jpg").convert_alpha()
		self.background = pygame.transform.scale(self.background, (self.width, self.height))

		self.mapaNoite = pygame.image.load("../Sprites/rodovias/mapas/rodoviaNoite.jpg").convert_alpha()
		self.mapaNeve = pygame.image.load("../Sprites/rodovias/mapas/rodoviaNeve.jpg").convert_alpha()
		self.mapaAquatico = pygame.image.load("../Sprites/rodovias/mapas/rodoviaAquatica.jpg").convert_alpha()
		self.mapaNormal = pygame.image.load("../Sprites/rodovias/mapas/rodovia1.png").convert_alpha()

		self.num1 = pygame.image.load("../Sprites/nump1.png").convert_alpha()
		self.num2 = pygame.image.load("../Sprites/nump2.png").convert_alpha()
		self.num3 = pygame.image.load("../Sprites/nump3.png").convert_alpha()
		self.num4 = pygame.image.load("../Sprites/nump4.png").convert_alpha()

		self.num1Select = pygame.image.load("../Sprites/nump1S.png").convert_alpha()
		self.num2Select = pygame.image.load("../Sprites/nump2S.png").convert_alpha()
		self.num3Select = pygame.image.load("../Sprites/nump3S.png").convert_alpha()
		self.num4Select = pygame.image.load("../Sprites/nump4S.png").convert_alpha()

		self.mapaNoiteSelect = pygame.image.load("../Sprites/rodovias/mapas/mapaNoite.png").convert_alpha()
		self.mapaNeveSelect = pygame.image.load("../Sprites/rodovias/mapas/mapaNeve.png").convert_alpha()
		self.mapaAquaticoSelect = pygame.image.load("../Sprites/rodovias/mapas/mapaAquatica.png").convert_alpha()
		self.mapaNormalSelect = pygame.image.load("../Sprites/rodovias/mapas/mapaNormal.png").convert_alpha()

		self.logo = pygame.image.load("../Sprites/logo.png").convert_alpha()
		self.play = pygame.image.load("../Sprites/play.png").convert_alpha()

		self.mapaNoite = pygame.transform.scale(self.mapaNoite, (320, 220))
		self.mapaNeve = pygame.transform.scale(self.mapaNeve, (320, 220))
		self.mapaNormal = pygame.transform.scale(self.mapaNormal, (320, 220))
		self.mapaAquatico = pygame.transform.scale(self.mapaAquatico, (320, 220))

		self.mapaNoiteSelect = pygame.transform.scale(self.mapaNoiteSelect, (320, 220))
		self.mapaNeveSelect = pygame.transform.scale(self.mapaNeveSelect, (320, 220))
		self.mapaNormalSelect = pygame.transform.scale(self.mapaNormalSelect, (320, 220))
		self.mapaAquaticoSelect = pygame.transform.scale(self.mapaAquaticoSelect, (320, 220))

		self.display_G.blit(self.background,(0, 0))
		self.display_G.blit(self.mapaNoite,(35, 80))
		self.display_G.blit(self.mapaNeve,(365, 80))
		self.display_G.blit(self.mapaNormal,(35, 320))
		self.display_G.blit(self.mapaAquatico,(365, 320))
		self.display_G.blit(self.logo,(695, 80))

		self.display_G.blit(self.num1,(35, 550))
		self.display_G.blit(self.num2,(35+45, 550))
		self.display_G.blit(self.num3,(35+90, 550))
		self.display_G.blit(self.num4,(35+135, 550))
		self.display_G.blit(self.play,(1000-160, 520))

		lbInst = makeLabel("SELECIONE O MAPA E O NÚMERO DE JOGADORES", 35, 35, 25, "white", "Agency FB", (131,163,2))
		showLabel(lbInst)
		pygame.display.flip()

	def clearSelect(self):
		self.display_G.blit(self.mapaNoite,(35, 80))
		self.display_G.blit(self.mapaNeve,(365, 80))
		self.display_G.blit(self.mapaNormal,(35, 320))
		self.display_G.blit(self.mapaAquatico,(365, 320))

	def clearSelectNumber(self):
		self.display_G.blit(self.num1,(35, 550))
		self.display_G.blit(self.num2,(35+45, 550))
		self.display_G.blit(self.num3,(35+90, 550))
		self.display_G.blit(self.num4,(35+135, 550))

	def draw(self):
		clock = pygame.time.Clock()
		MAPA = NUM = PLAY = ''
		while not PLAY:

			pygame.event.pump()
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = event.pos
					if 840 <= x <= 840 + 144:
						if 520 <= y <= 520 + 56:
							if MAPA != '' and NUM != '': PLAY = True

					if 35 <= x <= 35 + 355:
						if 80 <= y <= 80 + 220:
							self.clearSelect()
							self.display_G.blit(self.mapaNoiteSelect,(35, 80))
							pygame.display.flip()
							MAPA = 'Noite'
					
					if 365 <= x <= 365 + 355:
						if 80 <= y <= 80 + 220:
							self.clearSelect()
							self.display_G.blit(self.mapaNeveSelect,(365, 80))
							pygame.display.flip()
							MAPA = 'Neve'
					
					if 35 <= x <= 35 + 355:
						if 320 <= y <= 320 + 220:
							self.clearSelect()
							self.display_G.blit(self.mapaNormalSelect,(35, 320))
							pygame.display.flip()
							MAPA = '1'
					
					if 365 <= x <= 365 + 355:
						if 320 <= y <= 320 + 220:
							self.clearSelect()
							self.display_G.blit(self.mapaAquaticoSelect,(365, 320))
							pygame.display.flip()
							MAPA = 'Aquatica'
					
					if 35 <= x <= 35 + 38:
						if 550 <= y <= 550 + 47:
							self.clearSelectNumber()
							self.display_G.blit(self.num1Select,(35, 550))
							pygame.display.flip()
							NUM = 1

					if 80 <= x <= 80 + 38:
						if 550 <= y <= 550 + 47:
							self.clearSelectNumber()
							self.display_G.blit(self.num2Select,(80, 550))
							pygame.display.flip()
							NUM = 2
					
					if 125 <= x <= 125 + 38:
						if 550 <= y <= 550 + 47:
							self.clearSelectNumber()
							self.display_G.blit(self.num3Select,(125, 550))
							pygame.display.flip()
							NUM = 3
					
					if 170 <= x <= 170 + 38:
						if 550 <= y <= 550 + 47:
							self.clearSelectNumber()
							self.display_G.blit(self.num4Select,(170, 550))
							pygame.display.flip()
							NUM = 4

				if event.type == pygame.QUIT:
					return
			clock.tick(30)
		clearLabels()
		return MAPA, NUM
# menu = Menu()
# mapa, numP = menu.draw()