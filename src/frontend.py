import sys

def qc_to_circ(filename):
    c = []
    with open(filename) as f:
        header = ""
        line = f.readline()
        while line != "BEGIN\n":
            header += line
            line = f.readline()
        qubits_mapping = {}
        nb_qubits = 0
        line = f.readline().strip()
        while line != "END":
            w = line.split(" ")
            for i in range(1, len(w)):
                if w[i] not in qubits_mapping:
                    qubits_mapping[w[i]] = nb_qubits
                    nb_qubits += 1
            if w[0] == "tof" and len(w) == 3:
                c += [("cx", (qubits_mapping[w[1]], qubits_mapping[w[2]]))]
            elif w[0] == "T" and len(w) == 2:
                c += [("T", qubits_mapping[w[1]])]
            elif w[0] == "S" and len(w) == 2:
                c += [("S", qubits_mapping[w[1]])]
            elif w[0] == "Z" and len(w) == 2:
                c += [("Z", qubits_mapping[w[1]])]
            else:
                sys.exit("Operator not implemented: " + w[0])
            line = f.readline().strip()
    return header, qubits_mapping, c

def random_circ(filename, nb_qubits):
    from random import randint, random
    with open(filename, "w") as f:
        f.write(".v")
        for i in range(nb_qubits):
            f.write(" " + str(i))
        f.write("\nBEGIN\n")
        for _ in range(nb_qubits * nb_qubits):
            i, j = randint(0, nb_qubits-1), randint(0, nb_qubits-1)
            if i != j:
                f.write("tof " + str(i) + " " + str(j) + "\n")
            if random() < 0.2:
                f.write("T " + str(randint(0, nb_qubits-1)) + "\n")
            if random() < 0.2:
                f.write("Z " + str(randint(0, nb_qubits-1)) + "\n")
            if random() < 0.2:
                f.write("S " + str(randint(0, nb_qubits-1)) + "\n")
        f.write("END\n")

def circ_to_qc(c, filename, header, qubits_mapping):
    reverse_mapping = {}
    for (key, value) in qubits_mapping.items():
        reverse_mapping[value] = key
    with open(filename, "w") as f:
        f.write(header)
        f.write("BEGIN\n")
        for (gate, qubits) in c:
            if gate == "cx":
                f.write("tof " + reverse_mapping[qubits[0]] + " " + reverse_mapping[qubits[1]] + "\n")
            elif gate == "T":
                f.write("T " + reverse_mapping[qubits] + "\n")
            elif gate == "S":
                f.write("S " + reverse_mapping[qubits] + "\n")
            elif gate == "Z":
                f.write("Z " + reverse_mapping[qubits] + "\n")
            else:
                sys.exit("Operator not implemented: " + gate)
        f.write("END\n")
