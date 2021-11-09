import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import numpy as np

REPEAT = 4
N = 28
x, y = np.meshgrid(range(N), range(N))

Tk().withdraw()
directory = askopenfilename()
Tk().destroy()
root_directory = os.path.dirname(os.path.abspath(directory))

files_to_plot = []
for roots, dirs, files in os.walk(root_directory):
	for file_ in files:
		if file_.endswith('.csv'):
			files_to_plot.append(root_directory + '\\' + file_)
		
print(files_to_plot, type(files_to_plot))
for file in files_to_plot:
	data = pd.read_csv(file)
	for i in range(int(data.shape[0]/REPEAT)):
		xspin = [l for l in range(REPEAT)]
		yspin = [l for l in range(REPEAT)]
		zspin = [l for l in range(REPEAT)]
		
		fig = plt.figure()
		
		axes = [a for a in range(REPEAT)]
		for k in range(REPEAT):
			
			xspin[k] = data.iloc[i*REPEAT + k, 0:N**2].values.reshape(N, N)
			yspin[k] = data.iloc[i*REPEAT + k, N**2:2*(N**2)].values.reshape(N, N)
			zspin[k] = data.iloc[i*REPEAT + k, 2*(N**2):3*(N**2)].values.reshape(N, N)
			
			axes[k] = fig.add_subplot(2,2, k+1)
			axes[k].set_aspect(1.0)
			axes[k].quiver(x, y, xspin[k], yspin[k], units='x', pivot='middle', width=0.15, scale=1, scale_units='x')
			axes[k].scatter(x, y, c=zspin[k], s=15, cmap='rainbow', alpha=0.75)
		
		D = data.iloc[i*REPEAT, 3*(N**2)]
		B = data.iloc[i*REPEAT, 3*(N**2)+1]
		T = data.iloc[i*REPEAT, 3*(N**2)+2]
		
		D = float(np.round_(D, decimals = 2))
		B = float(np.round_(B, decimals = 2))
		T = float(np.round_(T, decimals = 2))
		print(D, B, T)
		
		B_str = str(B).split('.')[0] + '_' + str(B).split('.')[1]
		D_str = str(D).split('.')[0] + '_' + str(D).split('.')[1]
		T_str = str(T).split('.')[0] + '_' + str(T).split('.')[1]
		filename_to_save = 'D'+D_str+'B'+B_str+'T'+T_str+".jpg"
		fig.suptitle("D=%s, B=%s, T=%s"%(D, B, T), fontsize = 12)
		plt.savefig(root_directory + '\\' + filename_to_save, dpi =300)
		print(root_directory + '\\' + filename_to_save + "has been saved")
		plt.close(fig)