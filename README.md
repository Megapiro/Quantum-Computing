# Introduction
This repository contains the material I used in order to face the __Quantum Computing__ area. I started to study this field thanks to a university project where I had to choose an algorithm to make a comparison between a classical and a quantum solver. In particular I decided to study the [SAT](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem) problem for its importance in the field of __Artificial Intelligence__ but also to show the impact of the enhancements provided by quantum algorithms on one of the most important problems for __Computational Theory__.

# Structure of this Repository
Two directories make a distinction between the implementations I realized and the corresponding documentation, respectively in the __Code__ and __Report__ folders we will find a folder for each of the studies. Up to now we can only find my first approach related to the __SAT__ problem with the sources and documentations that I realized at the end of my work. The result of my first research project is a paper that tries to give a description of the state of the art by providing coding examples to clarify the difficult quantum principles behind the real algorithms. 

## Code Folder
This folder contains the quantum implementations that I realized in order to deepen my knowledge in this very mathematical and complex area called __Quantum Computing__. Each directory focuses on a particular problem, in this first version we can see in the __SAT__ the different algorithms that I decided to implement for the aim of my research project, thus the comparison with the classical counterpart solver. 

The following table shows the libraries used to realize quantum algorithms and the respective implementations based on them:

|Library|Implementations|
|-------|---------------|
|[Qiskit](https://github.com/Qiskit)|SAT|

### SAT
In order to study the __Satisfiability Problem__ I developed three different implementations that are based on different approaches that can all be used in order to solve particular instances of the __SAT__. The following list provides a description of each algorithm and the respective commands to use the solvers:

* [Decision Version](https://github.com/Megapiro/Quantum-Computing/tree/master/Code/SAT/DecisionVersion): this implementation is able to encode in a quantum circuit the __Conjunctive Normal Form__ of a given __SAT__ specified in the respective folder. The solver that is based on this initialization considers the [Quantum Fourier Transform](https://en.wikipedia.org/wiki/Quantum_Fourier_transform) to find the solution. This solver only draws the representation of the conjunctive normal form for the SAT instance considered. It helped me to draw conclusions on the impossibility to implement a solver that encoded the problem in this way. To run the algorithm it suffices to use python and specify the name of the file containing the SAT problem to be represented:
```
python quantumSat.py satProblemDefinition 
```
* [Exactly-1 k-SAT](https://github.com/Megapiro/Quantum-Computing/tree/master/Code/SAT/Exactly_1): this implementation consists of a real solver able to find a solution for the general version of a k-SAT problem with "unlimited" number of variables and clauses. This solver is based on __Grover's search__ algorithm that uses [Amplitude Amplification](https://en.wikipedia.org/wiki/Amplitude_amplification) in order to find the correct solution. To execute the solver we need to pass four parameters:
  - __Problem Definition__: the file containing the formalization of the problem
  - __System Flag__: either 0 or 1, respectively 0 executes on the simulator while 1 on the real system
  - __Cycles__: integer specifying the number of times you want to iterate Grover's Algorithm
  - __System Name__: the name of the real system where you want to execute the algorithm. Check the enumeration [Systems](https://github.com/Megapiro/Quantum-Computing/blob/master/Code/SAT/Exactly_1/systems.py) for the specific name.

  In the end you will have to run using python with a code like the following:
  ```
  python quantumSat.py satProblemDefinition 0|1 #cycles MELBOURNE
  ```
* [Notebook](https://github.com/Megapiro/Quantum-Computing/blob/master/Code/SAT/quantumSat.ipynb): this jupyter notebook shows how the solver provided by Qiskit library is able to find the solution of very complex specifications of the problem. It has been used to start the approach with __Qiskit__ and to understand the __tradeof__ between the optimization regarding the number of qubits and the [decoherence](https://en.wikipedia.org/wiki/Quantum_decoherence).

## Report Folder
This folder contains the documentations related to the implementations I realized during my study. The result of my first research project is a paper that contains a brief introduction to the state of the art of quantum computing and then compares the quantum solvers with the classical counterparts. This paper is titled [An Introdution to Quantum Computing for Computer Scientist, with SAT](https://github.com/Megapiro/Quantum-Computing/blob/master/Report/SAT/Paper/QuantumSAT.pdf) and it contains the precise descriptions of all the three implementations that can be find in the __SAT__ folder in the Code section.
