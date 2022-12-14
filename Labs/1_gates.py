"""
## Classical logic gates with quantum circuits

### Source
https://learn.qiskit.org/course/ch-labs/lab-1-quantum-circuits

### Problem statement
Part1: Create quantum circuit functions that can compute the XOR, AND, NAND and OR gates using the NOT gate (expressed as x in Qiskit), the CNOT gate (expressed as cx in Qiskit) and the Toffoli gate (expressed as ccx in Qiskit).
Part2: Execute AND gate on a real quantum system and learn how the noise properties affect the result.

### References
QuantumCircuit: https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html
compose: https://medium.com/arnaldo-gunzi-quantum/how-to-use-the-compose-function-in-qiskit-5983bf4fffcf
AER Simulator: https://qiskit.org/documentation/tutorials/simulators/1_aer_provider.html
barrier: https://quantumcomputing.stackexchange.com/questions/8369/what-is-a-barrier-in-qiskit-circuits
"""

from qiskit import *
from qiskit.tools.monitor import job_monitor

def initCircuit(nq, inp):
    # print("Initialising circuit with ",nq," qubit(s) ",inp)
    
    # Initialise circuit
    qc = QuantumCircuit(nq, 1) # A quantum circuit with a single qubit and a single classical bit
    qc.reset(range(nq))
    
    # Encoding the input
    # We encode '0' as the qubit state |0⟩, and '1' as |1⟩
    # Since the qubit is initially |0⟩, we don't need to do anything for an input of '0'
    # For an input of '1', we do an x to rotate the |0⟩ to |1⟩
    for i in range(len(inp)):
        if inp[i]=='1':
            qc.x(i)
        
    return qc

def measureCircuitOnce(measureQ, qc):
    # Finally, we extract the |0⟩/|1⟩ output of the qubit and encode it in the bit c[0]
    qc.measure(measureQ,0)
    # We'll run the program on a simulator
    backend = Aer.get_backend('aer_simulator')
    # Since the output will be deterministic, we can use just a single shot to get it
    job = backend.run(qc, shots=1, memory=True)
    output = job.result().get_memory()[0]
    
    return qc, output

def AND(inp1,inp2):
    """An AND gate.
    
    Parameters:
        inpt1 (str): Input 1, encoded in qubit 0.
        inpt2 (str): Input 2, encoded in qubit 1.
        
    Returns:
        QuantumCircuit: Output XOR circuit.
        str: Output value measured from qubit 2.
    """
    
    qc = initCircuit(3,[inp1,inp2])
    # barrier between input state and gate operation 
    qc.barrier()
    
    # AND using CNOT
    qc.ccx(0, 1, 2)
    
    #barrier between gate operation and measurement
    qc.barrier()
    
    # Finally, we extract the |0⟩/|1⟩ output of the qubit and encode it in the bit c[0]
    qc,output = measureCircuitOnce(2, qc)
    
    return qc, output

def OR(inp1,inp2):
    """An OR gate.
    
    Parameters:
        inpt1 (str): Input 1, encoded in qubit 0.
        inpt2 (str): Input 2, encoded in qubit 1.
        
    Returns:
        QuantumCircuit: Output OR circuit.
        str: Output value measured from qubit 2.
    """
    
    qc = initCircuit(3,[inp1,inp2])
    # barrier between input state and gate operation 
    qc.barrier()
    
    # OR using CNOT
    qc.cx(0, 2)
    qc.cx(1, 2)
    
    #barrier between gate operation and measurement
    qc.barrier()
    
    # Finally, we extract the |0⟩/|1⟩ output of the qubit and encode it in the bit c[0]
    qc,output = measureCircuitOnce(2, qc)
    
    return qc, output

def NAND(inp1,inp2):
    """An NAND gate.
    
    Parameters:
        inpt1 (str): Input 1, encoded in qubit 0.
        inpt2 (str): Input 2, encoded in qubit 1.
        
    Returns:
        QuantumCircuit: Output XOR circuit.
        str: Output value measured from qubit 2.
    """
    
    qc = initCircuit(3,[inp1,inp2])
    # barrier between input state and gate operation 
    qc.barrier()
    
    # NAND using CNOT
    qc.ccx(0, 1, 2)
    qc.x(2)
    
    #barrier between gate operation and measurement
    qc.barrier()
    
    # Finally, we extract the |0⟩/|1⟩ output of the qubit and encode it in the bit c[0]
    qc,output = measureCircuitOnce(2, qc)
    
    return qc, output

