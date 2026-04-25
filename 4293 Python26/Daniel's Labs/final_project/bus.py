import json
import argparse
from pf_solver import newton_raphson


def load_system_data(json_file):
    """
    Load power system data from JSON and merge generators into bus_data
    so the solver only needs bus_data + branch_data.
    """
    with open(json_file, 'r') as f:
        data = json.load(f)

    bus_data = data.get('bus', [])
    branch_data = data.get('branch', [])
    gen_data = data.get('gen', [])
    baseMVA = data.get('baseMVA', 100.0)

    # Merge generator data into buses (so solver sees Pg/Qg on the bus)
    for g in gen_data:
        bus_id = g['bus']
        for b in bus_data:
            if b['bus_i'] == bus_id:
                b['Pg'] = g.get('Pg', 0.0)
                b['Qg'] = g.get('Qg', 0.0)
                break

    print(f"Successfully loaded system data from {json_file}")
    print(f"Number of buses: {len(bus_data)}")
    print(f"Number of branches: {len(branch_data)}")
    print(f"Number of generators: {len(gen_data)}")
    print(f"Base MVA: {baseMVA}\n")

    return bus_data, branch_data, baseMVA


def print_power_flow_results(results, bus_data):
    """Print results in a clear and organized manner."""
    print("=" * 60)
    print("          IEEE 9-Bus Newton-Raphson Power Flow Results")
    print("=" * 60)

    print("\nBus Voltages:")
    print("Bus   Vm (p.u.)   Va (deg)")
    print("-" * 30)
    for i, bus in enumerate(bus_data):
        print(f"{bus['bus_i']:3d}   {results['Vm'][i]:.4f}      {results['Va_deg'][i]:.4f}")

    print(f"\nSlack Bus Power:")
    print(f"Bus {next(b['bus_i'] for b in bus_data if b.get('type') == 3)}: "
          f"P = {results['slackP_MW']:.3f} MW, Q = {results['slackQ_MVAr']:.3f} MVAr")

    print(f"\nTotal loss = {results['Ploss_total_MW']:.3f} MW")

    print("\nBranch Power Flows:")
    print("    From      To       Pij       Qij       Pji       Qji      Ploss(MW)")
    for row in results['branch_flow']:
        print(f"{int(row[0]):8d} {int(row[1]):8d} {row[2]:9.4f} {row[3]:9.4f} "
              f"{row[4]:9.4f} {row[5]:9.4f} {row[6]:9.4f}")

    print(f"\nConvergence:")
    print(f"Success: {results['success']}")
    print(f"Iterations used: {results['iterations']}")
    print(f"Maximum mismatch: {results['max_mismatch']:.2e}")
    print("=" * 60)


# ====================== MAIN ======================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IEEE 9-Bus Newton-Raphson Power Flow")
    parser.add_argument("--preset", "-p", type=str, default="input_source.json",
                        help="Path to JSON preset file (default: input_source.json)")
    args = parser.parse_args()

    bus_data, branch_data, baseMVA = load_system_data(args.preset)

    print("Running Newton-Raphson Power Flow Solver...\n")

    # Run the power flow solver and get results
    results = newton_raphson(
        bus_data=bus_data,
        branch_data=branch_data,
        baseMVA=baseMVA,
        max_iter=50,
        tol=1e-4,
        damping=0.7
    )

    print_power_flow_results(results, bus_data)