# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-fourier-transform.ipynb
# 011426 Yikai Mao

from qiskit import QuantumCircuit
import numpy as np

def qft_rotations(circuit, n):
    
    if n == 0:
        return circuit
    n -= 1
    
    circuit.h(n)
    
    for qubit in range(n):
        circuit.cp(np.pi/2**(n-qubit), qubit, n)
        
    qft_rotations(circuit, n)

def swap_registers(circuit, n):
    
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
        
    return circuit

def initilize_in_fourier_basis(n, number):
    # NOTE: NO OUT OF BOUND CHECK!
    
    circuit = QuantumCircuit(n)
    
    if len(f"{number:b}") > n:
        print("number too big! not enough qubits!")
    
    for qubit in range(n):
        circuit.h(qubit)
        circuit.p(number*np.pi/(2**(n-qubit-1)), qubit)
        
    return circuit

def qft(n, options=[]):
    # n = number of qubits
    # options = [initialize, inverse, measurement]
    # initialize = decimal number to be initialized in fourier basis, 0 = random, -1 = no initialization
    # inverse = 'normal', 'inverse', output inverse QFT
    # measurement = 'measure', 'no_measure', add measurement

    initialize = options[0]
    inverse = options[1]
    measurement = options[2]
        
    qft_circuit = QuantumCircuit(n)
    
    qft_rotations(qft_circuit, n)
    swap_registers(qft_circuit, n)
    
    if inverse:
        qft_circuit = qft_circuit.inverse()
        
    if measurement:
        qft_circuit.measure_all()
        
    if initialize > 0:
        initialize_number = initialize
        initialize_circuit = initilize_in_fourier_basis(n, initialize_number)
        qft_circuit = initialize_circuit & qft_circuit
    elif initialize == 0:
        initialize_number = np.random.randint(2**n)
        initialize_circuit = initilize_in_fourier_basis(n, initialize_number)
        qft_circuit = initialize_circuit & qft_circuit
    # else:
        # do nothing
    
    return qft_circuit