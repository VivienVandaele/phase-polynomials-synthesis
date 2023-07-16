import numpy as np

def phase_polynomial_from_circ(c, nb_qubits):
    matrix = np.eye(nb_qubits, dtype=bool)
    parities = {}
    for (gate, qubits) in c:
        if gate == "cx":
            matrix[qubits[1]] ^= matrix[qubits[0]]
        elif gate == "T" or gate == "S" or gate == "Z":
            if tuple(matrix[qubits]) not in parities:
                parities[tuple(matrix[qubits])] = 0
            if gate == "T":
                parities[tuple(matrix[qubits])] += 1
            elif gate == "S":
                parities[tuple(matrix[qubits])] += 2
            elif gate == "Z":
                parities[tuple(matrix[qubits])] += 4
    table = np.empty((nb_qubits, 0), dtype=bool)
    angles = np.zeros(len(parities), dtype=int)
    for (p, angle) in parities.items():
        angles[table.shape[1]] = angle
        table = np.append(table, np.atleast_2d(p).T, axis=1)
    return (table, angles)

def get_cnot_count_depth(c, nb_qubits):
    count = 0
    depth = np.zeros(nb_qubits, dtype=int)
    for (gate, qubits) in c:
        if gate == "cx":
            count += 1
            depth[qubits[0]] = max(depth[qubits[0]], depth[qubits[1]]) + 1
            depth[qubits[1]] = depth[qubits[0]]
    return (count, max(depth))
