from random import *
import Veiculo as v

CAMINHAO = 0
AMBULANCIA = 1
POLICIA = 2
POPULAR = 3

class Via:

	def __init__(self):
		self.veiculos = []


	def verificaVel(self, veiculo, i):
		#veiculo gerado
		try:
			if  i > 4 and (veiculo.coord[0]+110 < self.veiculos[len(self.veiculos)-1].coord[0]):

				x_vec = veiculo.coord[0]+110
				dist_res = 1024 - x_vec
				temp_resN = (dist_res * 0.00000000002)/veiculo.velocidade

				x_vec = self.veiculos[len(self.veiculos)-1].coord[0]
				dist_res = 1024 - x_vec
				temp_resU = (dist_res * 0.00000000002)/self.veiculos[len(self.veiculos)-1].velocidade
				if temp_resU <= temp_resN: return True

			elif i <= 4 and (self.veiculos[len(self.veiculos)-1].coord[0]+110 < veiculo.coord[0]):
				x_vec = veiculo.coord[0]
				dist_res = 1024 - (1024 - x_vec)
				temp_resN = (dist_res * 0.00000000002)/veiculo.velocidade

				x_vec = self.veiculos[len(self.veiculos)-1].coord[0]+110
				dist_res = 1024 - (1024 - x_vec)
				temp_resU = (dist_res * 0.00000000002)/self.veiculos[len(self.veiculos)-1].velocidade
				if temp_resU <= temp_resN: return True

		except: return True
		
		return False


	def gerarVeiculo(self, coord, i, idVeiculos):
		prob = random()
		if prob > 0.01: return idVeiculos
		veiculo = v.Veiculo(coord, i)
		if veiculo.tipo == CAMINHAO: veiculo.getCaminhao()
		elif veiculo.tipo == AMBULANCIA: veiculo.getAmbulancia()
		elif veiculo.tipo == POLICIA: veiculo.getPolicia()
		elif veiculo.tipo == POPULAR: veiculo.getPopular()
		prob = random()
		if veiculo.tipo == CAMINHAO and prob > 0.05: return idVeiculos
		if veiculo.tipo == POPULAR and prob > 0.2: return idVeiculos
		if not self.verificaVel(veiculo, i): return idVeiculos

		veiculo.id = idVeiculos
		idVeiculos += 1
		self.veiculos.append(veiculo)
		return idVeiculos
