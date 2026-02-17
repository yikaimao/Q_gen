# helper functions
# 122225 Yikai Mao

from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def decomposer(circ, level=1):
    # decompose the circuit to see the basis gates
    # level = how many times to decompose
    
    decomposed_circ = circ
    
    for i in range(level):
        decomposed_circ = decomposed_circ.decompose()
        
    return decomposed_circ

def show_circuit(circuit, decompose_level):
    # output = text, mpl, latex, latex_source
    # style = iqp, iqp-dark, textbook, bw, clifford
    
    display(decomposer(circuit, decompose_level).draw(output = 'mpl', style="iqp-dark"))

    return None

def run_ideal_simulation(circuit, device, shots, optimization_level, seed, verbose):
    # assume perfect quantum computer with no noise
    # circuit = circuit to simulate, BEFORE transpilation
    # device = 'CPU' or 'GPU'
    # shots = how many shots to run
    # optimization_level = passed to the transpiler, min = 0, max = 3
    # seed = random seed for simultaion, can be None
    # verbose = 'verbose', 'silent'
    
    # print("available simulators:")
    # print(AerSimulator().available_methods())
    # print("available devices:")
    # print(AerSimulator().available_devices())

    if device == 'GPU':
        simulator = AerSimulator(device='GPU', cuStateVec_enable=True)
    elif device == 'CPU':
        simulator = AerSimulator(device='CPU')

    if verbose == 'verbose':
        print('---- START ----')
        print('simulator name =', simulator.configuration().to_dict()['backend_name'])

        print('max supported #qubits =', simulator.configuration().to_dict()['n_qubits'])
        print('#qubits of circuit =', circuit.num_qubits)
        print('#clbits of circuit =', circuit.num_clbits)

    if circuit.num_qubits > simulator.configuration().to_dict()['n_qubits']:
        print('too many qubits for the simulator!')
        print('---- FAIL ----')
        return None

    trans_qc = transpile(circuit, simulator, optimization_level=optimization_level)
    job = simulator.run(trans_qc, shots=shots, seed_simulator=seed)
    result = job.result()

    if verbose == 'verbose':
        print('---- DONE ----')
    
    return result

def sim_result_analysis(sim_result, show_plot, show_counts, show_probs, verbose):
    # show_plot = 'show_plot', 'silent'
    # show_counts = 'show_counts', 'silent'
    # show_probs = 'show_probs', 'silent'
    # verbose = 'verbose', 'silent'

    result_dict = sim_result.to_dict()

    if result_dict['status'] != 'COMPLETED':
        print(result_dict['status'])
        return

    device = result_dict['results'][0]['metadata']['device']
    # https://qiskit.org/ecosystem/aer/howtos/running_gpu.html
    device_time = result_dict['metadata']['time_taken_execute']
    total_time = sim_result.time_taken
    sim_time = [device, device_time, total_time]

    if verbose == 'verbose':
        print('device =', device)
        print('device time =', device_time)
        print('total time =', total_time)

    # build simulation result dict
    try:
        raw_counts = sim_result.get_counts()
    except:
        print('result error, output has no counts')
        return
      
    sorted_counts = {}
    # print("raw counts:\n", raw_counts)
    num_clbits = result_dict['results'][0]['metadata']['num_clbits']
    # sorting the raw counts, add state zero
    for i in range(pow(2, num_clbits)):
        bin_str = format(i, str('0>' + str(num_clbits) + 'b'))
        if bin_str not in raw_counts:
            sorted_counts[bin_str] = 0
        else:
            sorted_counts[bin_str] = raw_counts[bin_str]

    shots = sum(sorted_counts.values())
    sorted_probs = sorted_counts.copy()
    for key, value in sorted_probs.items():
        sorted_probs[key] = value/shots*100

    if show_plot == 'show_plot':
        plot = plot_histogram(sorted_counts, 
                              number_to_keep=len(sorted_counts), 
                              sort='value_desc', 
                              title='ideal simulation (sorted)')
        display(plot)
        
    if show_counts == 'show_counts':
        print('sorted counts:')
        print(sorted_counts)

    if show_probs == 'show_probs':
        print('sorted probabilities (%):')
        print(sorted_probs)
    
    return sim_time, raw_counts, sorted_counts, sorted_probs