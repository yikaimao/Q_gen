# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-counting.ipynb
# 012226 Yikai Mao

from qiskit import QuantumCircuit
from qiskit.circuit.library import Diagonal, GroverOperator, QFT
import numpy as np

def quantum_counting(n, options=[]):
    # Grover iteration circuit for oracle with M/N solutions
    # n = number of counting qubits, circuit has n+t qubits and t classical bits
    # options = [print_oracle]
    # print_oracle = 'print', 'silent'
    
    # this locks num_searching equal to num_counting
    # notice num_searching does not need to be equal (see commented code below)
    # it can affect the accuracy of the algorithm
    num_counting = n # t
    num_searching = n # n
    
    # here n = the full qubit amaount of the generated circuit
    # num_counting = int(np.ceil(n/2)) # t
    # num_searching = n-num_counting # n
    
    print_solutions = options[0]
    
    quantum_counting_circuit = QuantumCircuit(num_counting+num_searching, num_counting)
    
    # Initialize all qubits to |+>
    for qubit in range(num_counting+num_searching):
        quantum_counting_circuit.h(qubit)
    
    quantum_counting_oracle = QuantumCircuit(num_counting+num_searching, name='oracle')
    
    nsolutions = np.random.randint(1, 2**num_searching)
    diagonal_elements = [-1]*nsolutions + [1]*((2**num_searching) - nsolutions)
    np.random.shuffle(diagonal_elements)
    oracle_gate = Diagonal(diagonal_elements)
    
    if print_solutions:
        print("counting qubits =", num_counting)
        print("searching qubits =", num_searching)
        print("num_solutions =", nsolutions)
        print(diagonal_elements) # diagonal matrix elements
    
    # Begin controlled Grover iterations
    n_iterations = 1
    for qubit in range(num_counting):
        
        grover_it = GroverOperator(oracle_gate).repeat(n_iterations).to_gate()
        grover_it.label = f"Grover$^{n_iterations}$"
        
        cgrit = grover_it.control()
        quantum_counting_oracle.append(cgrit, 
                                       [qubit] + list(range(num_counting, num_searching+num_counting)))
        
        n_iterations *= 2
    
    # controlled Grover iterations oracle
    quantum_counting_circuit.append(quantum_counting_oracle, range(num_counting+num_searching))    
    
    # Do inverse QFT on counting qubits
    qft_dagger = QFT(num_counting, inverse=True).to_gate()
    qft_dagger.label = "QFT†"
    quantum_counting_circuit.append(qft_dagger, range(num_counting))
    
    # Measure counting qubits
    quantum_counting_circuit.measure(range(num_counting), range(num_counting))
    
    return quantum_counting_circuit

def calculate_M(raw_counts, n):
    # For Processing Output of Quantum Counting
    
    # this locks num_searching equal to num_counting
    # notice num_searching does not need to be equal (see commented code below)
    # it can affect the accuracy of the algorithm
    num_counting = n # t
    num_searching = n # n
    
    # if n = the full qubit amount of the generated circuit:
    # num_counting = int(np.ceil(n/2)) # t
    # num_searching = n-num_counting # n
    
    measured_int = int(max(raw_counts, key=raw_counts.get), 2)
    print("Register Output = %i" % measured_int)
    
    # Calculate Theta
    theta = (measured_int/(2**num_counting))*np.pi*2
    print("Theta = %.5f" % theta)
    
    # Calculate No. of Solutions
    N = 2**num_searching
    M = N * (np.sin(theta/2)**2)
    print(f"No. of Solutions = {M:.1f}")
    
    # Calculate Upper Error Bound
    m = num_counting - 1 #Will be less than this (out of scope) 
    err = (np.sqrt(2*M*N) + N/(2**(m+1)))*(2**(-m))
    print("Error < %.2f" % err)