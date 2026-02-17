# https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/shor.ipynb
# https://github.com/ttlion/ShorAlgQiskit
# 012126 Yikai Mao

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from numpy import pi, zeros
from random import choice
import math
from Q_gen_qft.qft import qft

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def get_value_a(N):
    # a and N are coprime
    a = 2
    a_list = []
    
    while a <= N:
        if math.gcd(a,N) == 1:
            a_list.append(a)
        a = a + 1
        
    return a_list
    
def getAngles(a,N):
    # calculates the array of angles to be used in the addition in Fourier Space
    s=bin(int(a))[2:].zfill(N) 
    angles=zeros([N])
    for i in range(0, N):
        for j in range(i,N):
            if s[j]=='1':
                angles[N-i-1]+=math.pow(2, -(j-i))
        angles[N-i-1]*=pi
    return angles

def ccphase(circuit,angle,ctl1,ctl2,tgt):
    # doubly controlled phase gate
    circuit.cu(0,0,angle/2,0,ctl1,tgt)
    circuit.cx(ctl2,ctl1)
    circuit.cu(0,0,-angle/2,0,ctl1,tgt)
    circuit.cx(ctl2,ctl1)
    circuit.cu(0,0,angle/2,0,ctl2,tgt)

def phiADD(circuit,q,a,N,inv):
    # performs addition by a in Fourier Space
    # Can also be used for subtraction by setting the parameter inv to a value different from 0
    angle=getAngles(a,N)
    for i in range(0,N):
        if inv==0:
            circuit.p(angle[i],q[i])
        else:
            circuit.p(-angle[i],q[i])

def cphiADD(circuit,q,ctl,a,n,inv):
    # Single controlled version of the phiADD circuit
    angle=getAngles(a,n)
    for i in range(0,n):
        if inv==0:
            circuit.cu(0,0,angle[i],0,ctl,q[i])
        else:
            circuit.cu(0,0,-angle[i],0,ctl,q[i])

def ccphiADD(circuit,q,ctl1,ctl2,a,n,inv):
    # Doubly controlled version of the phiADD circuit
    angle=getAngles(a,n)
    for i in range(0,n):
        if inv==0:
            ccphase(circuit,angle[i],ctl1,ctl2,q[i])
        else:
            ccphase(circuit,-angle[i],ctl1,ctl2,q[i])

def create_QFT(circuit,up_reg,n,with_swaps,inv):
    if inv==0:
        i=n-1
        # Apply the H gates and Cphases
        # The Cphases with |angle| < threshold are not created because they do 
        # nothing. The threshold is put as being 0 so all CPhases are created,
        # but the clause is there so if wanted just need to change the 0 of the
        # if-clause to the desired value
        while i>=0:
            circuit.h(up_reg[i])        
            j=i-1  
            while j>=0:
                if (pi)/(pow(2,(i-j))) > 0:
                    circuit.cu(0,0,(pi)/(pow(2,(i-j))),0 , up_reg[i] , up_reg[j] )
                    j=j-1   
            i=i-1  
    
        # If specified, apply the Swaps at the end
        if with_swaps==1:
            i=0
            while i < ((n-1)/2):
                circuit.swap(up_reg[i], up_reg[n-1-i])
                i=i+1
                
    if inv==1:
        # If specified, apply the Swaps at the beggining
        if with_swaps==1:
            i=0
            while i < ((n-1)/2):
                circuit.swap(up_reg[i], up_reg[n-1-i])
                i=i+1
        
        # Apply the H gates and Cphases
        # The Cphases with |angle| < threshold are not created because they do 
        # nothing. The threshold is put as being 0 so all CPhases are created,
        # but the clause is there so if wanted just need to change the 0 of the
        # if-clause to the desired value
        i=0
        while i<n:
            circuit.h(up_reg[i])
            if i != n-1:
                j=i+1
                y=i
                while y>=0:
                     if (pi)/(pow(2,(j-y))) > 0:
                        circuit.cu(0,0, - (pi)/(pow(2,(j-y))),0 , up_reg[j] , up_reg[y] )
                        y=y-1   
            i=i+1

