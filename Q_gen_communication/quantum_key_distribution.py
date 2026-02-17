# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-key-distribution.ipynb
# 021126 Yikai Mao

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

def encode_message(n, bits, bases):
    
    encoder = QuantumCircuit(n)
    
    for i in range(n):
        
        # Prepare qubit in Z-basis
        if bases[i] == '0':
            if bits[i] == '0':
                pass 
            else:
                encoder.x(i)
                
        # Prepare qubit in X-basis
        else:
            if bits[i] == '0':
                encoder.h(i)
            else:
                encoder.x(i)
                encoder.h(i)
    
    encoder = encoder.to_gate(label='encoder')
    
    return encoder

def decode_message(n, bases):
    
    decoder = QuantumCircuit(n)
    
    for i in range(n):
        
        # measuring in Z-basis
        if bases[i] == '0':
            pass
        
        # measuring in X-basis
        if bases[i] == '1':
            decoder.h(i)
    
    decoder = decoder.to_gate(label='decoder')
    
    return decoder

def remove_garbage(n, a_bases, b_bases, bits):
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            # If both used the same basis, add
            # this to the list of 'good' bits
            good_bits.append(bits[q])
    return good_bits

def sample_bits(bits, selection):
    sample = []
    for i in selection:
        # # use np.mod to make sure the
        # # bit we sample is always in 
        # # the list range
        # i = np.mod(i, len(bits))
        # # pop(i) removes the element of the
        # # list at index 'i'
        # sample.append(bits.pop(i))
        
        sample.append(bits[i])
    return sample

def quantum_key_distribution(n, options=[]):
    # options = [interception]
    # interception = 'interception', 'none', with/without eve's interception
    
    interception = options[0]
    
    quantum_key_distribution_circuit = QuantumCircuit(n,n)
    
    # step 1
    alice_bits = random_bin_str(n, True)
    alice_bases = random_bin_str(n, True)
    bob_bases = random_bin_str(n, True)
    message = encode_message(n, alice_bits, alice_bases)
    # print('alice bases =  ', alice_bases)
    # print('alice message =', alice_bits)
    # print('bob bases =  ', bob_bases)
        
    # step 2
    quantum_key_distribution_circuit.append(message, list(range(n)))
    quantum_key_distribution_circuit.barrier()
    
    # interception
    if interception == 'interception':
        eve_bases = random_bin_str(n, True)
        # eve_bases = bob_bases
        # print('****eve bases (eve steals from bob)=', eve_bases)
        quantum_key_distribution_circuit.append(decode_message(n, eve_bases), list(range(n)))
        quantum_key_distribution_circuit.barrier()
        for i in range(n):
            quantum_key_distribution_circuit.measure(i, i)
        quantum_key_distribution_circuit.barrier()
    
    # step 3
    quantum_key_distribution_circuit.append(decode_message(n, bob_bases), list(range(n)))
    quantum_key_distribution_circuit.barrier()
    for i in range(n):
        quantum_key_distribution_circuit.measure(i, i)
    
    return quantum_key_distribution_circuit

def play_quantum_key_distribution(n, options=[]):
    # play a round of key distribution with simulation
    # options = [run_ideal_simulation]
    # run_ideal_simulation = run_ideal_simulation() from helper_functions.py
    # require "from helper_functions import run_ideal_simulation"
    
    run_ideal_simulation = options[0]
    
    play_quantum_key_distribution_circuit = QuantumCircuit(n,n)
    
    # step 1
    alice_bits = random_bin_str(n, True)
    alice_bases = random_bin_str(n, True)
    bob_bases = random_bin_str(n, True)
    message = encode_message(n, alice_bits, alice_bases)
    print('alice bases =  ', alice_bases)
    print('alice message =', alice_bits)
    print('bob bases =  ', bob_bases)
        
    # step 2
    play_quantum_key_distribution_circuit.append(message, list(range(n)))
    play_quantum_key_distribution_circuit.barrier()
    
    # interception
    # eve_bases = random_bin_str(n, True)
    eve_bases = bob_bases
    print('****eve bases (eve steals from bob)=', eve_bases)
    play_quantum_key_distribution_circuit.append(decode_message(n, eve_bases), list(range(n)))
    play_quantum_key_distribution_circuit.barrier()
    for i in range(n):
        play_quantum_key_distribution_circuit.measure(i, i)
    play_quantum_key_distribution_circuit.barrier()
    raw_counts = run_ideal_simulation(play_quantum_key_distribution_circuit, 'CPU', 1, 0, None, 'silnet').get_counts()
    # reversed for qiskit endian
    eve_message = str(list(raw_counts.items())[0][0])[::-1]
    print('****eve message =', eve_message)
    eve_key = remove_garbage(n, alice_bases, eve_bases, alice_bits)
    print('****eve key =', eve_key)
    
    # step 3
    play_quantum_key_distribution_circuit.append(decode_message(n, bob_bases), list(range(n)))
    play_quantum_key_distribution_circuit.barrier()
    for i in range(n):
        play_quantum_key_distribution_circuit.measure(i, i)
    
    # step 4
    raw_counts = run_ideal_simulation(play_quantum_key_distribution_circuit, 'CPU', 1, 0, None, 'silnet').get_counts()
    # reversed for qiskit endian
    bob_message = str(list(raw_counts.items())[0][0])[::-1]
    print('bob message =', bob_message)
    alice_key = remove_garbage(n, alice_bases, bob_bases, alice_bits)
    bob_key = remove_garbage(n, alice_bases, bob_bases, bob_message)
    print('alice key =', alice_key)
    print('bob key =  ', bob_key)
    
    # step 5
    # Change this to something lower and see if 
    # Eve can intercept the message without Alice
    # and Bob finding out
    sample_size = int(np.floor(n/2))
    
    # bit_selection = np.random.randint(n, size=sample_size)
    bit_selection = np.random.randint(0, len(alice_key), size=sample_size)
    print('test bit index =', bit_selection)
    alice_sample = sample_bits(alice_key, bit_selection)
    bob_sample = sample_bits(bob_key, bit_selection)
    print('alice sample =', alice_sample)
    print('bob sample   =', bob_sample)
    if bob_sample != alice_sample:
        print("Eve's interference was detected.")
    else:
        print("Eve went undetected! (or no interception)")
    
    return play_quantum_key_distribution_circuit