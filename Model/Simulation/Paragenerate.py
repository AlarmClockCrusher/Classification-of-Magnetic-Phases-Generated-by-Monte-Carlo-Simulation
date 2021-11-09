import multiprocessing as mp
from PhaseDiagram import PhaseDiagram
import numpy as np
import sys

num_processes = int(sys.argv[1])

file = open('/users/PAS1495/gsdbuilder/FinalProject/Parameters.txt', 'r')
print(file.readline())

N = int(file.readline().split('=')[1])
print(N)

file.readline()
Boltzmann = file.readline().split('=')[1]

k1 = float(Boltzmann.split('*')[0])
k2 = Boltzmann.split('**')[1]
k2 = int(k2.split('(')[1].split(')')[0])
k = k1 * 10 ** k2
print(k)

max_iterations = int(file.readline().split('=')[1])
print(max_iterations)
file.readline()
delta = float(file.readline().split('=')[1])
print(delta)
file.readline()
REPEAT = int(file.readline().split('=')[1])
print(REPEAT)
D_values = np.fromstring(file.readline().split('=')[1], dtype=float, sep=',')
print(D_values)
B_values = np.fromstring(file.readline().split('=')[1], dtype=float, sep=',')
print(B_values)
T_values = np.fromstring(file.readline().split('=')[1], dtype=float, sep=',')
print(T_values)


def part(D_values, B_values, T_values, N, k, max_iterations, delta, REPEAT, output):
	PhaseDiagram(D_values, B_values=B_values, T_values=T_values, N=N, max_iterations=max_iterations, delta=delta, REPEAT=REPEAT)

if __name__ == '__main__':
	output = mp.Queue()
	#Four precesses
	D_values = D_values.reshape(num_processes, -1)
	
	processes = [mp.Process(target=part, args=(D_values[i], B_values, T_values, N, k, max_iterations, delta, REPEAT, output)) for i in range(num_processes)]
	
	for p in processes:
		p.start()
		print("Process started")
		
	for p in processes:
		p.join()

