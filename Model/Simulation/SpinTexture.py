import numpy as np
from numpy.random import rand

"""The mathematical functions"""

#Takes in two (phi, theta) tuples and return a dot product between the two.
def angle_dot(orient1, orient2):
    return np.sin(orient1[1])*np.sin(orient2[1])*np.cos(orient1[0]-orient2[0])+np.cos(orient1[1])*np.cos(orient2[1])

#Takes in two (phi, theta) tuples and return a Cartesian vector.
def angle_cross(orient1, orient2):
	phi1 = orient1[0]
	phi2 = orient2[0]
	theta1 = orient1[1]
	theta2 = orient2[1]
	
	x = np.sin(theta1)*np.sin(phi1)*np.cos(theta2)-np.sin(theta2)*np.sin(phi2)*np.cos(theta1)
	y = -np.sin(theta1)*np.cos(phi1)*np.cos(theta2)+np.cos(theta1)*np.sin(theta2)*np.cos(phi2)
	z = np.sin(theta1)*np.cos(phi1)*np.sin(theta2)*np.sin(phi2)-np.sin(theta1)*np.sin(phi1)*np.sin(theta2)*np.cos(phi2)
	return (x, y, z)
	
def angle_cross_x(orient1, orient2):
	phi1 = orient1[0]
	phi2 = orient2[0]
	theta1 = orient1[1]
	theta2 = orient2[1]
	return np.sin(theta1)*np.sin(phi1)*np.cos(theta2)-np.sin(theta2)*np.sin(phi2)*np.cos(theta1)
	
def angle_cross_y(orient1, orient2):
	phi1 = orient1[0]
	phi2 = orient2[0]
	theta1 = orient1[1]
	theta2 = orient2[1]
	return -np.sin(theta1)*np.cos(phi1)*np.cos(theta2)+np.cos(theta1)*np.sin(theta2)*np.cos(phi2)
	
def angle_cross_z(orient1, orient2):
	phi1 = orient1[0]
	phi2 = orient2[0]
	theta1 = orient1[1]
	theta2 = orient2[1]
	return np.sin(theta1)*np.cos(phi1)*np.sin(theta2)*np.sin(phi2)-np.sin(theta1)*np.sin(phi1)*np.sin(theta2)*np.cos(phi2)
	

