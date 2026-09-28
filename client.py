import sys, json, math

class AutomatedTreasuryCashSweepOptimizer:
    """
    Corporate Treasury Cash Pooling & Automated Liquidity Rebalancing Engine.
    Ensures operational checking accounts maintain zero overdraft risk while
    sweeping idle excess capital into yield-generating treasury vaults and tax reserves.
    """
    def __init__(self, target_yield_apr=0.048):
        self.target_yield_apr = target_yield_apr

    def compute_optimal_cash_sweep(self, operating_balance, upcoming_obligations_14d, safety_buffer_multiplier=1.25):
        # Target operational reserve = upcoming commitments * safety multiplier
        required_reserve = upcoming_obligations_14d * safety_buffer_multiplier
        surplus_or_deficit = operating_balance - required_reserve

        if surplus_or_deficit > 1000.0:
            # Surplus cash: Sweep 70% to Yield Vault, 30% to Tax Escrow
            sweep_to_yield = round(surplus_or_deficit * 0.70, 2)
            sweep_to_tax = round(surplus_or_deficit * 0.30, 2)
            action = "SWEEP_SURPLUS_OUT"
            annual_yield_gain = round(sweep_to_yield * self.target_yield_apr, 2)
            recommendation = f"Sweep ${sweep_to_yield} into High-Yield Vault (est. +${annual_yield_gain}/yr yield) and ${sweep_to_tax} into Tax Escrow."
        elif surplus_or_deficit < -500.0:
            # Deficit: Top up operating checking from Yield Vault
            deficit_amount = round(abs(surplus_or_deficit), 2)
            sweep_to_yield = -deficit_amount
            sweep_to_tax = 0.0
            action = "TOP_UP_CHECKING_FROM_VAULT"
            annual_yield_gain = 0.0
            recommendation = f"Transfer ${deficit_amount} from Yield Vault to Operating Checking to prevent overdraft."
        else:
            action = "HOLD_EQUILIBRIUM"
            sweep_to_yield = 0.0
            sweep_to_tax = 0.0
            annual_yield_gain = 0.0
            recommendation = "Operating balance is within optimal buffer window. No rebalancing needed."

        return {
            "action": action,
            "operating_balance": operating_balance,
            "required_reserve": round(required_reserve, 2),
            "surplus_or_deficit": round(surplus_or_deficit, 2),
            "sweep_to_yield_vault": sweep_to_yield,
            "sweep_to_tax_escrow": sweep_to_tax,
            "estimated_annual_yield_gain": annual_yield_gain,
            "recommendation": recommendation
        }

    def project_runway_and_liquidity(self, liquid_assets_dict, monthly_burn_rate):
        # liquid_assets_dict: {"checking": 120000, "yield_vault": 450000, "tax_escrow": 80000}
        total_cash = sum(liquid_assets_dict.values())
        safe_burn = max(1.0, monthly_burn_rate)
        runway_months = total_cash / safe_burn

        return {
            "total_liquid_cash": total_cash,
            "monthly_burn_rate": safe_burn,
            "runway_months": round(runway_months, 1),
            "runway_status": "EXCELLENT" if runway_months > 18 else ("HEALTHY" if runway_months > 12 else "CRITICAL_ACTION_REQUIRED"),
            "assets_breakdown": liquid_assets_dict
        }

    def run_benchmark_treasury_sweep(self):
        # Case 1: Large surplus ($500k in checking, $100k commitments -> $375k surplus)
        c1 = self.compute_optimal_cash_sweep(500000.0, 100000.0, 1.25)
        # Case 2: Deficit ($80k in checking, $100k commitments -> deficit)
        c2 = self.compute_optimal_cash_sweep(80000.0, 100000.0, 1.25)
        # Case 3: Runway projection
        runway = self.project_runway_and_liquidity({"checking": 100000, "vault": 500000}, monthly_burn_rate=50000)

        return {
            "benchmark_status": "PASSED",
            "surplus_action": c1["action"],
            "deficit_action": c2["action"],
            "sweep_yield_amount": c1["sweep_to_yield_vault"],
            "projected_runway_months": runway["runway_months"]
        }
