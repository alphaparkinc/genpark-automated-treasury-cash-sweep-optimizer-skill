import sys, json
from client import AutomatedTreasuryCashSweepOptimizer

def main():
    treasury = AutomatedTreasuryCashSweepOptimizer()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(treasury.run_benchmark_treasury_sweep(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "compute_optimal_cash_sweep", "description": "Calculate idle cash surplus eligible for yield sweeps."},
                        {"name": "project_runway_and_liquidity", "description": "Project company runway from multi-vault assets."},
                        {"name": "run_benchmark_treasury_sweep", "description": "Run corporate treasury benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "compute_optimal_cash_sweep":
                    out = treasury.compute_optimal_cash_sweep(args.get("operating_balance", 0.0), args.get("upcoming_obligations_14d", 0.0), args.get("safety_buffer_multiplier", 1.25))
                elif tname == "project_runway_and_liquidity":
                    out = treasury.project_runway_and_liquidity(args.get("liquid_assets_dict", {}), args.get("monthly_burn_rate", 50000.0))
                elif tname == "run_benchmark_treasury_sweep":
                    out = treasury.run_benchmark_treasury_sweep()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
