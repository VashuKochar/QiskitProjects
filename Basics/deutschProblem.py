"""
### Source
https://learn.qiskit.org/course/ch-gates/phase-kickback

### Problem statement
Make a function, deutsch() that takes a Deutsch function as a QuantumCircuit and uses the Deutsch algorithm to solve it on a quantum simulator. Your function should return True if the Deutsch funciton is balanced, and False if it's constant.

You can use the function deutsch_problem() to create a QuantumCircuit you can use as input to your deutsch() function.

### References
QuantumCircuit: https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html
compose: https://medium.com/arnaldo-gunzi-quantum/how-to-use-the-compose-function-in-qiskit-5983bf4fffcf
AER Simulator: https://qiskit.org/documentation/tutorials/simulators/1_aer_provider.html
"""

import numpy as np

# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, transpile, Aer

def deutsch_problem(seed=None):
    """Returns a circuit that carries out the function
    from Deutsch's problem.
    Args:
        seed (int): If set, then returned circuit will
            always be the same for the same seed.
    Returns: QuantumCircuit
    """
    np.random.seed(seed)
    problem = QuantumCircuit(2)
    if np.random.randint(2):
        print("Function is balanced.")
        problem.cx(0, 1)
    else:
        print("Function is constant.")
    if np.random.randint(2):
        problem.x(1)
    return problem

def deutsch(function):
    """Implements Deutsch's algorithm.

    Args:
        function (QuantumCircuit): Deutsch function to solve.
            Must be a 2-qubit circuit, and either balanced,
            or constant.
    Returns:
        bool: True if the circuit is balanced, otherwise False.
    """

    # your code here
    solution_circuit = QuantumCircuit(2,1)

    solution_circuit.x(1)
    solution_circuit.h([0,1])

    final_circuit = solution_circuit.compose(function)
    final_circuit.h(0)
    final_circuit.measure(0,0)
    # final_circuit.draw()

    sim = Aer.get_backend('aer_simulator')
    circ_trans = transpile(final_circuit, sim)
    count = list(sim.run(circ_trans).result().get_counts().keys())
    
    if count[0] == '1':
        return True
    else:
        return False

prob = deutsch_problem()
check = deutsch(prob)

if check:
    print("Function is balanced.")
else:
    print("Function is constant.")