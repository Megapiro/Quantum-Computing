"""
To implement the Grover's algorithm as we can use it to solve the Exactly-1 3-SAT problem
we will use three basic subroutines:
    (i) The first to construct the initial state
    (ii) The second to compute the unitary matrix Uf implementing the black-box function f
    (iii) The third to perform the inversion about the average

Remember that Grover's algorithm applies to a function with an n-qubit input and a single qubit output.
"""

from qiskit import *


class GroverSAT(object):
    def __init__(self, n, exactly_1_k_sat_formula):
        self.n = n
        self.exactly_1_k_sat_formula = exactly_1_k_sat_formula
        self.f_in = QuantumRegister(n, 'x')
        self.f_out = QuantumRegister(1)
        self.aux = QuantumRegister(len(exactly_1_k_sat_formula) + (max(n, len(exactly_1_k_sat_formula)) - 2))
        self.ans = ClassicalRegister(n)
        self.circuit = QuantumCircuit(self.f_in, self.f_out, self.aux, self.ans, name='grover')

    def __input_state(self):
        """ This is the (n+1)-quibit state for Grover's search """
        for j in range(self.n):
            self.circuit.h(self.f_in[j])
        self.circuit.x(self.f_out)
        self.circuit.h(self.f_out)
        self.circuit.barrier()
        self.circuit.barrier()

    def __black_box_u_f(self):
        """
        For each clause we construct a circuit that bit flips the corresponding auxiliary
        qubit if and only if the clause has exactly one true literal
        """
        num_clauses = len(self.exactly_1_k_sat_formula)
        self.__build_clauses(num_clauses)

        # the formula is satisfied if and only if all auxiliary qubits except the ancillas for the multiple CCNOT
        # are equal to 1
        s = 0
        target = 0
        while s < num_clauses:
            if s == 0:
                self.circuit.ccx(self.aux[0], self.aux[1], self.aux[num_clauses + target])
                s += 1
            elif s == num_clauses - 1:
                self.circuit.ccx(self.aux[s], self.aux[num_clauses + target - 1], self.f_out[0])
                target -= 2
            else:
                self.circuit.ccx(self.aux[s], self.aux[num_clauses + target - 1], self.aux[num_clauses + target])
            target += 1
            s += 1

        # This backwards while is used to reset the state of all the auxiliary qubits used
        s -= 3
        while s >= 0:
            if s == 0:
                self.circuit.ccx(self.aux[0], self.aux[1], self.aux[num_clauses + target])
            else:
                self.circuit.ccx(self.aux[s + 1], self.aux[num_clauses + target - 1], self.aux[num_clauses + target])
            target -= 1
            s -= 1

        self.__build_clauses(num_clauses)

    def __build_clauses(self, num_clauses):
        for (k, clause) in enumerate(self.exactly_1_k_sat_formula):
            i = 0
            target = 0
            count = 0
            second_literal = None

            # this loop ensures aux[k], the Quantum auxiliary register to be 1 if an odd number of literals are true
            for literal in clause:
                count += 1
                if literal > 0:
                    self.circuit.cx(self.f_in[literal - 1], self.aux[k])
                else:
                    self.circuit.x(self.f_in[-literal - 1])
                    self.circuit.cx(self.f_in[-literal - 1], self.aux[k])

            self.circuit.barrier()

            for literal in clause:
                qubit_pos = abs(literal)
                if literal == second_literal:
                    continue
                elif literal == clause[0]:
                    second_literal = clause[1]
                    self.circuit.ccx(self.f_in[qubit_pos - 1], self.f_in[abs(second_literal) - 1],
                                     self.aux[num_clauses + target])
                elif literal == clause[len(clause) - 1]:
                    self.circuit.ccx(self.f_in[qubit_pos - 1], self.aux[num_clauses + target - 1], self.aux[k])
                    target -= 2
                else:
                    self.circuit.ccx(self.f_in[qubit_pos - 1], self.aux[num_clauses + target - 1],
                                     self.aux[num_clauses + target])
                target += 1

            for literal in reversed(clause[:len(clause) - 1]):
                qubit_pos = abs(literal)
                if literal == clause[0]:
                    break
                elif literal == second_literal:
                    self.circuit.ccx(self.f_in[abs(clause[0]) - 1], self.f_in[qubit_pos - 1],
                                     self.aux[num_clauses + target])
                else:
                    self.circuit.ccx(self.f_in[qubit_pos - 1], self.aux[num_clauses + target - 1],
                                     self.aux[num_clauses + target])
                target -= 1

            self.circuit.barrier()

            for literal in clause:
                 if literal < 0:
                    self.circuit.x(self.f_in[-literal - 1])

            self.circuit.barrier()
            self.circuit.barrier()

    def __inversion_about_average(self):
        """This methods applies the inversion about the average step of Grover's algorithm"""
        for j in range(self.n):
            self.circuit.h(self.f_in[j])
        for j in range(self.n):
            self.circuit.x(self.f_in[j])
        self.__n_controlled_z([self.f_in[j] for j in range(self.n-1)])
        for j in range(self.n):
            self.circuit.x(self.f_in[j])
        for j in range(self.n):
            self.circuit.h(self.f_in[j])

    def __n_controlled_z(self, controls):
        """This method realizes a C^n-1 Z gate"""
        i = 0
        temp_target = 0
        num_clauses = len(self.exactly_1_k_sat_formula)
        final_target = self.f_in[self.n - 1]
        self.circuit.h(final_target)

        if len(controls) == 1:
            self.circuit.cx(controls[0], final_target)
        elif len(controls) == 2:
            self.circuit.ccx(controls[0], controls[1], final_target)
        else:
            while i < len(controls):
                if i == 0:
                    self.circuit.ccx(controls[0], controls[1], self.aux[num_clauses + temp_target])
                    i += 1
                elif i == len(controls) - 1:
                    self.circuit.ccx(controls[i], self.aux[num_clauses + temp_target - 1], final_target)
                    temp_target -= 2
                else:
                    self.circuit.ccx(controls[i], self.aux[num_clauses + temp_target - 1], self
                                     .aux[num_clauses + temp_target])
                temp_target += 1
                i += 1

            # This backwards while is used to reset the state of all the auxiliary qubits used
            i -= 3
            while i >= 0:
                if i == 0:
                    self.circuit.ccx(controls[0], controls[1], self.aux[num_clauses + temp_target])
                else:
                    self.circuit.ccx(controls[i], self.aux[num_clauses + temp_target - 1], self
                                     .aux[num_clauses + temp_target])
                temp_target -= 1
                i -= 1

        self.circuit.h(final_target)

    def grover(self):
        """Here I apply two iterations of: black_box + average_inversion"""
        self.__input_state()
        self.__black_box_u_f()
        self.__inversion_about_average()
        self.__black_box_u_f()
        self.__inversion_about_average()

    @classmethod
    def from_file(cls, file):
        exactly_1_k_sat_formula = []
        m = 0
        for line in file:
            line = line.strip()
            if len(line) > 0:
                clause = []
                temp = 0
                for literal in line.split():
                    clause.append(int(literal))
                    temp = abs(int(literal))
                exactly_1_k_sat_formula.append(clause)
                m = temp if temp > m else m

        return cls(m, exactly_1_k_sat_formula)

    def solve(self, b):
        if b:
            provider = IBMQ.enable_account('IBMQ_token_HERE')
            backend = provider.get_backend('ibmq_16_melbourne')
        else:
            backend = Aer.get_backend('qasm_simulator')
        return execute(self.circuit, backend)