def XOR(inp1,inp2):
    """An XOR gate.
    
    Parameters:
        inpt1 (str): Input 1, encoded in qubit 0.
        inpt2 (str): Input 2, encoded in qubit 1.
        
    Returns:
        QuantumCircuit: Output XOR circuit.
        str: Output value measured from qubit 1.
    """
    
    qc = initCircuit(2,[inp1,inp2])
    # barrier between input state and gate operation 
    qc.barrier()
    
    # XOR using CNOT
    qc.cx(0, 1)
    
    #barrier between gate operation and measurement
    qc.barrier()
    
    # Finally, we extract the |0⟩/|1⟩ output of the qubit and encode it in the bit c[0]
    qc,output = measureCircuitOnce(1, qc)
    
    return qc, output

def NOT(inp):
    """An NOT gate.
    
    Parameters: 
        inp (str): Input, encoded in qubit 0.
        
    Returns:
        QuantumCircuit: Output NOT circuit.
        str: Output value measured from qubit 0.
    """
    
    qc = initCircuit(1,[inp])
    # barrier between input state and gate operation 
    qc.barrier()
    
    # Now we've encoded the input, we can do a NOT on it using x
    qc.x(0)
    
    #barrier between gate operation and measurement
    qc.barrier()
    
    # Finally, we extract the |0⟩/|1⟩ output of the qubit and encode it in the bit c[0]
    qc,output = measureCircuitOnce(0, qc)
    
    return qc, output

def realAND(inp1, inp2, backend, layout):
    qc = QuantumCircuit(3, 1) 
    qc.reset(range(3))
    
    if inp1=='1':
        qc.x(0)
    if inp2=='1':
        qc.x(1)
        
    qc.barrier()
    qc.ccx(0, 1, 2) 
    qc.barrier()
    qc.measure(2, 0) 
  
    qc_trans = transpile(qc, backend, initial_layout=layout, optimization_level=3)
    job = backend.run(qc_trans, shots=8192)
    print(job.job_id())
    job_monitor(job)
    
    output = job.result().get_counts()
    
    return qc_trans, output

# Tests
for inp in ['0', '1']:
    qc, out = NOT(inp)
    print('NOT with input',inp,'gives output',out)
    
for inp1 in ['0', '1']:
    for inp2 in ['0', '1']:
        qc, out = XOR(inp1, inp2)
        print('XOR with input ',inp1,' and ',inp2,' gives output ',out)
        
for inp1 in ['0', '1']:
    for inp2 in ['0', '1']:
        qc, out = OR(inp1, inp2)
        print('OR with input ',inp1,' and ',inp2,' gives output ',out)
        # print(qc)
        
for inp1 in ['0', '1']:
    for inp2 in ['0', '1']:
        qc, out = AND(inp1, inp2)
        print('AND with input ',inp1,' and ',inp2,' gives output ',out)
        # print(qc)
        
for inp1 in ['0', '1']:
    for inp2 in ['0', '1']:
        qc, out = NAND(inp1, inp2)
        print('NAND with input ',inp1,' and ',inp2,' gives output ',out)
        # print(qc)
        
provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_qasm_simulator')

layout= [0,1,2]
output_all = []
qc_trans_all = []
prob_all = []

worst = 1
best = 0
for input1 in ['0','1']:
    for input2 in ['0','1']:
        qc_trans, output = realAND(input1, input2, backend, layout)
        
        output_all.append(output)
        qc_trans_all.append(qc_trans)
        
        prob = output[str(int( input1=='1' and input2=='1' ))]/8192
        prob_all.append(prob)
        
        print('\nProbability of correct answer for inputs',input1,input2)
        print('{:.2f}'.format(prob) )
        print('---------------------------------')
        
        worst = min(worst,prob)
        best = max(best, prob)
        
print('')
print('\nThe highest of these probabilities was {:.2f}'.format(best))
print('The lowest of these probabilities was {:.2f}'.format(worst))