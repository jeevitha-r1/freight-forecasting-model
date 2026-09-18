"""
What-If Engine Service — Isolated scenario simulations preventing baseline object mutation.
"""

import copy
from typing import Any, Callable, List
from backend.models.decision_models import (
    DecisionEnum,
    RiskEvaluation,
    VoyageProposalModel,
    WhatIfScenarioRequest,
    WhatIfScenarioResult,
)

ALLOWED_WHAT_IF_FIELDS = {
    "cargo_quantity_mt": ("cargo", "quantity_mt"),
    "vessel_capacity_dwt": ("vessel", "capacity_dwt"),
    "vessel_draft_m": ("vessel", "draft_m"),
    "port_max_draft_m": ("port", "max_draft_m"),
    "schedule_margin_days": ("schedule_margin_days", None),
}


class WhatIfEngine:
    """Executes controlled scenario simulations against isolated deep copies of proposal objects."""

    def __init__(self, evaluation_callback: Callable):
        self.evaluation_callback = evaluation_callback

    def run_scenario(
        self,
        baseline_proposal: VoyageProposalModel,
        baseline_decision: DecisionEnum,
        baseline_risk: RiskEvaluation,
        scenario: WhatIfScenarioRequest,
    ) -> WhatIfScenarioResult:
        # 1. Parameter Validation against explicit allowlist
        for param in scenario.overrides.keys():
            if param not in ALLOWED_WHAT_IF_FIELDS:
                raise ValueError(
                    f"Invalid what-if parameter '{param}'. Allowed parameters: {list(ALLOWED_WHAT_IF_FIELDS.keys())}"
                )

        # 2. Deep-copy baseline to preserve original state
        cloned_proposal = copy.deepcopy(baseline_proposal)

        # 3. Apply overrides to cloned copy
        for param, val in scenario.overrides.items():
            if val is None or (isinstance(val, (int, float)) and val < 0):
                raise ValueError(f"Invalid value '{val}' for parameter '{param}'. Must be non-negative.")

            target, subfield = ALLOWED_WHAT_IF_FIELDS[param]
            if target == "schedule_margin_days":
                setattr(cloned_proposal, "schedule_margin_days", float(val))
            elif target == "cargo":
                setattr(cloned_proposal.cargo, subfield, float(val))
            elif target == "vessel":
                setattr(cloned_proposal.vessel, subfield, float(val))
            elif target == "port":
                setattr(cloned_proposal.port, subfield, float(val))

        # 4. Evaluate simulated scenario
        simulated_response = self.evaluation_callback(cloned_proposal, scenarios=None)

        decision_changed = simulated_response.decision != baseline_decision
        risk_changed = (simulated_response.risk.level != baseline_risk.level) or (
            simulated_response.risk.score != baseline_risk.score
        )

        triggered_factors = [f.factor for f in simulated_response.risk.factors]

        explanation = (
            f"Scenario '{scenario.scenario_id}': Decision changed from {baseline_decision.value} to {simulated_response.decision.value}. "
            f"Risk score shifted from {baseline_risk.score} ({baseline_risk.level.value}) to {simulated_response.risk.score} ({simulated_response.risk.level.value})."
        )

        return WhatIfScenarioResult(
            scenario_id=scenario.scenario_id,
            modified_parameters=scenario.overrides,
            decision=simulated_response.decision,
            feasibility_status=simulated_response.feasibility_status,
            risk_level=simulated_response.risk.level,
            risk_score=simulated_response.risk.score,
            decision_changed=decision_changed,
            risk_changed=risk_changed,
            triggered_factors=triggered_factors,
            explanation=explanation,
        )