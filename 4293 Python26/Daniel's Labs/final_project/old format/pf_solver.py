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
    Standard Newton-Raphson power flow solver.
    Solves J * dx = F directly without Levenberg-Marquardt or Line Search.
    """
    nb = len(bus_data)
    Ybus, id_to_idx = ybus(bus_data, branch_data, baseMVA)
    G = np.real(Ybus)
    B = np.imag(Ybus)

    # Bus type indices (0-based)
    bus_types = np.array([bus.get('type', 1) for bus in bus_data])
    slk = np.where(bus_types == 3)[0]
    pv = np.where(bus_types == 2)[0]
    pq = np.where(bus_types == 1)[0]

    idx_Va = np.concatenate([pv, pq]) # Unknown Angles (PV + PQ)
    idx_Vm = pq                       # Unknown Magnitudes (PQ only)

    # Specified net power injections (p.u.)
    P_spec = np.array([(bus.get('Pg', 0.0) - bus.get('Pd', 0.0)) / baseMVA for bus in bus_data])
    Q_spec = np.array([(bus.get('Qg', 0.0) - bus.get('Qd', 0.0)) / baseMVA for bus in bus_data])

    # Initial voltage vector
    Vm0 = np.array([bus.get('Vm', 1.0) for bus in bus_data], dtype=float)
    Va0 = np.array([np.deg2rad(bus.get('Va', 0.0)) for bus in bus_data], dtype=float)
    V = Vm0 * np.exp(1j * Va0)

    success = False
    iterations = 0
    print("Starting Direct Newton-Raphson...")

    for it in range(max_iter):
        Vm = np.abs(V)
        Va = np.angle(V)

        # ── Power mismatch ──────────────────────────────────────────────
        I_calc = Ybus @ V
        S_calc = V * np.conj(I_calc)
        
        dP = P_spec - np.real(S_calc)
        dQ = Q_spec - np.imag(S_calc)
        
        # F = [dP (PV+PQ), dQ (PQ)]
        F = np.concatenate([dP[idx_Va], dQ[idx_Vm]])
        
        max_err = np.max(np.abs(F))
        print(f"Iteration {it+1}: Max Mismatch = {max_err:.2e}")
        iterations = it + 1

        if max_err < tol:
            print("Converged!")
            success = True
            break

        # ── Analytical Jacobian (H, N, M, L) ───────────────────────────
        # ── Optimized Jacobian Construction ────────────────────────────
        H = np.zeros((nb, nb))
        N = np.zeros((nb, nb))
        M = np.zeros((nb, nb))
        L = np.zeros((nb, nb))

        # Pre-calculate Power at every bus for the diagonal terms
        P_calc_i = np.real(S_calc)
        Q_calc_i = np.imag(S_calc)

        for i in range(nb):
            # --- Off-Diagonal Terms (k != i) ---
            for k in range(nb):
                if k == i: continue
                theta = Va[i] - Va[k]
                Gik = G[i, k]
                Bik = B[i, k]
                
                # Common Terms
                a = Gik * np.sin(theta) - Bik * np.cos(theta)
                b = Gik * np.cos(theta) + Bik * np.sin(theta)
                
                H[i, k] = Vm[i] * Vm[k] * a
                N[i, k] = Vm[i] * b
                M[i, k] = -Vm[i] * Vm[k] * b
                L[i, k] = Vm[i] * a

            # --- Diagonal Terms (k == i) ---
            # Uses exact power balance equations: avoids loop summation errors
            H[i, i] = -Q_calc_i[i] - (B[i, i] * Vm[i]**2)
            N[i, i] = P_calc_i[i] + (G[i, i] * Vm[i]**2)
            M[i, i] = P_calc_i[i] - (G[i, i] * Vm[i]**2)
            L[i, i] = Q_calc_i[i] - (B[i, i] * Vm[i]**2)

        # Assemble reduced Jacobian
        J = np.block([
            [H[np.ix_(idx_Va, idx_Va)], N[np.ix_(idx_Va, idx_Vm)]],
            [M[np.ix_(idx_Vm, idx_Va)], L[np.ix_(idx_Vm, idx_Vm)]]
        ])

        # ── Direct Newton Step (J * dx = F) ─────────────────────────────
        try:
            dx = np.linalg.solve(J, F)
        except np.linalg.LinAlgError:
            print("Singular Jacobian encountered. Solver failed.")
            break

        # ── Update State ────────────────────────────────────────────────
        n_Va = len(idx_Va)
        dVa = damping * dx[:n_Va]
        dVm = damping * dx[n_Va:]

        # Apply updates to the temporary arrays
        Va[idx_Va] += dVa
        Vm[idx_Vm] += dVm
        
        # Strict Enforcement: Reset PV and Slack Magnitudes to scheduled values
        Vm[pv] = Vm0[pv]
        Vm[slk] = Vm0[slk]
        Va[slk] = Va0[slk]

        # Reconstruct complex voltage for next iteration
        V = Vm * np.exp(1j * Va)

    if not success:
        print(f"Did not converge within {max_iter} iterations.")

    # ── Final Results Calculation ──────────────────────────────────────
    # (Same as before)
    final_Vm = np.abs(V)
    final_Va = np.angle(V)
    I_final = Ybus @ V
    S_final = V * np.conj(I_final)
    P_inj = np.real(S_final) * baseMVA
    Q_inj = np.imag(S_final) * baseMVA
    
    slack_idx = int(slk[0])
    slackP_MW = P_inj[slack_idx]
    slackQ_MVAr = Q_inj[slack_idx]

    r_arr = np.array([br['r'] for br in branch_data], dtype=float)
    x_arr = np.array([br['x'] for br in branch_data], dtype=float)
    b_arr = np.array([br['b'] for br in branch_data], dtype=float)
    
    branch_flow = []
    for k, branch in enumerate(branch_data):
        i = id_to_idx[branch['fbus']]
        j = id_to_idx[branch['tbus']]
        z_k = complex(r_arr[k], x_arr[k])
        if abs(z_k) < 1e-10: z_k = 1j*1e-6
        
        y_ser = 1.0 / z_k
        b_half = 1j * b_arr[k] / 2.0
        
        Vf = V[i]; Vt = V[j]
        Iij = (Vf - Vt) * y_ser + Vf * b_half
        Iji = (Vt - Vf) * y_ser + Vt * b_half
        Sij = Vf * np.conj(Iij)
        Sji = Vt * np.conj(Iji)
        
        Pij = np.real(Sij) * baseMVA; Qij = np.imag(Sij) * baseMVA
        Pji = np.real(Sji) * baseMVA; Qji = np.imag(Sji) * baseMVA
        Ploss = Pij + Pji
        branch_flow.append([branch['fbus'], branch['tbus'], Pij, Qij, Pji, Qji, Ploss])

    Ploss_total = sum(row[6] for row in branch_flow)

    return {
        'Vm': final_Vm,
        'Va_deg': np.rad2deg(final_Va),
        'success': success,
        'iterations': iterations,
        'max_mismatch': float(max_err),
        'P_inj_MW': P_inj,
        'Q_inj_MVAr': Q_inj,
        'slackP_MW': slackP_MW,
        'slackQ_MVAr': slackQ_MVAr,
        'Ploss_total_MW': Ploss_total,
        'branch_flow': branch_flow,
    }
