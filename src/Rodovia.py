import Via as via
import pygame
from time import sleep
from sys import exit
from random import randint
from termcolor import colored
import Veiculo as v
import Galinha as g
import socket

CAMINHAO = 0
AMBULANCIA = 1
POLICIA = 2
POPULAR = 3

FAROLD = pygame.image.load("../Sprites/farol.png").convert_alpha()
FAROLE = pygame.image.load("../Sprites/farole.png").convert_alpha()

class Rodovia:

	def __init__(self, mapa, galinha, numPlayers, width):
		self.mp = mapa
		v.MAPA = mapa
		if mapa != '1':
			self.mapa = pygame.image.load("../Sprites/rodovias/rodovia"+mapa+".jpg").convert()
		else: 
			self.mapa = pygame.image.load("../Sprites/rodovias/rodovia"+mapa+".png").convert()
		self.mapa = pygame.transform.scale(self.mapa, (1024, 680))

		self.vias = []
		self.width = width
		self.numPlayers = numPlayers
		self.galinha = galinha
		for i in range(0, 10): self.vias.append(via.Via())
		self.sangue = []
		self.explosao = []
		for i in range(0, 64):
			if i < 10: self.explosao.append(pygame.image.load("../Sprites/explosao/type_B-0"+str(i)+"-00.png").convert_alpha())
			else: self.explosao.append(pygame.image.load("../Sprites/explosao/type_B-"+str(i)+"-00.png").convert_alpha())
		
		self.indexExp = -1
		self.coordCol = None
		self.saveVeiculos = []
		self.idVeiculos = 0
		self.notDraw = {}
		self.fonte = pygame.font.SysFont("comicsansms", 50)

	def drawExplosao(self, display_G):
		display_G.blit(self.explosao[self.indexExp], self.coordCol)
		self.indexExp += 1
		if self.indexExp == 63: self.indexExp = -1

	def updateVias(self):
		self.idVeiculos = self.vias[0].gerarVeiculo([1140, 50+(27-18)], 0, self.idVeiculos)
		self.idVeiculos = self.vias[1].gerarVeiculo([1140, 50+59+(27-18)], 1, self.idVeiculos)
		self.idVeiculos = self.vias[2].gerarVeiculo([1140, 50+(2*59)+(27-18)], 2, self.idVeiculos)
		self.idVeiculos = self.vias[3].gerarVeiculo([1140, 50+(3*59)+(27-18)], 3, self.idVeiculos)
		self.idVeiculos = self.vias[4].gerarVeiculo([1140, 50+(4*59)+(27-18)], 4, self.idVeiculos)
		self.idVeiculos = self.vias[5].gerarVeiculo([-115, 50+(5*59)+(27-18)], 5, self.idVeiculos)
		self.idVeiculos = self.vias[6].gerarVeiculo([-115, 50+(6*59)+(27-18)], 6, self.idVeiculos)
		self.idVeiculos = self.vias[7].gerarVeiculo([-115, 50+(7*59)+(27-18)], 7, self.idVeiculos)
		self.idVeiculos = self.vias[8].gerarVeiculo([-115, 50+(8*59)+(27-18)], 8, self.idVeiculos)
		self.idVeiculos = self.vias[9].gerarVeiculo([-115, 50+(9*59)+(27-18)], 9, self.idVeiculos)


	def saveCoordVeic(self, veiculos):
		
		arq = open('veiculosIZI.txt', 'w')

		for veiculo in veiculos:
			arq.write(str(veiculo.tipo)+'::'+str(veiculo.velocidade)+'::'+str(veiculo.via)+'::'+str(veiculo.coord[0])+'::'
			+str(veiculo.coord[1])+'::'+str(veiculo.id)+'::'+str(veiculo.indexImgPE)+'::'+str(veiculo.indexImgPD)+'\n')

		arq.close()		

	def getCoodVeic(self):
		coordenadasV = str(self.galinha.socketConnectPC.recv(16384))
		coordenadasV = coordenadasV.split("$")

		veiculos = []
		for received in coordenadasV:
			try:
				if len(received.split("::")) != 8: continue

				if received.find('b') != -1:
					received = received[2:len(received)]
				received = received.split("::")
				veiculo = v.Veiculo([float(received[3]), float(received[4])], int(received[2]))
				veiculo.tipo = int(received[0])
				veiculo.id = int(received[5])
				veiculo.indexImgPE = int(received[6])
				veiculo.indexImgPD = int(received[7])
				if veiculo.tipo == CAMINHAO: veiculo.getCaminhao()
				if veiculo.tipo == POPULAR: veiculo.getPopular()
				if veiculo.tipo == AMBULANCIA: veiculo.getAmbulancia()
				if veiculo.tipo == POLICIA: veiculo.getPolicia()
				veiculos.append(veiculo)
			except: pass
		return veiculos

	def getPosGs(self, posGs, display_G):

		galinhas = []
		coords = []
		vidas = []
		for pg in posGs:
			if len(pg) < 4: continue
			if pg.find('b') != -1:
				pg = pg[2:len(pg)]

			nome, x, y, updown, indexCor, pontos, vida, imb = pg.split('::')[0], int(pg.split('::')[1]), int(pg.split('::')[2]), int(pg.split('::')[3]), int(pg.split('::')[4]), int(pg.split('::')[5]), int(pg.split('::')[6]), int(pg.split('::')[7])
			vidas.append(vida)
			gInim = g.Galinha(nome, 3, [x, y], 0, indexCor)
			score = self.fonte.render(str(pontos), 1, gInim.cor[1])
			display_G.blit(score, (gInim.coord[0]-32, 10))
			if imb == 1 and nome != self.galinha.nome:
				self.galinha.stop = True

			if nome != self.galinha.nome:
				# print('Adversario: ', nome, indexCor)
				if updown == 1:
					display_G.blit(gInim.spritesDOWN[1], (x, y))
				elif updown == -1:
					display_G.blit(gInim.spriteMorta, (x, y))
				else: 
					display_G.blit(gInim.spritesUP[1], (x, y))
			galinhas.append(gInim)

		if all(i == 0 for i in vidas):
			return 'end'
		return galinhas


	def draw(self, display_G):

		SIRENE_AMBULANCIA = False
		SIRENE_POLICIA = False
		REMOVE_VEIC = False
		veiculos = self.getCoodVeic()
		if len(veiculos) > 100:
			veiculos = veiculos[:100]			
		
		try:
			self.galinha.sendPos()
		except: pass
		
		posG = str(self.galinha.socketConnectPG.recv(16384))
		posG = posG.split("$")
		galinhas = self.getPosGs(posG, display_G)
		if galinhas == 'end': return 'end'
		for veiculo in veiculos:

			if veiculo == -1: continue
			if veiculo.id in self.notDraw: continue

			if veiculo.via <= 4:

				for chicken in galinhas:

					if chicken.colisao(veiculo.imagemE, veiculo.coord):
						if chicken.nome == self.galinha.nome and self.galinha.invis: continue
						self.indexExp = 0
						self.coordCol = (veiculo.coord[0]-80, veiculo.coord[1]-80)
						if chicken.nome == self.galinha.nome:
							self.galinha.moveInicio()
							self.galinha.vida -= 1
						REMOVE_VEIC = True

				if self.mp == 'Noite' and veiculo.tipo == AMBULANCIA: display_G.blit(FAROLE, (veiculo.coord[0]-73, veiculo.coord[1]+3)) 
				elif self.mp == 'Noite': display_G.blit(FAROLE, (veiculo.coord[0]-65, veiculo.coord[1]))
				display_G.blit(veiculo.imagemE, veiculo.coord)
			else:

				for chicken in galinhas:

					if chicken.colisao(veiculo.imagemD, veiculo.coord):
						if chicken.nome == self.galinha.nome and self.galinha.invis: continue
						self.indexExp = 0
						self.coordCol = (veiculo.coord[0]-70, veiculo.coord[1]-80)
						if chicken.nome == self.galinha.nome: 
							self.galinha.moveInicio()
							self.galinha.vida -= 1
						REMOVE_VEIC = True

				if self.mp == 'Noite' and veiculo.tipo == AMBULANCIA: display_G.blit(FAROLD, (veiculo.coord[0]+73, veiculo.coord[1]-5)) 
				elif self.mp == 'Noite': display_G.blit(FAROLD, (veiculo.coord[0]+55, veiculo.coord[1]-5))
				display_G.blit(veiculo.imagemD, veiculo.coord)

			# buzinar
			if self.galinha.colisao(veiculo.imagemD, [veiculo.coord[0]+450, veiculo.coord[1]]):
				print("businarrrrrrrrrr")
				v.SOM_POP.play()
			if veiculo.tipo == AMBULANCIA and not SIRENE_AMBULANCIA:
				v.SOM_AMB.play()
				SIRENE_AMBULANCIA = True
			if veiculo.tipo == POLICIA and not SIRENE_POLICIA:
				v.SOM_POL.play()
				# veiculo.som.play()
				SIRENE_POLICIA = True

			if REMOVE_VEIC:
				if veiculo.id not in self.notDraw:
					self.notDraw[veiculo.id] = 0
				REMOVE_VEIC = False


	def draw2(self, display_G):
		SIRENE_AMBULANCIA = False
		REMOVE_VEIC = False
		SIRENE_POLICIA = False
		# print("LEN: >> ", len(self.saveVeiculos), end='\r')
		# if len(self.saveVeiculos) > 400000: 
			# self.saveCoordVeic(self.saveVeiculos)
			# exit(0)
		fps = 0
		for i in range(0, 10):
			size = len(self.vias[i].veiculos)
			for j in range(0, size):
				fps += 1
				# print('len via: '+str(i)+'> '+str(len(self.vias[i].veiculos)))
				try:
					if self.vias[i].veiculos[j].coord[0] >= 1150 or self.vias[i].veiculos[j].coord[0] < -120:
						self.vias[i].veiculos.pop(j)
						continue
					else:
						veiculo = v.Veiculo([self.vias[i].veiculos[j].coord[0], self.vias[i].veiculos[j].coord[1]], i)
						veiculo.velocidade = self.vias[i].veiculos[j].velocidade
						veiculo.tipo = self.vias[i].veiculos[j].tipo
						veiculo.id = self.vias[i].veiculos[j].id
						veiculo.indexImgPE = self.vias[i].veiculos[j].indexImgPE
						veiculo.indexImgPD = self.vias[i].veiculos[j].indexImgPD
						self.saveVeiculos.append(veiculo)
				except: continue

				if i <= 4:
					if self.galinha.colisao(self.vias[i].veiculos[j].imagemE, self.vias[i].veiculos[j].coord):
						self.indexExp = 0
						self.coordCol = (self.vias[i].veiculos[j].coord[0]-80, self.vias[i].veiculos[j].coord[1]-80)
						self.galinha.moveInicio()
						REMOVE_VEIC = True
					
					self.vias[i].veiculos[j].coord[0] -= self.vias[i].veiculos[j].velocidade
					display_G.blit(self.vias[i].veiculos[j].imagemE, self.vias[i].veiculos[j].coord)
				else:
					
					if self.galinha.colisao(self.vias[i].veiculos[j].imagemD, self.vias[i].veiculos[j].coord):
						self.indexExp = 0
						self.coordCol = (self.vias[i].veiculos[j].coord[0]-70, self.vias[i].veiculos[j].coord[1]-80)
						self.galinha.moveInicio()
						REMOVE_VEIC = True

					self.vias[i].veiculos[j].coord[0] += self.vias[i].veiculos[j].velocidade
					display_G.blit(self.vias[i].veiculos[j].imagemD, self.vias[i].veiculos[j].coord)


				#buzinar
				if self.galinha.colisao(self.vias[i].veiculos[j].imagemD, [self.vias[i].veiculos[j].coord[0]+400, self.vias[i].veiculos[j].coord[1]]):
					# print("businarrrrrrrrrr")
					v.SOM_POL.play()

				if self.vias[i].veiculos[j].tipo == AMBULANCIA and not SIRENE_AMBULANCIA:
					self.vias[i].veiculos[j].som.play()
					SIRENE_AMBULANCIA = True
				if self.vias[i].veiculos[j].tipo == POLICIA and not SIRENE_POLICIA:
					self.vias[i].veiculos[j].som.play()
					SIRENE_POLICIA = True
				
				if REMOVE_VEIC:
					self.vias[i].veiculos.pop(j)
					REMOVE_VEIC = False

