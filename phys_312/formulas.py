import numpy as np

def maxwell_boltzmann(v, m, T, k):
	normalization_factor = (m/(2*np.pi*k*T))**(3/2)
	exponential = np.exp(-0.5*m*(v**2)/(k*T))
	f = normalization_factor*(4*np.pi*(v**2))*exponential
	return f