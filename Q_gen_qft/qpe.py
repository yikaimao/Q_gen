# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-phase-estimation.ipynb
# 011426 Yikai Mao

from qiskit import QuantumCircuit
from numpy import pi
from Q_gen_qft.qft import qft

def qpe(n, options=[]):
    # n = number of counting qubits
    # options = [phase_theta]
    # phase_theta = the decimal number to be initialized in fourier basis
    
    phase_theta = options[0]
    
    # n counting qubits
    # 1 eigenstate qubit
    qpe_circuit = QuantumCircuit(n+1, n)
    
    # Prepare the eigenstate |psi>:
    qpe_circuit.x(n)
    
    # Apply H-Gates to counting qubits:
    for qubit in range(n):
        qpe_circuit.h(qubit)
    
    # Do the controlled-U operations:
    phase_lambda = (2*pi)*(phase_theta) # divide the result by 2^n to get phase_theta
    repetitions = 1
    for counting_qubit in range(n):
        for i in range(repetitions):
            qpe_circuit.cp(phase_lambda, counting_qubit, n)
        repetitions *= 2
    
    # Do the inverse QFT:
    qpe_circuit = qpe_circuit & qft(n, [-1, 'inverse', 'measure'])
    
    return qpe_circuit