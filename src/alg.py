import numpy as np
import networkx as nx

def phase_polynomial_synthesis(table, angles):
    table, angles = np.copy(table), np.copy(angles)
    nb_qubits = len(table)
    c = []

    def insert_cnot(i, j):
        nonlocal table, c
        c.append(("cx", [i, j]))
        table[i] ^= table[j]

    def implement_rotation(col):
        nonlocal table, angles, c, weights
        if sum(table[:,col]) != 1:
            lines = np.where(table[:, col])[0]
            for i in lines:
                indices = np.where(table[i])[0]
                for j in lines:
                    if i != j:
                        weights[i][j] = sum(table[j][indices])*2 - len(indices)

            edges = [(int(i), int(j), weights[i][j]) for i in lines for j in lines if i != j]
            dg = nx.DiGraph()
            dg.add_weighted_edges_from(edges)
            tree = nx.algorithms.tree.branchings.Edmonds(dg).find_optimum(style="arborescence")
            root = [n for n,d in tree.in_degree() if d==0][0]
            for (i, j) in reversed(list(nx.bfs_edges(tree, source=root))):
                insert_cnot(j, i)
        index = np.where(table[:,col])[0][0]
        if angles[col] % 2:
              c.append(("T", index)) 
        if angles[col] % 4 >= 2:
              c.append(("S", index)) 
        if angles[col] % 8 >= 4:
              c.append(("Z", index)) 
        table = np.delete(table, col, 1)
        angles = np.delete(angles, col)

    offset = 0
    for col in np.where(sum(table) <= 1)[0]:
        implement_rotation(col + offset)
        offset -= 1
    weights = np.identity(nb_qubits)
    while table.shape[1]:
        cols = np.argwhere(sum(table) == np.amin(sum(table)))
        for i in range(nb_qubits):
            ones = cols[np.where(table[i, cols])[0]]
            if len(ones):
                cols = ones
                if len(cols) == 1:
                    break
        implement_rotation(cols[0])
    return c

def lu_decomposition(matrix):
    nb_qubits = matrix.shape[0]
    p, l, u= np.eye(nb_qubits, dtype=bool), np.eye(nb_qubits, dtype=bool), matrix.copy()
    for i in range(nb_qubits):
        if u[i, i] != 1:
            j = np.where(u[:, i])[0][-1]
            p[[i, j]] = p[[j, i]]
            matrix[[i, j]] = matrix[[j, i]]
            u[[i, j]] = u[[j, i]]
        for j in range(i+1, nb_qubits):
            if u[j, i] == 1:
                u[j, :] ^= u[i, :]
    for i in range(nb_qubits):
        for j in range(i):
            if matrix[i, j] != sum(l[i, :] & u[:, j]) & 1:
                l[i, j] = 1
    return (p, l, u)

def greedy_ge(l):
    nb_qubits = l.shape[0]
    c = []
    for i in range(nb_qubits):
        weights = np.zeros((nb_qubits, nb_qubits), dtype=int)
        rows = np.argwhere(l[:,i])
        for j in rows:
            for k in rows:
                if k <= j:
                    continue
                for col in range(i, nb_qubits):
                    if l[j, col] != l[k, col]:
                            break
                    weights[j, k] += 1 
        while np.max(weights) > 0:
            (j, k) = np.unravel_index(np.argmax(weights), weights.shape)
            c.append(("cx", (j, k)))
            l[k,:] ^= l[j,:]
            for j in range(nb_qubits):
                weights[j, k] = 0
    return c

def linear_reversible_function_synthesis(matrix):
    m = matrix.copy()
    m2 = matrix.copy()
    (p, l, u) = lu_decomposition(matrix)
    c = []
    for i in range(p.shape[0]):
        if not p[i, i]:
            j = np.where(p[:, i])[0][0]
            p[[i, j]] = p[[j, i]]
            c += [("cx", (i, j)), ("cx", (j, i)), ("cx", (i, j))]
    c.reverse()
    c += greedy_ge(l)
    for (gate, (i, j)) in greedy_ge(np.transpose(u))[::-1]:
        c.append((gate, (j, i)))
    for (gate, (i, j)) in c:
        m[j,:] ^= m[i,:]
    return c[::-1]
