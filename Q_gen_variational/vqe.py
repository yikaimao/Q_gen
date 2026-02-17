# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-applications/vqe-molecules.ipynb
# https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.library.EfficientSU2
# https://www.youtube.com/watch?v=XF0eMYKd9ks
# 021626 Yikai Mao

from qiskit import QuantumCircuit
from qiskit.circuit.library import efficient_su2
import numpy as np

def vqe(n, options=[]):
    # options = [repeat, gates, entanglement]
    # repeat = how many times to repeat the variational form
    # gates = single qubit gates used in the variational form (['ry', 'rz'])
    # entanglement = CX between the single qubit gates (full, linear, reverse_linear, circular, sca)
    # parameters = a bind_dict for assigning the parameters to the gates, or 'random'
    
    repeat = options[0]
    gates = options[1]
    entanglement = options[2]
    parameters = options[3]
    
    vqe_circuit = efficient_su2(
        num_qubits=n, 
        reps=repeat, 
        su2_gates=gates, 
        entanglement=entanglement, 
        parameter_prefix='th', 
        insert_barriers=True)
    
    if parameters == 'random':
        vqe_circuit.assign_parameters(
            {p:np.random.uniform(low=-np.pi, high=np.pi) for p in vqe_circuit.parameters}, 
            inplace=True)
    else:
        bind_dict = parameters
        # for key in vqe_circuit.parameters:
            # bind_dict[key] = 
        vqe_circuit.assign_parameters(bind_dict, inplace=True)
    
    vqe_circuit.measure_all()
    
    return vqe_circuit