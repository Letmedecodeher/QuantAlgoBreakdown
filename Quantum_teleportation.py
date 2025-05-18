# Step 2: Verify Qiskit installation
import qiskit
print("Qiskit version:", qiskit._version_)

# Required imports
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from IPython.display import display

# Create a quantum circuit with 1 qubit and 1 classical bit
qc = QuantumCircuit(1, 1)
qc.h(0)             # Apply Hadamard to put in superposition
qc.measure(0, 0)    # Measure the qubit

print("Simple Superposition Circuit:")
display(qc.draw(output='mpl'))

# Simulate
backend = Aer.get_backend('qasm_simulator')
job = backend.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

print("Measurement Results:")
plot_histogram(counts)
plt.show()

# === Test Conditional Gate ===
print("\n=== Test Conditional Gate ===\n")
test_qreg = QuantumRegister(1, name="tq")
test_creg = ClassicalRegister(1, name="tc")
test_circuit = QuantumCircuit(test_qreg, test_creg)

test_circuit.measure(test_qreg[0], test_creg[0])
x_instr = test_circuit.x(test_qreg[0])  # Apply X gate
x_instr[0].c_if(test_creg[0], 1)        # Make it conditional

print("Test Conditional Circuit:")
display(test_circuit.draw(output='mpl'))

# Simulate test circuit
print("\nSimulating test circuit...")
test_job = backend.run(test_circuit, shots=100)
test_result = test_job.result()
test_counts = test_result.get_counts()
print("Test Simulation Results:")
print(test_counts)

# === Quantum Teleportation Circuit ===
print("\n=== Quantum Teleportation Circuit ===\n")

qreg = QuantumRegister(3, name="q")  # Qubits: [0]=ψ, [1]=A, [2]=B
creg = ClassicalRegister(2, name="c")  # Classical bits

teleport_circuit = QuantumCircuit(qreg, creg)

# Step 1: Prepare |+> state to teleport
teleport_circuit.h(qreg[0])
teleport_circuit.barrier()

# Step 2: Entangle A and B
teleport_circuit.h(qreg[1])
teleport_circuit.cx(qreg[1], qreg[2])
teleport_circuit.barrier()

# Step 3: Bell measurement of ψ and A
teleport_circuit.cx(qreg[0], qreg[1])
teleport_circuit.h(qreg[0])
teleport_circuit.barrier()

# Step 4: Measure ψ and A
teleport_circuit.measure(qreg[0], creg[0])
teleport_circuit.measure(qreg[1], creg[1])
teleport_circuit.barrier()

# Step 5: Apply classical corrections to B
x_gate = teleport_circuit.x(qreg[2])
x_gate[0].c_if(creg[1], 1)
z_gate = teleport_circuit.z(qreg[2])
z_gate[0].c_if(creg[0], 1)

print("Quantum Teleportation Circuit:")
display(teleport_circuit.draw(output='mpl', fold=15))

# Simulate
print("\nSimulating teleportation...")
job = backend.run(teleport_circuit, shots=1)
result = job.result()
counts = result.get_counts()
print("Simulation Results:")
print(counts)

# Optional: Verify final qubit B state (should be |+>)
verify_circuit = teleport_circuit.copy()
verify_circuit.barrier()
verify_circuit.h(qreg[2])  # Convert |+> to |0> for verification
verify_measure = ClassicalRegister(1, 'verify')
verify_circuit.add_register(verify_measure)
verify_circuit.measure(qreg[2], verify_measure[0])

verify_job = backend.run(verify_circuit, shots=100)
verify_result = verify_job.result()
verify_counts = verify_result.get_counts()

print("\nVerification Results (ideally mostly '0'):")
print(verify_counts)