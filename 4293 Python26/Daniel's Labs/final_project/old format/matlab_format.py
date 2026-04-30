import numpy as np
from scipy.sparse import lil_matrix


def ybus(bus_data, branch_data, baseMVA):
    """
    Build Ybus using pi-line model.
    Mirrors MATLAB pf_ABOUZAHR.m Ybus construction exactly.
    """
    nb = len(bus_data)

    # Map external bus IDs to 0-based indices
    ext_id = [b['bus_i'] for b in bus_data]
    id_to_idx = {eid: i for i, eid in enumerate(ext_id)}

    r = np.array([br['r'] for br in branch_data], dtype=float)
    x = np.array([br['x'] for br in branch_data], dtype=float)
    b = np.array([br['b'] for br in branch_data], dtype=float)

    z = r + 1j * x
    bad = (~np.isfinite(z)) | (np.abs(z) == 0)
    if np.any(bad):
        print("Warning: Found invalid/zero z=r+jx; adding tiny reactance.")
        z[bad] = 1j * 1e-6

    y_series = 1.0 / z
    y_shunt  = 1j * b / 2.0
    y_shunt[~np.isfinite(y_shunt)] = 0.0

    Ybus = np.zeros((nb, nb), dtype=complex)

    # Series admittance contribution
    for k, branch in enumerate(branch_data):
        i = id_to_idx[branch['fbus']]
        j = id_to_idx[branch['tbus']]
        y = y_series[k]
        Ybus[i, i] += y
        Ybus[j, j] += y
        Ybus[i, j] -= y   # off-diagonal
        Ybus[j, i] -= y   # off-diagonal

    # Shunt admittance (pi model) contribution
    for k, branch in enumerate(branch_data):
        i = id_to_idx[branch['fbus']]
        j = id_to_idx[branch['tbus']]
        ys = y_shunt[k]
        if ys != 0:
            Ybus[i, i] += ys
            Ybus[j, j] += ys

    # Bus shunt (Gs + jBs) / baseMVA
    for bus in bus_data:
        i = id_to_idx[bus['bus_i']]
        Ybus[i, i] += complex(bus.get('Gs', 0.0), bus.get('Bs', 0.0)) / baseMVA

    return Ybus, id_to_idx


