# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-applications/qaoa.ipynb
# 021626 Yikai Mao

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np
import networkx as nx

def qaoa(n, options=[]):
    # options = [graph, parameters]
    # graph = if 'cycle', use the default cycle graph. Else, supply custom networkx graph
    # parameters = if 'random', use random gamma/beta. Else, supply gamma and beta
    
    graph = options[0]
    parameters = options[1]
    
    if graph == 'cycle':
        graph = nx.cycle_graph(n)
        # print(list(cycle_graph.edges()))
        # nx.draw(cycle_graph)
    else:
        graph = options[0]
        
    gamma = Parameter("$\\gamma$")
    beta = Parameter("$\\beta$")
    if parameters == 'random':
        gamma = np.random.uniform(low=-np.pi, high=np.pi)
        beta = np.random.uniform(low=-np.pi, high=np.pi)
    else:
        gamma = parameters[0]
        beta = parameters[1]
    
    qaoa_circuit = QuantumCircuit(n)
    
    for qubit in range(n):
        qaoa_circuit.h(qubit)
    
    qaoa_circuit.barrier()
    
    # gamma = pi/8.000 # maxcut n=4
    for pair in list(graph.edges()):  # pairs of nodes
        qaoa_circuit.rzz(2 * gamma, pair[0], pair[1])
        qaoa_circuit.barrier()
    
    # beta = pi/2.666 # maxcut n=4
    for qubit in range(n):
        qaoa_circuit.rx(2 * beta, qubit)
    
    qaoa_circuit.measure_all()
    
    return qaoa_circuit