def create_quantum_circuit(num_qubits):

    from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

    QR = QuantumRegister(num_qubits)
    CR = ClassicalRegister(num_qubits)
    QC = QuantumCircuit(QR, CR)

    return QC
