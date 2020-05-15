"""
This class allows to build a quantum circuit that is able to encode
every instance of a general k-SAT problem as it can be used to show
the complexity speedup with respect the classical solver. This
program has been used as a first approach to the implementation of a
quantum algorithm, and it follows the description given in:

            https://doi.org/10.1023/A:1009651417615

The files that we will consider to study the satisfiability problem
belong to the particular class called 3-SAT where 3 is the number
of literals every clause can be at most composed of.

I assume that the clauses parsed in the file are always ordered in
lexicographical order. Typical files will be in the form:

                            1 -2 3
                            1 2 -3
                            -1 -2 -3

In this way the construction of the quantum circuit can be done
with one single scan of all the clauses of the circuit encoding
them at the exact time when they are parsed.
"""

from qiskit import *


class SATInstance(object):
    def __init__(self):
        self.variables = 3
        self.quantumCircuit = QuantumCircuit(QuantumRegister(self.variables, 'x'))
        self.variables_dict = dict()
        self.clauses = []
        self.regCount = 0

    def parse_clause(self, line):
        first = True
        self.clauses.append(0)
        for literal in line.split():
            negated = 1 if literal.startswith('-') else 0
            variable = literal[negated:]

            if variable not in self.variables_dict:
                self.variables_dict[variable] = self.variables_dict.__len__()
            pos = self.variables_dict[variable]

            # now I bring the variable on the ancilla and build the or of the literals
            self.quantumCircuit.add_register(QuantumRegister(1, 'y' + str(self.regCount)))
            self.quantumCircuit.cx(pos, self.variables + self.regCount)

            if negated == 1:
                self.quantumCircuit.x(self.variables + self.regCount)
            if len(line) > 2:
                self.quantumCircuit.x(self.variables + self.regCount)
            if first:
                first = False
            else:
                self.regCount += 1
                self.quantumCircuit.add_register(QuantumRegister(1, 'y' + str(self.regCount)))
                self.quantumCircuit.x(self.variables + self.regCount)
                self.quantumCircuit.ccx(self.variables + self.regCount - 2, self.variables + self.regCount - 1,
                                        self.variables + self.regCount)
                if literal != line.split()[-1]:
                    self.quantumCircuit.x(self.variables + self.regCount)

            self.clauses[self.clauses.__len__() - 1] = self.variables + self.regCount
            self.regCount += 1

    @classmethod
    def from_file(cls, file):
        instance = cls()
        for line in file:
            line = line.strip()
            if len(line) > 0 and not line.startswith('#'):
                instance.parse_clause(line)
        return instance
