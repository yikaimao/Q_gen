# https://quantumai.google/cirq/experiments/quantum_walks
# 021926 Yikai Mao

from qiskit import QuantumCircuit
import numpy as np
        
def quantum_walk_simple(n, options=[]):
    # n = number of nodes in the waling graph
    # a simple version of the quantum walk algorithm that uses less quantum resources
    # assume coin qubit is always the most significant qubit
    # options = [starting_qubit, initialization, steps]
    # starting_qubit = index of the starting qubit, or 'random'
    # initialization = gate sequence to initialize the coin qubit, 'x', 'h', 's', or None
    # steps = number of walker steps

    if options[0] == 'random':
        starting_qubit = np.random.randint(n)
    else:
        starting_qubit = options[0]
    initialization = options[1]
    steps = options[2]
    
    quantum_walk_simple_circuit = QuantumCircuit(n+1, n)
    quantum_walk_simple_circuit.x(starting_qubit)

    # assume coin qubit is always the most significant qubit
    for gate in initialization:
        if gate == None:
            continue
        elif gate == 'x':
            quantum_walk_simple_circuit.x(n)
        elif gate == 'h':
            quantum_walk_simple_circuit.h(n)
        elif gate == 's':
            quantum_walk_simple_circuit.s(n)
        else:
            print('input init gate not yet implemented')
            return
    
    quantum_walk_simple_circuit.barrier()

    for step in range(steps):
        quantum_walk_simple_circuit.h(n)

        quantum_walk_simple_circuit.x(n)
        for i in range(n, 0, -1):
            quantum_walk_simple_circuit.mcx(list(range(n, i-1, -1)), i-1)
            if i > 1:
                quantum_walk_simple_circuit.x(i-1)
        quantum_walk_simple_circuit.x(n)
        quantum_walk_simple_circuit.barrier()        

        for i in range(1, n+1):
            quantum_walk_simple_circuit.mcx(list(range(n, i-1, -1)), i-1)
            if i < n:
                quantum_walk_simple_circuit.x(i)
        quantum_walk_simple_circuit.barrier()

    for i in range(n):
        # remember qiskit is little endian
        quantum_walk_simple_circuit.measure(i, i)
        # this will reverse the output to big-endian
        # quantum_walk_simple_circuit.measure(i, n-i-1)
    
    return quantum_walk_simple_circuit