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