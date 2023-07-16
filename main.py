import sys
import time
import numpy as np
from src.utils import phase_polynomial_from_circ, get_cnot_count_depth
from src.frontend import qc_to_circ, circ_to_qc
from src.alg import phase_polynomial_synthesis, linear_reversible_function_synthesis

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        (header, qubits_mapping, c_init) = qc_to_circ(filename)
        nb_qubits = len(qubits_mapping)
        (table, angles) = phase_polynomial_from_circ(c_init, nb_qubits)
        start = time.process_time()
        c = phase_polynomial_synthesis(table, angles)
        t = time.process_time() - start
        matrix = np.eye(nb_qubits, dtype=bool)
        for (gate, qubits) in c[::-1] + c_init:
            if gate == "cx":
                matrix[qubits[1]] ^= matrix[qubits[0]]
        c += linear_reversible_function_synthesis(matrix)
        (count, depth) = get_cnot_count_depth(c, nb_qubits)
        print("CNOT count:", count)
        print("CNOT depth:", depth)
        print("Time :", t, "seconds")
        circ_to_qc(c, "outputs/"+filename.split("/")[-1], header, qubits_mapping)

if __name__ == "__main__":
    main()
