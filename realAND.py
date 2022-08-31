"""
## Classical logic gates with quantum circuits

### Source
https://learn.qiskit.org/course/ch-labs/lab-1-quantum-circuits

### Problem statement
Execute AND gate on a real quantum system and learn how the noise properties affect the result.

### References
QuantumCircuit: https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html
compose: https://medium.com/arnaldo-gunzi-quantum/how-to-use-the-compose-function-in-qiskit-5983bf4fffcf
AER Simulator: https://qiskit.org/documentation/tutorials/simulators/1_aer_provider.html
barrier: https://quantumcomputing.stackexchange.com/questions/8369/what-is-a-barrier-in-qiskit-circuits
"""


from qiskit import *
from qiskit.visualization import plot_histogram,plot_error_map
import numpy as np
from qiskit.tools.monitor import job_monitor

def AND(inp1, inp2, backend, layout):
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
        qc_trans, output = AND(input1, input2, backend, layout)
        
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