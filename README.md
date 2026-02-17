
# Q-gen Quantum Circuit Generator

Please see our preprint on arXiv:  

[Q-gen: A Parameterized Quantum Circuit Generator](https://arxiv.org/abs/2407.18697)

Our [Wiki](https://github.com/yikaimao/Q_gen/wiki) page offers an overview of the simple circuits inside the Q-gen quantum circuit dataset: 

 - Circuit visualization with histogram/counts: [Circuit with histogram/counts](https://github.com/yikaimao/Q_gen/wiki#circuit-with-histogramcounts)
 - State vector simulation results: [State vectors](https://github.com/yikaimao/Q_gen/wiki#state-vectors)
 - Real measurement outputs from IBM quantum processors: [Real measurement outputs](https://github.com/yikaimao/Q_gen/wiki#real-measurement-outputs-from-ibm-quantum-processors)

The full dataset is available at [Q-gen Quantum Circuit Dataset](https://www.kaggle.com/datasets/ykmaoykmao/q-gen-quantum-circuit-dataset).

## Available Algorithms

![algorithms overview](images/alg_system.png)

**Quantum Query Algorithms:**  
 - Deutsch-Jozsa Algorithm  
 - Bernstein-Vazirani Algorithm  
 - Simon's Algorithm

**Quantum Fourier Transform Algorithms:**  
 - Quantum Fourier Transform  
 - Quantum Phase Estimation  
 - Shor's Algorithm

**Quantum Search Algorithms:**  
 - Grover's Algorithm  
 - Quantum Counting Algorithm  
 - Quantum Walk Algorithm  

**Quantum Communication Algorithms:**  
 - Quantum Key Distribution  
 - Quantum Teleportation  
 - Superdense Coding  

**Variational Quantum Algorithms:**  
 - Quantum Approximate Optimization Algorithm  
 - Variational Quantum Eigensolver  
 - Variational Quantum Classifier

```
Dependencies:
    numpy
    qiskit 0.46.0
    qiskit-aer-gpu 0.13.3
    networkx
```

## Acknowledgements

We thank the community for sharing many algorithm implementations and learning resources:

 - [Qiskit](https://github.com/Qiskit/qiskit)
 - [Qiskit Textbook](https://github.com/Qiskit/textbook) (deprecated)
 - [Qiskit Algorithms](https://github.com/qiskit-community/qiskit-algorithms)
 - [Qiskit Machine Learning](https://github.com/qiskit-community/qiskit-machine-learning)
 - [ShorAlgQiskit](https://github.com/ttlion/ShorAlgQiskit) by Rui Maia and Tiago Leão

## License

[MIT License](LICENSE.txt)
