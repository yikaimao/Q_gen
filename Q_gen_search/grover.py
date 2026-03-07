# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/grover.ipynb
# 012226 Yikai Mao

from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal
import numpy as np

class _oracle:
    # grover oracle class
    def __init__(self, gate, sol):
        self.gate = gate
        self.sol = sol
        
    @property
    def iterations(self):
        return int(np.floor((np.pi/4)*np.sqrt((2**self.gate.num_qubits)/len(self.sol))))

def grover_diffuser(n):
    
    qc = QuantumCircuit(n)
    
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(n):
        qc.h(qubit)
        
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(n):
        qc.x(qubit)
        
    # Do multi-controlled-Z gate
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)  # multi-controlled-toffoli
    qc.h(n-1)
    
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(n):
        qc.x(qubit)
        
    # Apply transformation |00..0> -> |s>
    for qubit in range(n):
        qc.h(qubit)
        
    # We will return the diffuser as a gate
    diffuser = qc.to_gate()
    diffuser.name = "Diffuser"
    return diffuser

def grover(n, options=[]):
    # n = number of qubits of the grover oracle, n must >= 2
    # options = [num_solutions, print_solutions]
    # num_solutions = 'optimal', 'random', or int number of solutions, if n = 2 then this is forced to be 1
    # print_solutions = 'print', 'silent', show solutions and optimal iteration
    # optimal iteration will always be 1 if num_solutions = 2**(n-2))

    nsolutions = options[0]
    print_solutions = options[1]
    
    grover_circuit = QuantumCircuit(n)
    
    # init
    grover_circuit.h(list(range(n)))
    grover_circuit.barrier(list(range(n)))
    
    # core
    core = QuantumCircuit(n, name="grover_iteration")
    
    if n < 3:
        nsolutions = 1
    elif nsolutions == 'optimal':
        nsolutions = 2**(n-2)
    elif nsolutions == 'random':
        nsolutions = np.random.randint(1, np.ceil((2**n)/4)) # iteration will be >=1
    else:
        pass
    
    diagonal_elements = [-1]*nsolutions + [1]*((2**n) - nsolutions)
    np.random.shuffle(diagonal_elements)
    #print(diagonal_elements) # diagonal matrix elements
    oracle_gate = Diagonal(diagonal_elements)
    
    sol = []
    for idx, e in enumerate(diagonal_elements):
        if e < 1:
            state = "%s" % format(idx, "0%ib" % n)
            sol.append(state)
    
    oracle_gate.name = "Grover\nOracle"
    
    grover_oracle = _oracle(oracle_gate, sol)
    
    if print_solutions == 'print':
        print("solutions:", grover_oracle.sol)
        print("total:", len(grover_oracle.sol))
        print("optimal iteration:", grover_oracle.iterations)

    core.append(grover_oracle.gate, list(range(n)))
    core.append(grover_diffuser(n), list(range(n)))
    
    for i in range(grover_oracle.iterations):
        grover_circuit.append(core, list(range(n)))
    
    # measure
    grover_circuit.measure_all()
    
    return grover_circuit