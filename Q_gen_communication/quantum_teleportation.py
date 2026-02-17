# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/teleportation.ipynb
# 021526 Yikai Mao

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, random_statevector
from qiskit.circuit.library import Initialize

def quantum_teleportation(n, options=[]):
    # options = [state]
    # state = specify the state to teleport (state=Statevector([0, 1])), or 'random'
        
    state = options[0]
        
    quantum_teleportation_circuit = QuantumCircuit(3*n,1*n)

    for i in range(n):
        
        offset = 3*i
        if state == 'random':
            s = random_statevector(2)
            # display(s.draw(output='text'))
            # print('Q'+str(i)+' prob =', s.probabilities())
            init_gate = QuantumCircuit(1).compose(Initialize(s), front = True, inplace = False).to_instruction(label='init')
        else:
            init_gate = QuantumCircuit(1).compose(Initialize(state), front = True, inplace = False).to_instruction(label='init')
        inverse_init = QuantumCircuit(1).compose(Initialize(s).gates_to_uncompute(), front = True, inplace = False).to_instruction(label='disentangle')
        
        # First, let's initialize Alice's q0
        quantum_teleportation_circuit.append(init_gate, [0+offset])
        quantum_teleportation_circuit.barrier(0+offset,1+offset,2+offset)
        
        # Now begins the teleportation protocol
        quantum_teleportation_circuit.h(1+offset)
        quantum_teleportation_circuit.cx(1+offset,2+offset)
        quantum_teleportation_circuit.barrier(0+offset,1+offset,2+offset)
        
        # Send q1 to Alice and q2 to Bob
        quantum_teleportation_circuit.cx(0+offset,1+offset)
        quantum_teleportation_circuit.h(0+offset)
        quantum_teleportation_circuit.barrier(0+offset,1+offset,2+offset)
        
        # Alice sends classical bits to Bob
        quantum_teleportation_circuit.cx(1+offset,2+offset)
        quantum_teleportation_circuit.cz(0+offset,2+offset)
        
        # We undo the initialization process
        quantum_teleportation_circuit.append(inverse_init, [2+offset])
        
        # See the results, we only care about the state of qubit 2
        quantum_teleportation_circuit.measure(2+offset,i)
    
    return quantum_teleportation_circuit