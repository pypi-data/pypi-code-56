from pyquil import get_qc, Program
from pyquil.api._quantum_computer import _get_qvm_qc
from pyquil.device.devices import ibmq_ourense, ibmq_yorktown, google_bristlecone
import time

t0 = time.time()
yorktown_device = ibmq_ourense()
t1 = time.time()
qc = _get_qvm_qc("ibmq_yorktown", "qvm", device=yorktown_device)
t2 = time.time()

print(t1 - t0)
print(t2 - t1)

# Non-native CNOT
program = Program("CNOT 1 0")
print(qc.compile(program, protoquil=True).program)
t3 = time.time()

print(t3 - t2)

# Native CNOT
program = Program("CNOT 0 1")
print(qc.compile(program, protoquil=True).program)

qc = get_qc("Aspen-4-4Q-A-qvm")
program = Program("CNOT 0 1")
print(qc.compile(program).program)
