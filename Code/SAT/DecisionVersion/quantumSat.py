"""
This is the main class where the circuit is built from the instance and its solution is retrieved.
The clauses still need to be conjuncted in order to obtain the CNF and then solve the instance
of the 3-SAT that has been parsed.
"""

from sys import argv

from satInstance import SATInstance
from qiskit import QuantumRegister
from qiskit.visualization import *
import matplotlib.pyplot as plt


def run_solver(input_file):
    instance = SATInstance.from_file(input_file)
    clauses = instance.clauses

    partial_result = instance.variables + instance.regCount
    partial_index = 0
    instance.quantumCircuit.barrier()
    instance.quantumCircuit.add_register(QuantumRegister(2 + 2 * (len(clauses) - 2), 'z'))
    instance.quantumCircuit.add_register(QuantumRegister(1, 'f(x_0, x_1, x_2)'))

    while partial_index < len(clauses):
        first = partial_result
        second = first + 1

        if partial_index == 0:
            instance.quantumCircuit.cx(clauses[partial_index], first)
            partial_index += 1

        instance.quantumCircuit.cx(clauses[partial_index], second)
        partial_index += 1
        partial_result += 2
        instance.quantumCircuit.ccx(first, second, partial_result)

    # basic text circuit is drawn in a file in the Circuits folder
    circuit_drawer(instance.quantumCircuit, 0.7, 'Circuits/' + argv[1] + 'circuit', fold=300)

    # fancy circuit
    instance.quantumCircuit.draw(output='mpl')
    plt.show()


def main(args):
    file = open('Input/' + args[1], 'r')
    run_solver(file)


if __name__ == '__main__':
    main(argv)
