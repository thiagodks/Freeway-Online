from random import randint
import pygame

MAPA = 'Neve'

CAMINHAO = 0
AMBULANCIA = 1
POLICIA = 2
POPULAR = 3

pygame.init()
display_G = pygame.display.set_mode((10, 10), pygame.HWSURFACE|pygame.DOUBLEBUF, 32)

SOM_AMB = pygame.mixer.Sound('../sounds/sirene_ambulancia_n.ogg')
SOM_POP = pygame.mixer.Sound('../sounds/sirene_policia_n.ogg')
SOM_POL = pygame.mixer.Sound('../sounds/buzina_popular'+str(randint(1,2))+'_n.ogg')
SOM_CAM = pygame.mixer.Sound('../sounds/businaTruck2_n.ogg')
SOM_AMB.set_volume(0.008)
SOM_POL.set_volume(0.008)
SOM_POP.set_volume(0.01)
SOM_CAM.set_volume(0.008)

populares = ['Audi', 'Black_viper', 'Car', 'Mini_truck', 'Mini_van', 'taxi']
IMG_AMB = [pygame.image.load("../Sprites/veiculos/"+MAPA+"/Ambulance.png").convert_alpha(),
		   pygame.image.load("../Sprites/veiculos/"+MAPA+"/Ambulance_D.png").convert_alpha()]
IMG_POL = [pygame.image.load("../Sprites/veiculos/"+MAPA+"/Police.png").convert_alpha(),
		   pygame.image.load("../Sprites/veiculos/"+MAPA+"/Police_D.png").convert_alpha()]
# IMG_POP = [pygame.image.load("../Sprites/veiculos/"+populares[randint(0,5)]+'.png').convert_alpha(),
		   # pygame.image.load("../Sprites/veiculos/"+populares[randint(0,5)]+'_D.png').convert_alpha()]
IMG_CAM = [pygame.image.load("../Sprites/veiculos/"+MAPA+"/truck.png").convert_alpha(),
		   pygame.image.load("../Sprites/veiculos/"+MAPA+"/truck_D.png").convert_alpha()]

IMG_POP = [pygame.image.load("../Sprites/veiculos/"+MAPA+"/Audi.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/Black_viper.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/Car.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/Mini_truck.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/Mini_van.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/taxi.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/Audi_D.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/Black_viper_D.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/Car_D.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/Mini_truck_D.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/Mini_van_D.png").convert_alpha(),
			pygame.image.load("../Sprites/veiculos/"+MAPA+"/taxi_D.png").convert_alpha()]

FAROL = pygame.image.load("../Sprites/farol.png").convert_alpha()

class Veiculo:

	def __init__(self, coord, via):
		self.tipo = randint(0,3)
		self.coord = coord
		self.via = via
		self.id = -1
		self.indexImgPE = randint(0, 5)
		self.indexImgPD = randint(6, 11)

	def getAmbulancia(self):
		self.imagemE = IMG_AMB[0]
		self.imagemD = IMG_AMB[1]
		self.velocidade = 2.5
		self.som = SOM_AMB

	def getPolicia(self):
		self.imagemE = IMG_POL[0]
		self.imagemD = IMG_POL[1]
		self.velocidade = 2.3
		self.som = SOM_POL

	def getPopular(self):
		self.imagemE = IMG_POP[self.indexImgPE]
		self.imagemD = IMG_POP[self.indexImgPD]
		self.velocidade = 1.8
		self.som = SOM_POP

	def getCaminhao(self):
		self.imagemE = IMG_CAM[0]
		self.imagemD = IMG_CAM[1]
		self.velocidade = 1.8
		self.som = SOM_CAM