def newton_raphson(bus_data, branch_data, baseMVA, max_iter, tol, damping):
    """
    Newton-Raphson power flow solver.
    Analytically assembled Jacobian (H, N, M, L submatrices),
    Levenberg-Marquardt step, and backtracking line search.
    """
    nb = len(bus_data)

    Ybus, id_to_idx = ybus(bus_data, branch_data, baseMVA)
    G = np.real(Ybus)
    B = np.imag(Ybus)

    # Bus type indices (0-based)
    bus_types = np.array([bus.get('type', 1) for bus in bus_data])
    slk = np.where(bus_types == 3)[0]
    pv  = np.where(bus_types == 2)[0]
    pq  = np.where(bus_types == 1)[0]
    idx_Va = np.concatenate([pv, pq])   # buses where Va is a variable
    idx_Vm = pq                          # buses where Vm is a variable

    # Specified net power injections (p.u.)
    P_spec = np.array([(bus.get('Pg', 0.0) - bus.get('Pd', 0.0)) / baseMVA
                       for bus in bus_data])
    Q_spec = np.array([(bus.get('Qg', 0.0) - bus.get('Qd', 0.0)) / baseMVA
                       for bus in bus_data])

    # Initial voltage vector
    Vm0 = np.array([bus.get('Vm', 1.0)             for bus in bus_data], dtype=float)
    Va0 = np.array([np.deg2rad(bus.get('Va', 0.0)) for bus in bus_data], dtype=float)
    V   = Vm0 * np.exp(1j * Va0)

    success    = False
    iterations = 0

    print("Starting Newton-Raphson...")

    for it in range(max_iter):
        Vm = np.abs(V)
        Va = np.angle(V)

        # ── Power mismatch ──────────────────────────────────────────────
        I_calc = Ybus @ V
        S_calc = V * np.conj(I_calc)
        dP = P_spec - np.real(S_calc)
        dQ = Q_spec - np.imag(S_calc)
        F  = np.concatenate([dP[idx_Va], dQ[idx_Vm]])

        max_err = np.max(np.abs(F))
        print(f"Iteration {it+1}: Max Mismatch = {max_err:.2e}")
        iterations = it + 1

        if max_err < tol:
            print("Converged!")
            success = True
            break

        # ── Analytical Jacobian (H, N, M, L) ───────────────────────────
        # Matches MATLAB submatrix construction exactly.
        H = np.zeros((nb, nb))
        N = np.zeros((nb, nb))
        M = np.zeros((nb, nb))
        L = np.zeros((nb, nb))

        for i in range(nb):
            # Diagonal seed (self-admittance terms)
            H[i, i] = -(Vm[i] ** 2) * B[i, i]
            M[i, i] =  (Vm[i] ** 2) * G[i, i]

            for k in range(nb):
                if k == i:
                    continue
                theta = Va[i] - Va[k]
                Gik   = G[i, k]
                Bik   = B[i, k]
                cs    = np.cos(theta)
                sn    = np.sin(theta)

                # Off-diagonal elements
                H[i, k] =  Vm[i] * Vm[k] * ( Gik * sn - Bik * cs)   # dP_i / dVa_k
                N[i, k] =  Vm[i]          * ( Gik * cs + Bik * sn)   # dP_i / dVm_k
                M[i, k] = -Vm[i] * Vm[k] * ( Gik * cs + Bik * sn)   # dQ_i / dVa_k
                L[i, k] =  Vm[i]          * ( Gik * sn - Bik * cs)   # dQ_i / dVm_k

                # Diagonal accumulation
                H[i, i] -= Vm[i] * Vm[k] * ( Gik * sn - Bik * cs)
                M[i, i] -= Vm[i] * Vm[k] * (-Gik * cs - Bik * sn)
                N[i, i] += Vm[k]          * ( Gik * cs + Bik * sn)
                L[i, i] += Vm[k]          * ( Gik * sn - Bik * cs)

        # Assemble reduced Jacobian for non-slack unknowns
        J = np.block([
            [H[np.ix_(idx_Va, idx_Va)], N[np.ix_(idx_Va, idx_Vm)]],
            [M[np.ix_(idx_Vm, idx_Va)], L[np.ix_(idx_Vm, idx_Vm)]]
        ])

        # ── Levenberg-Marquardt step ────────────────────────────────────
        # Matches MATLAB:  A = J'J + λI;  dx = A \ J'F
        diag_J = np.diag(J)
        lam    = 1e-8 * (np.max(np.abs(diag_J)) ** 2 + np.finfo(float).eps)
        A    = J.T @ J + lam * np.eye(J.shape[1])
        bvec = J.T @ F
        dx   = np.linalg.solve(A, bvec)

        n_Va  = len(idx_Va)
        dVa   = damping * dx[:n_Va]
        dVm   = damping * dx[n_Va:]

        # ── Backtracking line search (8 halvings) ──────────────────────
        Va_cur = np.angle(V).copy()
        Vm_cur = np.abs(V).copy()
        best_V    = V.copy()
        best_norm = np.max(np.abs(F))
        step = 1.0

        for _ in range(8):
            Va_try = Va_cur.copy()
            Vm_try = Vm_cur.copy()
            Va_try[idx_Va] = Va_cur[idx_Va] + step * dVa
            Vm_try[idx_Vm] = Vm_cur[idx_Vm] + step * dVm

            # PV buses: hold Vm at scheduled value
            Vm_try[pv] = Vm0[pv]

            V_try = Vm_try * np.exp(1j * Va_try)

            # Slack bus: hold V fixed at flat-start value
            V_try[slk] = Vm0[slk] * np.exp(1j * Va0[slk])

            I_try  = Ybus @ V_try
            S_try  = V_try * np.conj(I_try)
            mis_try = np.concatenate([
                (P_spec - np.real(S_try))[idx_Va],
                (Q_spec - np.imag(S_try))[idx_Vm]
            ])

            if not np.all(np.isfinite(mis_try)):
                step *= 0.5
                continue

            if np.max(np.abs(mis_try)) < best_norm:
                best_norm = np.max(np.abs(mis_try))
                best_V    = V_try.copy()
                break
            else:
                step *= 0.5

        V = best_V

    if not success:
        print(f"Did not converge within {max_iter} iterations.")

    # ── Final power flow quantities ─────────────────────────────────────
    final_Vm = np.abs(V)
    final_Va = np.angle(V)

    I_final = Ybus @ V
    S_final = V * np.conj(I_final)
    P_inj   = np.real(S_final) * baseMVA
    Q_inj   = np.imag(S_final) * baseMVA

    slack_idx   = int(slk[0])
    slackP_MW   = P_inj[slack_idx]
    slackQ_MVAr = Q_inj[slack_idx]

    # Branch flows (matches MATLAB branch_flow loop)
    r_arr = np.array([br['r'] for br in branch_data], dtype=float)
    x_arr = np.array([br['x'] for br in branch_data], dtype=float)
    b_arr = np.array([br['b'] for br in branch_data], dtype=float)

    branch_flow = []
    for k, branch in enumerate(branch_data):
        i = id_to_idx[branch['fbus']]
        j = id_to_idx[branch['tbus']]
        z_k = complex(r_arr[k], x_arr[k])
        if abs(z_k) < 1e-10:
            z_k = 1j * 1e-6
        y_ser  = 1.0 / z_k
        b_half = 1j * b_arr[k] / 2.0

        Vf = V[i]; Vt = V[j]
        Iij = (Vf - Vt) * y_ser + Vf * b_half
        Iji = (Vt - Vf) * y_ser + Vt * b_half
        Sij = Vf * np.conj(Iij)
        Sji = Vt * np.conj(Iji)

        Pij = np.real(Sij) * baseMVA
        Qij = np.imag(Sij) * baseMVA
        Pji = np.real(Sji) * baseMVA
        Qji = np.imag(Sji) * baseMVA
        Ploss = Pij + Pji

        branch_flow.append([branch['fbus'], branch['tbus'],
                            Pij, Qij, Pji, Qji, Ploss])

    Ploss_total = sum(row[6] for row in branch_flow)

    return {
        'Vm':             final_Vm,
        'Va_deg':         np.rad2deg(final_Va),
        'success':        success,
        'iterations':     iterations,
        'max_mismatch':   float(np.max(np.abs(F))) if not success else float(tol),
        'P_inj_MW':       P_inj,
        'Q_inj_MVAr':     Q_inj,
        'slackP_MW':      slackP_MW,
        'slackQ_MVAr':    slackQ_MVAr,
        'Ploss_total_MW': Ploss_total,
        'branch_flow':    branch_flow,
    }