"""If you want to change the chirality of this configuration, you need to change the direction of D"""	
class SpinTexture:
	#Generate a NxN array of randomly oriented spins
	def __init__(self):
		print("Please use initialize(N, B, D, J, T) to randomly generate a new model")
	
	#We want to generate a random spherical coordinate across the solid angle.
	#We know the theta must satisfy the sin(theta)/2 probability function
	def rand_orient(self):
		phi = np.random.uniform(0, 2*np.pi)
		theta = np.arccos(1 - 2 * np.random.uniform(0, 1))
		return (phi, theta)
	
	def initialize(self, N=28, k=1.38065*10**(-23), B=1, D=1, J=1, T=10):
		self.N = N
		self.B = B
		self.D = D
		self.J = J
		self.T = T
		self.k = k
		
		self.config = np.zeros((self.N, self.N, 2))
		self.energy = 0
		self.mag_x = 0
		self.mag_y = 0
		self.mag_z = 0
		self.beta = 1 / (self.k * self.T)
		
		for i in range(self.N):
			for j in range(self.N):
				self.config[i][j] = self.rand_orient()
				
		#Calculate the initial configuration's state.
		self.calcEnergy()
		print("A ", self.N, "x", self.N, "model generated, with initial energy ", self.energy)
		
		#Ideally, the x, y and z components should average to zeros
		self.calcMag_X()
		self.calcMag_Y() 
		self.calcMag_Z()
		print("The x, y and z components of the system is ", self.mag_x, self.mag_y, self.mag_z)
	
	#The Hamiltonian here is given by H=-sum(JSi dot Sj)-sum(D dot (Si cross Sj)) - sum(B dot Si)
	#D=0.72, J=1
	#The goal here is to make N^2 dots randomly reorient(The same dots can reorient multiple times).
	def mcmove(self):
		for i in range(self.N):
			for j in range(self.N):
				a = np.random.randint(0, self.N)
				b = np.random.randint(0, self.N)
				spin = self.config[a][b]
				#Calculate the energy before the spin reorientation
				dot = self.J * (angle_dot(self.config[(a+1)%self.N, b], spin) + angle_dot(self.config[(a-1)%self.N, b], spin) +
								angle_dot(self.config[a, (b+1)%self.N], spin) + angle_dot(self.config[a, (b-1)%self.N], spin))
				cross = self.D * (angle_cross_y(spin, self.config[(a+1)%self.N,b]) + angle_cross_y(self.config[(a-1)%self.N,b], spin) +
							angle_cross_x(spin, self.config[(a, (b+1)%self.N)]) + angle_cross_x(self.config[a, (b-1)%self.N], spin))
				Zeeman = self.B * np.cos(spin[1])
				E_loc1 = -dot - cross - Zeeman
				
				spin = self.rand_orient()
				#Calculate the energy after the spin reorientation
				dot = self.J * (angle_dot(self.config[(a+1)%self.N, b], spin) + angle_dot(self.config[(a-1)%self.N, b], spin) +
								angle_dot(self.config[a, (b+1)%self.N], spin) + angle_dot(self.config[a, (b-1)%self.N], spin))
				cross = self.D * (angle_cross_y(spin, self.config[(a+1)%self.N, b]) + angle_cross_y(self.config[(a-1)%self.N, b], spin) +
								angle_cross_x(spin, self.config[(a, (b+1)%self.N)]) + angle_cross_x(self.config[a, (b-1)%self.N], spin))
				Zeeman = self.B * np.cos(spin[1])
				E_loc2 = -dot - cross - Zeeman
				#If the energy decreases, the process is approved right away;
				#if not, this can still happend, though it needs activation energy now.
				deltaE_loc = E_loc2 - E_loc1
				if deltaE_loc < 0 or rand() < np.exp(-deltaE_loc * self.beta):
					self.config[a,b] = spin
					
	def equilibrate(self, max_iterations, delta=0.5):
		try:
			for i in range(max_iterations):
				self.mcmove()
				if i % 16 == 0:
					prev_energy = self.energy
					self.calcEnergy()
					delta_energy = self.energy - prev_energy
					if np.abs(delta_energy) < delta:
						print("The iteration converged and finished early around iteration ", i)
						break
					
			print("The system reaches an equilibrium")
			
			
		except KeyboardInterrupt:
			print("The iteration is interrupted by KeyboardInterrupt, but the state of the system is saved")
		
		print("The final energy of the system: ", self.energy)
		self.calcMag_X()
		self.calcMag_Y()
		self.calcMag_Z()
		print("The x, y and z components of the system is ", self.mag_x, self.mag_y, self.mag_z)
		
	def calcEnergy(self):
		self.energy = 0
		for i in range(len(self.config)):
			for j in range(len(self.config)):
				spin = self.config[i][j]
	
				dot_right_up = self.J * (angle_dot(self.config[(i+1)%self.N,j], spin) + angle_dot(self.config[i,(j+1)%self.N], spin))
				cross_right_up = self.D * (angle_cross_y(spin, self.config[(i+1)%self.N,j]) + angle_cross_x(spin, self.config[(i, (j+1)%self.N)]))
				Zeeman = self.B * np.cos(spin[1])
				self.energy += -dot_right_up - cross_right_up - Zeeman
	
	def calcMag_X(self):
		self.mag_x = 0
		print(self.N)
		for i in range(self.N):
			for j in range(self.N):
				self.mag_x += np.cos(self.config[i][j][1]) * np.cos(self.config[i][j][0])
		
	def calcMag_Y(self):
		self.mag_y = 0
		for i in range(self.N):
			for j in range(self.N):
				self.mag_y += np.sin(self.config[i][j][1]) * np.sin(self.config[i][j][0])
				
	def calcMag_Z(self):
		self.mag_z = 0
		for i in range(self.N):
			for j in range(self.N):
				self.mag_z += np.cos(self.config[i][j][1])
