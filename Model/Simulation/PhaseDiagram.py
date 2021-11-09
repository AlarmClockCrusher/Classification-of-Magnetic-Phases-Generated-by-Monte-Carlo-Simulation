import numpy as np
from SpinTexture import SpinTexture
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os

#We are going to fix J at 1 and select the range of D, B, and T.
def PhaseDiagram(D_values, B_values=np.arange(0.0, 2.0, 0.1), T_values=np.arange(0.5, 5, 0.5), N=28, k=1.38065*10**(-23), max_iterations=128, delta=0.1, REPEAT=4):
	"""
	N is the size of the model, delta is the early-stop criterion
	REPEAT is the number of test runs to test the stability of the model
	"""
	model = SpinTexture()
	
	x, y = np.meshgrid(range(N), range(N))
	xspin = np.zeros((N, N))
	yspin = np.zeros((N, N))
	zspin = np.zeros((N, N))
	
	filepath = "/users/PAS1495/gsdbuilder/FinalProject/Dataset/PhaseDiagram"
	D_lower = str(D_values.min()).split('.')[0] + '_' + str(D_values.min()).split('.')[1]
	D_upper = str(D_values.max()).split('.')[0] + '_' + str(D_values.max()).split('.')[1]
	filename = "D" + D_lower + '~'+ D_upper + ".csv"
			
	#Define the header of the csv file that stores all the simulation results at different conditions
	file = open(filepath + filename, 'w')
	print(filepath + filename + "created")
	for i in range(N):
		for j in range(N):
			file.write('xspin' + str(i*N+j+1) + ',')
		
	for i in range(N):
		for j in range(N):
			file.write('yspin' + str(i*N+j+1) + ',')
		
	for i in range(N):
		for j in range(N):
			file.write('zspin' + str(i*N+j+1) + ',')
	
	file.write('D,B,T,repeat\n')
	
	
	for D in D_values:
		for B in B_values:
			for T in T_values:
				print("Now processing D=%s, B=%s, T=%s" % (D, B, T))
				B_str = str(B).split('.')[0] + '_' + str(B).split('.')[1]
				D_str = str(D).split('.')[0] + '_' + str(D).split('.')[1]
				T_str = str(T).split('.')[0] + '_' + str(T).split('.')[1]
				for repeat in range(REPEAT):
					#Simulation part
					#initialize(self, N=28, B=1, D=1, J=1, T=10)
					#equilibrate(self, max_iterations, delta=0.5)
					model.initialize(N, k=k, B=B, D=D, T=T)
					model.equilibrate(max_iterations, delta=delta)
					
					for i in range(N):
						for j in range(N):
							zspin[i][j] = np.cos(model.config[i][j][1])
							xspin[i][j] = np.sin(model.config[i][j][1]) * np.cos(model.config[i][j][0])
							yspin[i][j] = np.sin(model.config[i][j][1]) * np.sin(model.config[i][j][0])					
					
					for row in range(N):
						#np.ndarray.tofile is a powerful way of writing 1D array into files.
						xspin[row].tofile(file, sep=',')
						file.write(',')
						
					for row in range(N):
						yspin[row].tofile(file, sep=',')
						file.write(',')
					
					for row in range(N):
						zspin[row].tofile(file, sep=',')
						file.write(',')
						
					file.write(str(D)+ ',' + str(B) + ',' + str(T) + ',' + str(repeat) + '\n')