def ccphiADDmodN(circuit, q, ctl1, ctl2, aux, a, N, n, inv):
    # doubly controlled modular addition by a
    if inv==0:
        ccphiADD(circuit, q, ctl1, ctl2, a, n, 0)
        phiADD(circuit, q, N, n, 1)
        create_QFT(circuit, q, n, 0, 1)
        circuit.cx(q[n-1],aux)
        create_QFT(circuit,q,n,0,0)
        cphiADD(circuit, q, aux, N, n, 0)
        
        ccphiADD(circuit, q, ctl1, ctl2, a, n, 1)
        create_QFT(circuit, q, n, 0, 1)
        circuit.x(q[n-1])
        circuit.cx(q[n-1], aux)
        circuit.x(q[n-1])
        create_QFT(circuit,q,n,0,0)
        ccphiADD(circuit, q, ctl1, ctl2, a, n, 0)
        
    if inv==1:
        ccphiADD(circuit, q, ctl1, ctl2, a, n, 1)
        create_QFT(circuit, q, n, 0, 1)
        circuit.x(q[n-1])
        circuit.cx(q[n-1],aux)
        circuit.x(q[n-1])
        create_QFT(circuit, q, n, 0, 0)
        ccphiADD(circuit, q, ctl1, ctl2, a, n, 0)
        
        cphiADD(circuit, q, aux, N, n, 1)
        create_QFT(circuit, q, n, 0, 1)
        circuit.cx(q[n-1], aux)
        create_QFT(circuit, q, n, 0, 0)
        phiADD(circuit, q, N, n, 0)
        ccphiADD(circuit, q, ctl1, ctl2, a, n, 1)

def cMULTmodN(circuit, ctl, q, aux, a, N, n):
    # single controlled modular multiplication by a
    create_QFT(circuit,aux,n+1,0,0)
    for i in range(0, n):
        ccphiADDmodN(circuit, aux, q[i], ctl, aux[n+1], (2**i)*a % N, N, n+1, 0)
    create_QFT(circuit, aux, n+1, 0, 1)

    for i in range(0, n):
        circuit.cswap(ctl,q[i],aux[i])

    a_inv = modinv(a, N)
    create_QFT(circuit, aux, n+1, 0, 0)
    i = n-1
    while i >= 0:
        ccphiADDmodN(circuit, aux, q[i], ctl, aux[n+1], math.pow(2,i)*a_inv % N, N, n+1, 1)
        i -= 1
    create_QFT(circuit, aux, n+1, 0, 1)
    
def shor(N, options=[]):
    # in Shor's algrithm, N is the number to be factored
    # options = [a]
    # a = 'random', use random a. 'min', use the smallest a

    random = options[0]
    
    a_list = get_value_a(N)
    if random:
        a = choice(a_list)
    else:
        a = a_list[0]
    # print('a =', a)
        
    n = math.ceil(math.log(N,2))
    # print('Total number of qubits used: {0}\n'.format(4*n+2))
    
    aux = QuantumRegister(n+2, 'aux')
    up_reg = QuantumRegister(2*n, 'counting')
    down_reg = QuantumRegister(n, 'mod_mult')
    up_classic = ClassicalRegister(2*n, 'c')

    shor_circuit = QuantumCircuit(down_reg, up_reg, aux, up_classic)
    shor_circuit.h(up_reg)
    shor_circuit.x(down_reg[0])
    
    for i in range(0, 2*n):
        temp_circuit = QuantumCircuit(down_reg, up_reg, aux)
        cMULTmodN(temp_circuit, up_reg[i], down_reg, aux, int(pow(a, pow(2, i))), N, n)
        temp_circuit = temp_circuit.to_instruction(label='c_mod_mult')
        shor_circuit = shor_circuit & temp_circuit
        
    inv_qft_circuit = qft(2*n, [-1, True, False]).to_instruction(label='inv_qft')
    shor_circuit = shor_circuit.compose(inv_qft_circuit, up_reg)

    shor_circuit.measure(up_reg, up_classic)
    
    return shor_circuit