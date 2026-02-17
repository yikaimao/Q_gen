# https://github.com/qiskit-community/qiskit-textbook/blob/main/qiskit-textbook-src/qiskit_textbook/tools/__init__.py
# 011426 Yikai Mao

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

def simon(n, options=[]):
    # n = number of qubits of the oracle
    # options = [oracle, print_oracle]
    # oracle = 'random'
    # print_oracle = 'print', 'silent'
    
    oracle = options[0]
    print_oracle = options[1]
    
    simon_circuit = QuantumCircuit(n*2, n)

    # Apply Hadamard gates before querying the oracle
    simon_circuit.h(range(n))    
    
    # Apply barrier for visual separation
    simon_circuit.barrier()

    # if oracle == ???:
    #     # user-defined oracle here
    
    simon_oracle = QuantumCircuit(n*2)
    
    b_str = random_bin_str(n, True)
    
    # Do copy; |x>|0> -> |x>|x>
    for q in range(n):
        simon_oracle.cx(q, q+n)
    
    # 1:1 mapping, so just exit
    if '1' not in b_str: 
        return simon_oracle
    
    # index of first non-zero bit in b
    i = b_str.find('1')
    
    # Do |x> -> |s.x> on condition that q_i is 1
    for q in range(n):
        if b_str[q] == '1':
            simon_oracle.cx(i, (q)+n)
    
    if print_oracle == 'print':
        # reverse s to fit qiskit's qubit ordering
        print("oracle =", b_str[::-1])
        print(simon_oracle)
    
    simon_oracle = simon_oracle.to_gate()
    simon_oracle.name = "simon_oracle"
    
    simon_circuit.append(simon_oracle, range(n*2))

    # Apply barrier for visual separation
    simon_circuit.barrier()

    # Apply Hadamard gates to the input register
    simon_circuit.h(range(n))

    # Measure qubits
    simon_circuit.measure(range(n), range(n))
    
    return simon_circuit

def simon_verify(b_str, counts):
    # verify the output of simon circuit
    # b_str = oracle binary string
    # counts = measurement counts
    
    verified = True
    
    for z in counts:
        # Calculate the dot product of the results
        accum = 0
        for i in range(len(b_str)):
            accum += int(b_str[i]) * int(z[i])
        bdotz = accum % 2
        
        print('{}.{} = {} (mod 2)'.format(b_str, z, bdotz))
        
        if bdotz != 0:
            verified = False
    
    if verified:
        print("Passed")
    else:
        print("Failed")
        
    return None