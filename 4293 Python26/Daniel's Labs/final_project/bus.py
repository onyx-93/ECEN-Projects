import json
from pf_solver import newton_raphson

def load_system_data(json_file):
    """
    Load power system data from a JSON file.
    
    Parameters:
        json_file (str): Path to the JSON file containing bus, branch, and baseMVA data.
    
    Returns:
        tuple: (bus_data, branch_data, baseMVA)
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    bus_data = data.get('bus', [])
    branch_data = data.get('branch', [])
    baseMVA = data.get('baseMVA', 100.0)
    
    print(f"Successfully loaded system data from {json_file}")
    print(f"Number of buses: {len(bus_data)}")
    print(f"Number of branches: {len(branch_data)}")
    print(f"Base MVA: {baseMVA}\n")
    
    return bus_data, branch_data, baseMVA


def print_power_flow_results(results, bus_data):
    """
    Print the power flow results in a clean, readable format (similar to MATLAB output).
    """
    print("=" * 60)
    print("          IEEE 9-Bus Newton-Raphson Power Flow Results")
    print("=" * 60)
    
    # Bus voltage results
    print("\nBus Voltages:")
    print("Bus   Vm (p.u.)   Va (deg)")
    print("-" * 30)
    for i in range(len(results['Vm'])):
        bus_num = bus_data[i]['bus_i']
        print(f"{bus_num:3d}   {results['Vm'][i]:.4f}      {results['Va_deg'][i]:.4f}")
    
    # Slack bus power
    slack_bus_idx = next(i for i, bus in enumerate(bus_data) if bus.get('type') == 3)
    # Note: Slack power calculation will be improved once full solver is implemented
    print(f"\nSlack Bus Power (approximate):")
    print(f"Bus {bus_data[slack_bus_idx]['bus_i']}: P = ??? MW, Q = ??? MVAr")
    
    # Convergence info
    print(f"\nConvergence:")
    print(f"Success: {results['success']}")
    print(f"Iterations used: {results['iterations']}")
    print(f"Maximum mismatch: {results['max_mismatch']:.2e}")
    
    print("\n" + "=" * 60)


# ====================== MAIN SECTION ======================
if __name__ == "__main__":
    # Change this filename if you want to use the increased load version later
    json_filename = "ieee9bus_original.json"
    
    # Step 1: Load data from JSON
    bus_data, branch_data, baseMVA = load_system_data(json_filename)
    
    # Step 2: Run Newton-Raphson power flow solver
    print("Running Newton-Raphson Power Flow Solver...\n")
    
    results = newton_raphson(
        bus_data=bus_data,
        branch_data=branch_data,
        baseMVA=baseMVA,
        max_iter=50,
        tol=1e-8,
        damping=0.7
    )
    
    # Step 3: Display results
    print_power_flow_results(results, bus_data)