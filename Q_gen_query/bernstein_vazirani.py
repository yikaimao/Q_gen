# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/bernstein-vazirani.ipynb
# 122325 Yikai Mao

from qiskit import QuantumCircuit
import numpy as np

def random_bin_str(width, zero=False):
    # return random binary string based on width
    # zero = T/F, T = include 0, F = do not return 0
    # width cannot be 0
    
    if width == 0:
        return None
    
    b = np.random.randint(2, size=width)
    b_str = ''.join(map(str, b.tolist()))
    
    if zero==True:
        return b_str
    
    else:
        while '1' not in b_str:
            b = np.random.randint(2, size=width)
            b_str = ''.join(map(str, b.tolist()))
        
        return b_str
        
def bernstein_vazirani(n, options=[]):
    # n = number of qubits of the oracle
    # options = [oracle, print_oracle]
    # oracle = 'random'
    # print_oracle = 'print', 'silent'
    
    oracle = options[0]
    print_oracle = options[1]
    
    # We need a circuit with n qubits, plus one auxiliary qubit
    # Also need n classical bits to write the output to
    bv_circuit = QuantumCircuit(n+1, n)
    
    # put auxiliary in state |->
    bv_circuit.h(n)
    bv_circuit.z(n)
    
    # Apply Hadamard gates before querying the oracle
    for i in range(n):
        bv_circuit.h(i)
        
    # Apply barrier 
    bv_circuit.barrier()
    
    bernstein_vazirani_oracle = QuantumCircuit(n+1)
    
    # if oracle == ???:
    #     # define new oracle here
    
    s_str = random_bin_str(n, False)
    
    if print_oracle == 'print':
        # reverse s to fit qiskit's qubit ordering
        print("oracle =", s_str[::-1])
    
    for q in range(n):
        if s_str[q] == '0':
            bernstein_vazirani_oracle.id(q)
        else:
            bernstein_vazirani_oracle.cx(q, n)
    
    bernstein_vazirani_oracle = bernstein_vazirani_oracle.to_gate()
    bernstein_vazirani_oracle.name = "bv_oracle"
    
    bv_circuit.append(bernstein_vazirani_oracle, range(n+1))
            
    # Apply barrier 
    bv_circuit.barrier()
    
    #Apply Hadamard gates after querying the oracle
    for i in range(n):
        bv_circuit.h(i)
    
    # Measurement
    for i in range(n):
        bv_circuit.measure(i, i)
    
    return bv_circuit