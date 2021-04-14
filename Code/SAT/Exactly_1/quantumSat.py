"""
This is the main class where we build the instance of the circuit and run Grover's search un order to find the
solution to our Exactly-1 k-SAT problem.

We can assume that the variables of each clause are provided in a file in increasing order; without loss of
generality this assumption allows us to manage easier the configuration of the quantum circuit able to solve
the problem.
"""

from sys import argv

from groverSat import GroverSAT
from qiskit.visualization import *
import matplotlib.pyplot as plt


def run_solver(input_file, b, cycles, system):
    instance = GroverSAT.from_file(input_file)
    instance.grover(cycles)

    # once I have the instance of my grover quantum circuit I measure the interested qubits for the result
    for j in range(instance.n):
        instance.circuit.measure(instance.f_in[j], instance.ans[j])
    job = instance.solve(b, system)
    counts = job.result().get_counts('grover')

    # circuit is drawn in a file in the Circuits folder
    instance.circuit.draw(scale=0.8, filename='Circuits/' + argv[1] + 'circuit', output='mpl',
                          fold=300, vertical_compression='low')

    # diagrams
    plot_histogram(counts, figsize=(16, 9))
    plt.show()


def main(args):
    file = open('Input/' + args[1], 'r')
    run_solver(file, int(args[2]), int(args[3]), args[4] if len(args) == 5 else 'MELBOURNE')


if __name__ == '__main__':
    main(argv)
