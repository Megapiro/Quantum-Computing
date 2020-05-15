# First I define the dimensions of the quantum circuit: 
# 3 qubits for the variables + 
# + 5 ancilla qubits for each clause 
# + 1 = 14 qubits
qc = QuantumCircuit(QuantumRegister(14, 'x'))

# A quantum circuit once initialized has all qubits set to 0
# Hence we need to invert them when storing the clauses

# Encoding of the first clause: C_0 = notX_1, X_2, X_3
qc.cx(0, 3)
qc.cx(1, 4)
qc.x(4)
qc.x(3)
qc.x(4)
qc.x(5)
qc.ccx(3, 4, 5)	# notX_1 or X_2 now encoded on qubit 5
qc.cx(2, 6)
qc.x(6)
qc.x(5)
qc.x(6)
qc.x(7)
qc.ccx(5, 6, 7)	# notX_1 or X_2 or X_3 now encoded on qubit 7

# Encoding of the second clause: X_1, notX_2, X_3
qc.cx(0, 8)
qc.cx(1, 9)
qc.x(8)
qc.x(8)
qc.x(9)
qc.x(10)
qc.ccx(8, 9, 10) # X_1 or notX_2 now encoded on qubit 10
qc.cx(3, 11)
qc.x(11)
qc.x(10)
qc.x(11)
qc.x(12)
qc.ccx(10, 11, 12) # X_1 or notX_2 or X_3 now encoded on qubit 12

# Now that we have both partial results 
# we can compute the and of the two clauses
qc.ccx(7, 12, 13)
