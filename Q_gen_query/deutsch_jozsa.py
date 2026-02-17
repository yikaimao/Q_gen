# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/deutsch-jozsa.ipynb
# 122225 Yikai Mao

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

def deutsch_jozsa(n, options=[]):
    # n = number of qubits of the oracle
    # options = [oracle, print_oracle]
    # oracle = 'constant' (easy), 'balanced' (hard)
    # print_oracle = 'print', 'silent'
    
    oracle = options[0]
    print_oracle = options[1]
    
    dj_circuit = QuantumCircuit(n+1, n)
    
    # output qubit:
    dj_circuit.x(n)
    dj_circuit.h(n)
    
    # input register:
    for qubit in range(n):
        dj_circuit.h(qubit)
        
    # append oracle:
    dj_circuit.barrier(list(range(n+1)))
    
    deutsch_jozsa_oracle = QuantumCircuit(n+1)
    
    if oracle == 'constant':
        # First decide what the fixed output of the oracle will be
        # (either always 0 or always 1)
        output = np.random.randint(2)
        if output == 1:
            deutsch_jozsa_oracle.x(n)
    
    if oracle == 'balanced':
        # First generate a random number that tells us which CNOTs to
        # wrap in X-gates:
        b_str = random_bin_str(n, False)
        # Next, we place the first X-gates. Each digit in our binary string 
        # corresponds to a qubit, if the digit is 0, we do nothing, if it's 1
        # we apply an X-gate to that qubit:
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                deutsch_jozsa_oracle.x(qubit)
        # Do the controlled-NOT gates for each qubit, using the output qubit 
        # as the target:
        for qubit in range(n):
            deutsch_jozsa_oracle.cx(qubit, n)
        # Next, place the final X-gates
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                deutsch_jozsa_oracle.x(qubit)
                
    # else:
    # define new oracle here
    
    if print_oracle == 'print':
        if oracle == 'constant':
            print("constant " + str(output) + " oracle")
        if oracle == 'balanced':
            # reverse s to fit qiskit's qubit ordering
            print("balanced oracle =", b_str[::-1])
        print(deutsch_jozsa_oracle)
    
    deutsch_jozsa_oracle = deutsch_jozsa_oracle.to_gate()
    deutsch_jozsa_oracle.name = "dj_oracle"
    
    dj_circuit.append(deutsch_jozsa_oracle, range(n+1))
    dj_circuit.barrier(list(range(n+1)))
    
    # H-gates again and measure:
    for qubit in range(n):
        dj_circuit.h(qubit)
    
    for i in range(n):
        dj_circuit.measure(i, i)
    
    return dj_circuit