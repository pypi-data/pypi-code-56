from pyquil import get_qc, Program
from pyquil.api._quantum_computer import _get_qvm_qc
from pyquil.device._library import ibmq_ourense, ibmq_yorktown


yorktown_device = ibmq_yorktown()
qc = _get_qvm_qc("ibmq_yorktown", "qvm", device=yorktown_device)

# Non-native CNOT
program = Program("CNOT 1 0")
print(qc.compile(program, protoquil=True).program)

# Native CNOT
program = Program("CNOT 0 1")
print(qc.compile(program, protoquil=True).program)
