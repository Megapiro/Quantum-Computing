def run_solver(input_file):
    instance = SATInstance.from_file(input_file)
    clauses = instance.clauses

    partial_result = instance.variables + instance.regCount
    partial_index = 0
    instance.quantumCircuit.barrier()
    instance.quantumCircuit.add_register(
    	QuantumRegister(2 + 2 * (len(clauses) - 2), 'z'))
    instance.quantumCircuit.add_register(
    	QuantumRegister(1, 'f(x_0, x_1, x_2)'))

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