from jsoperations import json_operations
from buildexecutecircuit import build_and_execute_circuit

# Основная программа
if __name__ == "__main__":
    # Загрузка данных из JSON файла
    load_json, save_json = json_operations()
    Qbits_list = load_json("Qbits_list.json")

    # Построение и выполнение квантовой схемы
    build_and_execute_circuit(Qbits_list)