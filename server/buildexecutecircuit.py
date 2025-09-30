def build_and_execute_circuit(Qbits_list):

    from qiskit import Aer, transpile
    from qiskit.visualization import plot_histogram
    import matplotlib
    import matplotlib.pyplot as plt

    from qgate import gate_functions
    from createqcirc import create_quantum_circuit
    from jsoperations import json_operations

    matplotlib.use('TkAgg')
    backend = Aer.get_backend('aer_simulator')
    func_dict = gate_functions()

    # Создаем квантовую схему
    QC = create_quantum_circuit(Qbits_list["qNum"])
    system_check = True

    # Проверка на корректность операции и добавление гейтов
    for gate in Qbits_list["gates"]:
        if gate["operation"] in func_dict:
            func_dict[gate["operation"]](gate["qbits"], QC)
        else:
            system_check = False
            print(f"Ошибка: Операция {gate['operation']} не поддерживается.")
            break

    if system_check:
        # Выполнение схемы и получение результата
        result = backend.run(transpile(QC, backend), shots=Qbits_list["shots"]).result()
        counts = result.get_counts(QC)

        # Сохраняем результат в JSON и выводим
        load_json, save_json = json_operations()
        save_json(counts, "Qbits_result.json")
        plot_histogram(counts)
        QC.draw('mpl')
        plt.show()
    else:
        # Сообщение об ошибке
        error_message = "ALARM, code 1"
        load_json, save_json = json_operations()
        save_json(error_message, "Qbits_result.json")
        print(error_message)