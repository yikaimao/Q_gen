# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-walk-search-algorithm.ipynb
# 021426 Yikai Mao

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import Diagonal, QFT
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

def grover_coin(n):
    # n = number of qubits
    # ...the coin is a Grover coin, 
    # which is the diffuser in Grover's algorithm
    
    coin=QuantumCircuit(n)
    coin.h(range(n))
    
    diagonal_elements = [1] + [-1]*((2**n) - 1)
    # daigonal_gate = decomposer(Diagonal(diagonal_elements),4).to_gate()
    daigonal_gate = Diagonal(diagonal_elements).to_gate(label="diagonal")
    # print(diagonal_elements) # diagonal matrix elements
    coin.append(daigonal_gate, list(range(n)))
    
    coin.h(range(n))
    coin = coin.to_gate(label="grover_coin")
    
    return coin

def shift_operator(n):
    # n = number of qubits of the coin
    
    shift_operator = QuantumCircuit(n+2**n)
    
    for i in range(0,2**n):
        if i==0:
            shift_operator.x(list(range(2**n,n+2**n)))
        else:
            f_str = '0'+str(n)+'b'
            i_bin = f'{i:{f_str}}'[::-1] # reversed for qiksit endian
            i_old_bin = f'{(i-1):{f_str}}'[::-1] # reversed for qiksit endian
            diff = [j+2**n for j in range(len(i_bin)) if i_bin[j] != i_old_bin[j]]
            # print(diff)
            shift_operator.x(diff)
        shift_operator.mcx(list(range(2**n,n+2**n)), i)
        
    shift_operator = shift_operator.to_gate(label="shift_operator")
    
    return shift_operator

def mark_auxiliary(n):
    # n = number of qubits of the coin
    # Mark auxiliary if the other qubits are non-zero
    
    mark_auxiliary_circuit = QuantumCircuit(2**n+1)
    mark_auxiliary_circuit.x(list(range(2**n+1)))
    mark_auxiliary_circuit.mcx(list(range(2**n)), 2**n)
    mark_auxiliary_circuit.z(2**n)
    mark_auxiliary_circuit.mcx(list(range(2**n)), 2**n)
    mark_auxiliary_circuit.x(list(range(2**n+1)))
    mark_auxiliary_gate = mark_auxiliary_circuit.to_gate(label="mark_aux")
    
    return mark_auxiliary_gate

def quantum_walk_one_step(n):
    # n = number of qubits of the coin
    
    one_step_circuit = QuantumCircuit(n+2**n)
    one_step_circuit.append(grover_coin(n), list(range(2**n,n+2**n)))
    one_step_circuit.append(shift_operator(n), list(range(n+2**n)))

    return one_step_circuit

def quantum_walk_phase_estimation(n, one_step_circuit):
    # n = number of qubits of the coin
    # one step of quantum walk
    
    # construct one step gates
    inv_cont_one_step = one_step_circuit.inverse().control()
    inv_cont_one_step_gate = inv_cont_one_step.to_instruction(label="inv_one_step")
    
    cont_one_step = one_step_circuit.control()
    cont_one_step_gate = cont_one_step.to_instruction(label="one_step")
    
    # phase estimation
    phase_estimation_circuit = QuantumCircuit(2**n+2**n+n+1)
    
    phase_estimation_circuit.h(list(range(2**n)))
    
    for i in range(0,2**n):
        stop = 2**i
        index = [i]
        for k in range(2**n+n):
            index.append(2**n+k)
        for j in range(0,stop):
            phase_estimation_circuit.append(cont_one_step_gate, index)

    # Inverse fourier transform
    inv_qft_gate = QFT(2**n, inverse=True).to_gate(label="inv_QFT")
    phase_estimation_circuit.append(inv_qft_gate, list(range(2**n)))

    # Mark all angles theta that are not 0 with an auxiliary qubit
    index = list(range(2**n))
    index.append(2**n+2**n+2+1-1)
    phase_estimation_circuit.append(mark_auxiliary(n), index)

    # Reverse phase estimation
    qft_gate = QFT(2**n, inverse=False).to_gate(label="QFT")
    phase_estimation_circuit.append(qft_gate, list(range(2**n)))

    for i in range(2**n-1,-1,-1):
        stop = 2**i
        index = [i]
        for k in range(2**n+n):
            index.append(2**n+k)
        for j in range(0,stop):
            phase_estimation_circuit.append(inv_cont_one_step_gate, index)
    
    # phase_estimation_circuit.barrier()
    phase_estimation_circuit.h(list(range(2**n)))

    # Make phase estimation gate
    phase_estimation_gate = phase_estimation_circuit.to_instruction(label="phase estimation")
    
    return phase_estimation_gate

def quantum_walk(n, options=[]):
    # n = number of qubits of the coin, must >= 2
    # options = [print_solutions]
    # print_solutions = 'print', 'silent'

    print_solutions = options[0]
    
    # full quantum walk search
    theta_q = QuantumRegister(2**n, 'theta')
    node_q = QuantumRegister(2**n, 'node')
    coin_q = QuantumRegister(n, 'coin')
    auxiliary_q = QuantumRegister(1, 'auxiliary')
    creg_c2 = ClassicalRegister(2**n, 'c')
    quantum_walk_circuit = QuantumCircuit(theta_q, node_q, coin_q, auxiliary_q, creg_c2)
    
    # Apply Hadamard gates to the qubits that represent the nodes and the coin
    quantum_walk_circuit.h(list(range(2**n,2**n+2**n+n)))
    # 1/sqrt(sqrt(M/N))
    iterations = 1/np.sqrt((2**(n-2))/(2**n))
    
    phase_estimation_gate = quantum_walk_phase_estimation(n, quantum_walk_one_step(n))
    
    quantum_walk_oracle =  QuantumCircuit(2**n)
    
    # num_sol = 2**(n-2) for simple iteration calculation
    # may still need more iterations for accurate estimation
    sol = []
    for i in range(2**(n-2)): 
        temp = random_bin_str(2**n, False)
        while temp in sol:
            temp = random_bin_str(n, False)
        sol.append(temp)
        
    if print_solutions == 'print':
        print("solutions:", sol)
    
    # use X gate to mark the solution
    for b_str in sol:
        
        # if 0, apply X gate
        for qubit in range(len(b_str)):
            if b_str[qubit] == '0':
                quantum_walk_oracle.x(2**n-qubit-1)
        
        # prepare MCX gate
        quantum_walk_oracle.h(2**n-1)
        quantum_walk_oracle.mcx(list(range(2**n-1)), 2**n-1)
        quantum_walk_oracle.h(2**n-1)
        
        # if 0, apply X gate
        for qubit in range(len(b_str)):
            if b_str[qubit] == '0':
                quantum_walk_oracle.x(2**n-qubit-1)
    
    quantum_walk_oracle = quantum_walk_oracle.to_gate(label="oracle")
    
    for i in range(0,int(iterations)):
        quantum_walk_circuit.append(quantum_walk_oracle, list(range(2**n,2**n+2**n)))
        quantum_walk_circuit.append(phase_estimation_gate, list(range(2**n+2**n+n+1)))
    
    for i in range(node_q.size):
        quantum_walk_circuit.measure(node_q[i], creg_c2[i])
    
    return quantum_walk_circuit