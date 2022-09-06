"""
### Source
https://learn.qiskit.org/course/machine-learning/data-encoding

### Problem statement
1) Basis Encoding
2) Amplitude Encoding
3) Angle Encoding
4) Arbitrary Encoding

"""

import numpy as np

# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, Aer, IBMQ, execute, assemble
from qiskit.circuit.library import EfficientSU2, ZZFeatureMap
from qiskit.providers.aer import QasmSimulator, StatevectorSimulator, UnitarySimulator
from qiskit.visualization import *
from ibm_quantum_widgets import *
import numpy as np
import math
from qiskit.visualization import plot_histogram, plot_bloch_multivector, array_to_latex
# Loading your IBM Quantum account(s)
provider = IBMQ.load_account()

# L : 1D List of values
def basis_encoding(L):
	# Get No of Qubits required to encode L
	N = math.ceil(math.log(max(L), 2))
	qc = QuantumCircuit(N)
	state = [0] * (2**N)
	for i in L:
		state[i] += (1 / math.sqrt(len(L)))
	print(state)
	qc.initialize(state, list(range(N)))
	print(qc.decompose().decompose().decompose().decompose().decompose())
	return qc

# L : 2D List of values
def amplitude_encoding(L):
    # Get No of Qubits required to encode L
	N = math.ceil(math.log(len(L)*len(L[0]), 2))
	qc = QuantumCircuit(N)
	# converting 2d list into 1d using list comprehension
	flat_L = [j for sub in L for j in sub]
	# Normalisation
	# print(flat_L)
	alpha = flat_L/ np.sqrt(np.sum([i**2 for i in flat_L]))
	print(alpha)
	qc.initialize(alpha, list(range(N)))
	print(qc.decompose().decompose().decompose().decompose().decompose())
	return qc

# L: One data point
def angle_encoding(L):
    # Get No of Qubits required to encode L
	N = len(L)
	qc = QuantumCircuit(N)	
	for i in range(N):
		qc.ry(2*L[i], i)
	print(qc)
	return qc

# L: One data point
def arbitrary_encoding_1(N, L):
    # Get No of Qubits required to encode L
	circuit = EfficientSU2(num_qubits=N, reps=1, insert_barriers=True)
	print(circuit.decompose())
	encode = circuit.bind_parameters(L)
	print(encode.decompose())
	return encode

def arbitrary_encoding_2(N, L):
    # Get No of Qubits required to encode L
	circuit = ZZFeatureMap(N, reps=1, insert_barriers=True)
	print(circuit.decompose())
	encode = circuit.bind_parameters(L)
	print(encode.decompose())
	return encode

# basis_encoding_dataset = [5, 7]
# qc = basis_encoding(basis_encoding_dataset)
# amplitude_encoding_dataset = [[1.5,0], [-2,3]]
# qc = amplitude_encoding(amplitude_encoding_dataset)
# angle_encoding_dataset = [0, math.pi/4, math.pi/2]
# qc = angle_encoding(angle_encoding_dataset)
# arbitrary_encoding_dataset_1 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
# qc = arbitrary_encoding_1(3, arbitrary_encoding_dataset_1)
# arbitrary_encoding_dataset_2 = [0.1, 0.2, 0.3]
# qc = arbitrary_encoding_2(3, arbitrary_encoding_dataset_2)