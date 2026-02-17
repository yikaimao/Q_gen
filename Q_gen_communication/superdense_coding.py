# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/superdense-coding.ipynb
# 021426 Yikai Mao

from qiskit import QuantumCircuit
from random import sample, randint

def entangle(n):
    # entange multiple qubits
    # n must >= 2
    
    qc = QuantumCircuit(n)
    
    qc.h(0)
    for i in range(n-1):
        qc.cx(i, i+1)
    
    qc = qc.to_gate(label='entangle')
    
    return qc

def encode_message_superdense(n, size):
    
    qc = QuantumCircuit(n)
    if size == 'half':
        size = int(round(n/2))
    elif size == 'all':
        size = n
    else:
        size = size
    message_index = sample(range(n), size)
    # print(message_index)
    
    for i in message_index:
        message = randint(0, 3)
        # print(i,message)
        if message == 0:
            qc.id(i)
        if message == 1:
            qc.x(i)
        if message == 2:
            qc.z(i)
        if message == 3:
            qc.x(i)
            qc.z(i)
            
    qc = qc.to_gate(label='message')
            
    return qc

def disentangle(n):
    # disentange multiple qubits
    # n must >= 2
    
    qc = QuantumCircuit(n)
    
    for i in range(n-1):
        qc.cx(n-2-i, n-1-i)
    qc.h(0)
        
    qc = qc.to_gate(label='disentangle')
        
    return qc

def superdense_coding(n, options=[]):
    # options = [size]
    # size = 'all': encode all qubits. 'half': encode half qubits. or just provide a number, must <= n
    
    size = options[0]
    
    superdense_coding_circuit = QuantumCircuit(n)

    # entanglement
    superdense_coding_circuit.append(entangle(n),list(range(n)))
    
    superdense_coding_circuit.barrier()
    
    # encode qubits
    superdense_coding_circuit.append(encode_message_superdense(n, size),list(range(n)))
    
    superdense_coding_circuit.barrier()
    
    # disentanglement
    superdense_coding_circuit.append(disentangle(n),list(range(n)))
    
    superdense_coding_circuit.measure_all()

    return superdense_coding_circuit