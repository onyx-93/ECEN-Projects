import numpy as np

def ybus(bus_data, branch_data, baseMVA=100.0):
    """
    Build the bus admittance matrix (Ybus) using the pi-model for lines.
    
    Parameters:
        bus_data (list of dict): Bus information from JSON
        branch_data (list of dict): Branch (line) information from JSON
        baseMVA (float): System base power (default 100 MVA)
    
    Returns:
        Ybus (numpy.ndarray, complex): Bus admittance matrix
    """
    # Find number of buses (assuming bus_i starts from 1)
    num_buses = max(bus['bus_i'] for bus in bus_data)
    
    # Initialize Ybus as complex matrix
    Ybus = np.zeros((num_buses, num_buses), dtype=complex)
    
    # Add series and shunt contributions from branches
    for branch in branch_data:
        f = branch['fbus'] - 1   # Convert to 0-based index
        t = branch['tbus'] - 1
        r = branch['r']
        x = branch['x']
        b = branch['b']
        
        z = complex(r, x)
        if abs(z) < 1e-10:          # Avoid division by zero
            z = 1j * 1e-6
        y_series = 1.0 / z
        y_shunt = 1j * b / 2.0      # Half shunt at each end
        
        # Update Ybus
        Ybus[f, f] += y_series + y_shunt
        Ybus[t, t] += y_series + y_shunt
        Ybus[f, t] -= y_series
        Ybus[t, f] -= y_series
    
    # Add bus shunts (Gs + jBs) if present
    for bus in bus_data:
        i = bus['bus_i'] - 1
        Gs = bus.get('Gs', 0.0) / baseMVA
        Bs = bus.get('Bs', 0.0) / baseMVA
        Ybus[i, i] += complex(Gs, Bs)
    
    return Ybus

def jacobian(V, Ybus, bus_type):
    """
    Compute the Jacobian matrix for the Newton-Raphson power flow.
    
    Parameters:
        V (numpy.ndarray, complex): Voltage vector (Vm * exp(j*Va))
        Ybus (numpy.ndarray, complex): Bus admittance matrix
        bus_type (numpy.ndarray, int): Bus type vector (1=PQ, 2=PV, 3=slack)

    Returns:
        J (numpy.ndarray, float): Jacobian matrix
    """
    # Diagonal elements for J1, J2, J3, J4 k = n
    # J1 = 
    
    
    # Placeholder - this will be replaced with actual Jacobian computation
    pass


def newton_raphson(bus_data, branch_data, baseMVA=100.0, max_iter=50, tol=1e-8, damping=0.7):
    """
    Solve power flow using Newton-Raphson method.
    
    Parameters:
        bus_data (list of dict): Bus data from JSON
        branch_data (list of dict): Branch data from JSON
        baseMVA (float): System base
        max_iter (int): Maximum iterations
        tol (float): Convergence tolerance
        damping (float): Damping factor for stability (0 < damping <= 1)
    
    Returns:
        dict: Results containing Vm, Va, success flag, iterations, etc.
    """
    num_buses = max(bus['bus_i'] for bus in bus_data)
    
    # Build Ybus
    Ybus = ybus(bus_data, branch_data, baseMVA)
    
    # Initialize voltage vector (complex) using Vm and Va from bus_data
    V = np.zeros(num_buses, dtype=complex)
    for bus in bus_data:
        i = bus['bus_i'] - 1
        vm = bus.get('Vm', 1.0)
        va_deg = bus.get('Va', 0.0)
        V[i] = vm * np.exp(1j * np.deg2rad(va_deg))
    
    # Identify bus types
    bus_type = np.zeros(num_buses, dtype=int)
    for bus in bus_data:
        i = bus['bus_i'] - 1
        bus_type[i] = bus.get('type', 1)   # default to PQ
    
    slack = np.where(bus_type == 3)[0]
    pv    = np.where(bus_type == 2)[0]
    pq    = np.where(bus_type == 1)[0]
    
    if len(slack) == 0:
        raise ValueError("No slack bus found in the system.")
    
    print(f"Starting Newton-Raphson solver - Slack bus: {slack[0]+1}")
    
    # Main Newton-Raphson iteration
    for iter_count in range(max_iter):
        # Step 1: Compute current injections and calculated power
        I = Ybus @ V
        S_calc = V * np.conj(I)          # Calculated complex power in p.u.
        
        # Step 2: Compute specified power injection (S_spec = (Pg - Pd) + j(Qg - Qd))
        S_spec = np.zeros(num_buses, dtype=complex)
        for bus in bus_data:
            i = bus['bus_i'] - 1
            Pd = bus.get('Pd', 0.0) / baseMVA
            Qd = bus.get('Qd', 0.0) / baseMVA
            Pg = bus.get('Pg', 0.0) / baseMVA
            Qg = bus.get('Qg', 0.0) / baseMVA
            S_spec[i] = complex(Pg - Pd, Qg - Qd)
        
        # Step 3: Power mismatch
        mismatch = S_spec - S_calc
        dP = np.real(mismatch)
        dQ = np.imag(mismatch)
        
        # Form mismatch vector F (only for unknown variables)
        F = np.concatenate((dP[np.concatenate((pv, pq))], dQ[pq]))
        
        # Check convergence
        max_mismatch = np.max(np.abs(F))
        print(f"Iteration {iter_count+1:2d} | Max mismatch = {max_mismatch:.2e}")
        
        if max_mismatch < tol:
            print("Converged successfully!")
            break
        
        # TODO: Build Jacobian matrix J here (J1, J2, J3, J4 submatrices)
        J = jacobian(V, Ybus, bus_type)
        
        
        # TODO: Solve J * dx = -F for corrections dVa and dVm       
        # TODO: Apply damping + line search (optional but recommended)
        # TODO: Update V vector (fix slack and PV magnitudes)
        
        # Placeholder - this will be replaced with actual Jacobian solve
        # For now, we just continue to show the structure
        pass
    
    else:
        print("Warning: Maximum iterations reached without full convergence.")
    
    # Final results
    Vm = np.abs(V)
    Va_deg = np.rad2deg(np.angle(V))
    
    return {
        'success': max_mismatch < tol,
        'iterations': iter_count + 1,
        'Vm': Vm,
        'Va_deg': Va_deg,
        'Ybus': Ybus,
        'max_mismatch': max_mismatch,
        'V_complex': V
    }