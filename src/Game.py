from pygame_functions import *
from pygame.locals import *
from random import randint
import Rodovia as r
import Galinha as g
import sys
import pygame
from time import sleep
from time import time
import Menu
import socket

CAMINHAO = 0
AMBULANCIA = 1
POLICIA = 2
POPULAR = 3

class Game:

	def __init__(self, mapa, numJog, IP, PORTA):

		pygame.init()
		self.info = pygame.display.Info()
		self.width = 1024
		self.height = 680
		screenSize(self.width,self.height)
		self.display_G = pygame.display.set_mode((self.width, self.height),  pygame.HWSURFACE)

		pygame.display.set_caption('Freeway')
		pygame.mixer.init()
		MUSIC_END = pygame.USEREVENT+1
		pygame.mixer.music.set_endevent(MUSIC_END)
		pygame.mixer.set_num_channels(5)
		# pygame.mixer.Sound.set_volume(0.2)

		self.fonte = pygame.font.SysFont("comicsansms", 50)
		self.win = pygame.image.load("../Sprites/win.png").convert_alpha()
		self.gameOver = pygame.image.load("../Sprites/gameOver.png").convert_alpha()
		self.galinha = g.Galinha('none', 3, [0, self.height-35], 0, randint(0, 3))
		
		self.numJog = numJog
		self.connectPlayer(numJog, IP, PORTA)
		self.rodovia = r.Rodovia(mapa, self.galinha, numJog, self.width)

	def connectPlayer(self, numJog, IP, PORTA):

		if self.galinha.connect2ServerPC(IP, PORTA, numJog, 'izi', mapa):
			print("Galinha carros"+self.galinha.nome+" conectada com sucesso!")
			if self.galinha.connect2ServerPG(IP, PORTA):
				print("Galinha posicao"+self.galinha.nome+" conectada com sucesso!")
		else:
			print("Falha ao conectar ao servidor")

	def drawCountDown(self):
		num = [pygame.image.load("../Sprites/num1.png").convert_alpha(),
			  pygame.image.load("../Sprites/num2.png").convert_alpha(),
			  pygame.image.load("../Sprites/num3.png").convert_alpha()]

		for i in range(2, -1, -1):
			self.display_G.fill([255,255,255])
			self.display_G.blit(self.rodovia.mapa,(0, 0))
			self.drawScores()
			self.galinha.draw(self.display_G, self.galinha.spritesUP)
			self.display_G.blit(num[i], ((self.width/2) - 27, (self.height/2) - 50))
			pygame.display.flip()
			sleep(1)

	def drawSearch(self):

		loading = []
		lbInst = makeLabel("Buscando por outros Jogadores...", 70, 120, 500, "white", "Agency FB", (131,163,2))
		showLabel(lbInst)
		for i in range(1, 9):
			loading.append(pygame.image.load("../Sprites/loading/l"+str(i)+".png").convert_alpha())

		i = 0
		clock = pygame.time.Clock()
		self.galinha.socketConnectPC.settimeout(0.001)
		while True:
			self.display_G.blit(loading[i], ((1024/2)-50, 290))
			pygame.display.flip()
			i += 1
			if i == 8: i = 0
			try:
				x = str(self.galinha.socketConnectPC.recv(16384))
				if x.find('::') != -1: break
			except socket.timeout: pass
			clock.tick(30)
		self.galinha.socketConnectPC.settimeout(1)

	def drawScores(self):
		score = self.fonte.render(str(self.galinha.pontuacao), 1, self.galinha.cor[1])
		self.display_G.blit(score, (self.galinha.coord[0]-32, 10))

	def draw(self, init):
		self.display_G.fill([255,255,255])
		self.display_G.blit(self.rodovia.mapa,(0, 0))
		self.drawScores()
		if self.galinha.moveUPDOWN == 0: self.galinha.draw(self.display_G, self.galinha.spritesUP)
		elif self.galinha.moveUPDOWN == 1: self.galinha.draw(self.display_G, self.galinha.spritesDOWN)
		elif self.galinha.moveUPDOWN == -1: self.galinha.draw(self.display_G, self.galinha.spritesDOWN)
		if self.rodovia.indexExp >= 0: self.rodovia.drawExplosao(self.display_G)
		if self.rodovia.draw(self.display_G) == 'end': self.endGame(False)
		self.galinha.drawVida(self.display_G)
		if init: self.drawCountDown()
		# self.rodovia.drawExplosao(self.display_G)
		pygame.display.flip()
		# pygame.display.update()

	def endGame(self, win_loser):

		if win_loser:
			self.display_G.blit(self.win, ((self.width/2)-257, (self.height/2)-102))
			pygame.display.flip()
			sleep(3)
		else:
			print(self.width)
			self.display_G.blit(self.gameOver, ((self.width/2)-140, (self.height/2)-116))
			pygame.display.flip()
			sleep(3)

		sys.exit(0)

	def play(self):

		clock = pygame.time.Clock()
		pygame.key.set_repeat(20)
		init = True
		inicio = fim = 0
		inicio2 = fim2 = -1
		poder = False
		while True:
			
			self.rodovia.updateVias()
			self.draw(init)
			init = False
			self.galinha.move = False

			pygame.event.pump()
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.type == pygame.QUIT: return
					if event.key == pygame.K_ESCAPE: return False
					if event.key == pygame.K_RETURN: return
					if event.key == pygame.K_2:
						self.galinha.imb = 1

					if event.key == pygame.K_1 and not self.galinha.invis and not poder: 
						self.galinha.invis = True
						poder = True
						inicio = time()
						# fim = time.time()
					if event.key == pygame.K_DOWN and not self.galinha.morta and not self.galinha.stop: 
						self.galinha.moveDown()
					if event.key == pygame.K_UP and not self.galinha.morta and not self.galinha.stop: 
						self.galinha.moveUp()

			if self.galinha.stop and inicio2 == -1:
				inicio2 = time()

			if self.galinha.stop:
				fim2  = (time() - inicio2)

			if self.galinha.invis: fim  = (time() - inicio)
			if fim >= 1: 
				fim = inicio = 0
				self.galinha.invis = False
			if fim2 >= 2: 
				fim2 = inicio2 = -1
				self.galinha.stop = False

			if self.galinha.atravessou(): 
				self.galinha.moveInicio()
				self.galinha.pontuacao +=1 

			if self.galinha.vida == 0: 
				self.galinha.morta = True
				self.galinha.moveUPDOWN = -1

			if self.galinha.pontuacao == 3: return True

			clock.tick(60)



parametros = sys.argv[1:]
IP = parametros[0]
PORTA = int(parametros[1])
menu = Menu.Menu()
mapa, numJog = menu.draw()
game = Game(mapa, numJog, IP, PORTA)
if numJog != 1: game.drawSearch()
game.endGame(game.play())

