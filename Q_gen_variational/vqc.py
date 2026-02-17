# https://qiskit-community.github.io/qiskit-machine-learning/tutorials/index.html
# https://github.com/rodneyosodo/variational-quantum-classifier-on-heartattack
# https://medium.com/qiskit/building-a-quantum-variational-classifier-using-real-world-data-809c59eb17c2
# 021626 Yikai Mao

from qiskit import QuantumCircuit
from qiskit.circuit.library import zz_feature_map, real_amplitudes
import numpy as np

def vqc(n, options=[]):
    # options = [repeat_f, repeat_v, parameters]
    # repeat_f = how many times to repeat the feature map
    # repeat_v = how many times to repeat the variational form
    # parameters = a bind_dict for assigning the parameters to the gates, or 'random'
    
    repeat_f = options[0]
    repeat_v = options[1]
    parameters = options[2]
    
    vqc_circuit = QuantumCircuit(n)
    
    # feature map
    vqc_circuit.append(zz_feature_map(n, reps=repeat_f), range(n))
    vqc_circuit.barrier()
    
    # variational form
    vqc_circuit.append(real_amplitudes(n, reps=repeat_v), range(n))
    
    if parameters == 'random':
        vqc_circuit.assign_parameters(
            {p:np.random.uniform(low=-np.pi, high=np.pi) for p in vqc_circuit.parameters}, 
            inplace=True)
    else:
        # NOT YET TESTED
        bind_dict = parameters
        # for key in vqc_circuit.parameters:
            # bind_dict[key] = 
        vqc_circuit.assign_parameters(bind_dict, inplace=True)
        
    vqc_circuit.measure_all()
    
    return vqc_circuit