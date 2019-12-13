from random import randint
from time import sleep
import pygame
import socket

#cores de galinha: branca, marrom, preta, verde
CORES = [('B', (255,255,255)), ('M', (127,108,53)), ('P', (0,0,0)), ('V', (50,205,50))]

class Galinha:

	def __init__(self, nome, vida, coord, pontuacao, indexCor):
		self.nome = nome
		self.vida = vida
		self.pontuacao = pontuacao
		self.coord = coord
		self.invis = False
		self.stop = False
		self.imb = 0
		self.move = False
		self.moveUPDOWN = 0
		self.spritesUP = []
		self.spritesDOWN = []
		self.spritesUPInv = []
		self.spritesDOWNInv = []
		self.indexCor = indexCor
		self.cor = CORES[indexCor]
		self.morta = False
		self.spriteMorta = pygame.image.load("../Sprites/galinhaMorta.png").convert_alpha()
		self.spriteCoracao = pygame.image.load("../Sprites/coracao2.png").convert_alpha()
		for i in range(1, 4):
			self.spritesUP.append(pygame.image.load("../Sprites/galinhas/galinha"+self.cor[0]+"/up/g"+str(i)+".png").convert_alpha())
			self.spritesDOWN.append(pygame.image.load("../Sprites/galinhas/galinha"+self.cor[0]+"/down/g"+str(i)+".png").convert_alpha())
			self.spritesUPInv.append(pygame.image.load("../Sprites/galinhas/galinha"+self.cor[0]+"/up/g"+str(i)+"i.png").convert_alpha())
			self.spritesDOWNInv.append(pygame.image.load("../Sprites/galinhas/galinha"+self.cor[0]+"/down/g"+str(i)+"i.png").convert_alpha())
		
	def drawVida(self, display_G):
		x = 20
		for i in range(0, self.vida):
			display_G.blit(self.spriteCoracao, (x,10))
			x += 30

	def draw(self, display_G, sprites):

		# display_G.blit(self.spritesUPInv[0], self.coord)
		# return
		if self.morta: 
			display_G.blit(self.spriteMorta, self.coord)
			return 
		if self.invis and self.moveUPDOWN == 0:
			display_G.blit(self.spritesUPInv[1], self.coord)
			return

		if self.invis and self.moveUPDOWN == 1:
			display_G.blit(self.spritesDOWNInv[1], self.coord)
			return

		for sprite in sprites:
			if not self.move: 
				display_G.blit(sprites[1], self.coord)
				return
			display_G.blit(sprite, self.coord)
			# pygame.display.flip()
		
	def colisao(self, veiculo, coordV):
		# self.rectGalinha = self.spritesUP[1].get_rect()
		self.rectGalinha = pygame.Rect(self.coord[0], self.coord[1]+10, 26, 26)
		# self.rectGalinha.top += 10
		# self.rectVeiculo = veiculo.get_rect()
		self.rectVeiculo = pygame.Rect(self.coord[0]-10, self.coord[1]+10, 50, 26)
		self.rectGalinha.x = self.coord[0]
		self.rectGalinha.y = self.coord[1]
		self.rectVeiculo.x = coordV[0]
		self.rectVeiculo.y = coordV[1]
		return self.rectGalinha.colliderect(self.rectVeiculo)


	def moveUp(self):
		self.coord[1] -= 5
		self.moveUPDOWN = 0
		self.move = True
	
	def moveDown(self):
		if self.coord[1] >= 645: return
		self.coord[1] += 5
		self.moveUPDOWN = 1
		self.move = True

	def moveInicio(self):
		self.coord[1] = 645

	def atravessou(self):
		return self.coord[1] <= 10

	def disconnect(self):
		self.socketConnectPC.close()
		self.socketConnectPG.close()

	def connect2ServerPC(self, IP, port, players, dific, mapa):

		self.socketConnectPC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socketConnectPC.connect((IP, port))

		message = self.nome+'::'+dific+'::'+str(players)+'::'+mapa+'\n'
		self.socketConnectPC.sendall(message.encode())

		received = str(self.socketConnectPC.recv(1024))
		print("Received: ", received)
		if received.find('ok') != -1:
			return True
		return False
# 204, 408, 612, 816 
	def connect2ServerPG(self, IP, port):

		self.socketConnectPG = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socketConnectPG.connect((IP, port))

		message = "myChicken"+'\n'
		self.socketConnectPG.sendall(message.encode())

		received = str(self.socketConnectPG.recv(1024))
		print("Received myChicken: ", received)
		if received.find('ok') != -1:
			self.coord[0] = int(received.split("::")[1])
			self.nome = received.split("::")[2]
			print(self.coord)
			# input(">")
			return True
		return False

	def sendPos(self):
		posGalinha = str(self.nome+'::'+str(self.coord[0]))+'::'+str(self.coord[1])+'::'+str(self.moveUPDOWN)+'::'+str(self.indexCor)+'::'+str(self.pontuacao)+'::'+str(self.vida)+'::'+str(self.imb)+'$'+'\n'
		self.socketConnectPG.sendall(posGalinha.encode())
		if self.imb == 1: self.imb = 0