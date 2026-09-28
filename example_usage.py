import sys, json
from client import AutomatedTreasuryCashSweepOptimizer

def main():
    print("Testing AutomatedTreasuryCashSweepOptimizer...")
    treasury = AutomatedTreasuryCashSweepOptimizer()
    res = treasury.run_benchmark_treasury_sweep()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["surplus_action"] == "SWEEP_SURPLUS_OUT"
    assert res["deficit_action"] == "TOP_UP_CHECKING_FROM_VAULT"
    assert res["projected_runway_months"] == 12.0
    print("All Automated Treasury Cash Sweep Optimizer tests passed successfully!")

if __name__ == "__main__":
    main()
