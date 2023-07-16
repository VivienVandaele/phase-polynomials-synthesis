Phase polynomials synthesis algorithm based on the paper [Phase polynomials synthesis algorithms for NISQ architectures and beyond](https://arxiv.org/abs/2104.00934).

### Installation
The numpy and networkx packages are required
```
pip install numpy networkx
```

To run the code, execute the following command
```
python main.py [-cnot-circuit] <filename>.qc
```
The option `-cnot-circuit` indicates that the final CNOT circuit should be implemented.
If this option is not provided, the output circuit will be equal to the input circuit up to a final CNOT circuit.
The optimized circuit will be placed in the `outputs` directory.
