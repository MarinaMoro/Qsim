def gate_functions():

    from qiskit import QuantumCircuit
    from qiskit.circuit.library import MCMT

    def h(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.h(i["target"])
            else:
                if len(i["control"]) == 1:
                    qc.ch(i["control"], i["target"])
                elif len(i["control"]) >= 2:
                    qc.append(MCMT("h", len(i["control"]), 1), i["control"] + [i["target"]])

    def x(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.x(i["target"])
            else:
                if len(i["control"]) == 1:
                    qc.cx(i["control"], i["target"])
                elif len(i["control"]) == 2:
                    qc.ccx(i["control"][0], i["control"][1], i["target"])
                else:
                    qc.mcx(i["control"], i["target"])

    def y(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.y(i["target"])
            else:
                if len(i["control"]) == 1:
                    qc.cy(i["control"], i["target"])
                elif len(i["control"]) >= 2:
                    qc.append(MCMT("y", len(i["control"]), 1), i["control"] + [i["target"]])

    def z(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.z(i["target"])
            else:
                if len(i["control"]) == 1:
                    qc.cz(i["control"], i["target"])
                elif len(i["control"]) == 2:
                    qc.ccz(i["control"][0], i["control"][1], i["target"])
                elif len(i["control"]) >= 3:
                    qc.append(MCMT("z", len(i["control"]), 1), i["control"] + [i["target"]])

    def s(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.s(i["target"])
            else:
                qc.append(MCMT("s", len(i["control"]), 1), i["control"] + [i["target"]])

    def t(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.t(i["target"])
            else:
                qc.append(MCMT("t", len(i["control"]), 1), i["control"] + [i["target"]])

    def rx(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.rx(i["rotation"], i["target"])
            else:
                if len(i["control"]) == 1:
                    qc.crx(i["rotation"], i["control"], i["target"])

    def ry(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.ry(i["rotation"], i["target"])
            else:
                if len(i["control"]) == 1:
                    qc.cry(i["rotation"], i["control"], i["target"])

    def rz(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.rz(i["rotation"], i["target"])
            else:
                if len(i["control"]) == 1:
                    qc.crz(i["rotation"], i["control"], i["target"])

    def u(qb, qc):
        for i in qb:
            if "control" not in i:
                qc.u(i["rotation"][0], i["rotation"][1], i["rotation"][2], i["target"])
            else:
                if len(i["control"]) == 1:
                    qc.cu(i["rotation"][0], i["rotation"][1], i["rotation"][2], i["phase"], i["control"], i["target"])

    def meas(qb, qc):
        for i in qb:
            qc.measure(i["control"], i["control"])

    def bar(qb, qc):
        for i in qb:
            qc.barrier(i["control"])
    def initialize(qb, qc):
        for i in qb:
            if i["target"] == 0:
                state = [1, 0]  # Это состояние |0⟩
                for m in i["control"]:
                    try: qc.initialize(state, m)
                    except AttributeError: pass
            if i["target"] == 1:
                state = [0, 1]  # Это состояние |1⟩
                for m in i["control"]:
                    try: qc.initialize(state, m)
                    except AttributeError: pass

    # def stvec(qb, qc):
    #         qc.save_statevector()
    #         result = backend.run(transpile(qc, backend), shots=Qbits_list["shots"]).result()
    #         print(result.get_statevector(qc))

    func_dict = {
        "h": h, "x": x, "y": y, "z": z, "rx": rx, "ry": ry, "rz": rz,
        "s": s, "t": t, "u": u, "Measure": meas, "barrier": bar, "initialize": initialize #, "stvec": stvec
    }

    return func_dict
