The project uses Monte Carlo simulation method to generate magnetic phases under different conditions.
The simulation methods are defined in the Simulation folder.(The phase diagram generation runs on the OSC. However, the SpinTexture class is able to run on PC)

The generated phases are fed to several different networks for classification test. The data used are shown in the Jupyter notebooks.
"Multiheaded.ipynb" is the most successful model, while "CVAE.ipynb", "VAE.ipynb" and "StackedNetwork.ipynb" are less satisfying attempts.

The different phases are spin spirals(labeled 2), skyrmions(labeled 0) and ferromagnetic phases(labeled 1).
The three phases, stored in the finalProject/Project/Model/SelectedPhases folder are picked from the data sets in this repo, e.g., lowD/ and newData/.

The train multiheaded network is saved and loaded in the "PhaseDiagram.ipynb" to show the phase boundaries.
Decision functions regarding different phases are also learned and plotted in the "PhaseDiagram.ipynb".
