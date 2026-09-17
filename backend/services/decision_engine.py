"""
Decision Engine Service — Pipeline orchestrator providing explainable decision traces.
"""

from typing import Dict, List, Optional
from backend.config.decision_config import DEFAULT_DECISION_CONFIG, DecisionConfig
from backend.models.decision_models import (
    DecisionEnum,
    DecisionEvaluationResponse,
    DecisionTraceStep,
    FeasibilityStatusEnum,
    RiskLevelEnum,
    VoyageProposalModel,
    WhatIfScenarioRequest,
    WhatIfScenarioResult,
)
from backend.services.cargo_allocator import CargoAllocator
from backend.services.compatibility import CompatibilityEngine
from backend.services.constraint_engine import ConstraintEngine
from backend.services.risk_engine import RiskEngine
from backend.services.route_optimizer import RouteOptimizer
from backend.services.what_if_engine import WhatIfEngine


class DecisionEngine:
    """Orchestrates pipeline services and produces explainable decision traces."""

    def __init__(self, config: DecisionConfig = DEFAULT_DECISION_CONFIG):
        self.config = config

    def evaluate_proposal(
        self, proposal: VoyageProposalModel, scenarios: Optional[List[WhatIfScenarioRequest]] = None
    ) -> DecisionEvaluationResponse:
        decision_trace: List[DecisionTraceStep] = []
        reasons: List[str] = []
        warnings: List[str] = []

        # Step 1: Compatibility
        compatibility = CompatibilityEngine.evaluate(proposal)
        decision_trace.append(
            DecisionTraceStep(
                stage="compatibility",
                status="PASS" if compatibility.compatible else "FAIL",
                details="All pair-wise entity compatibility checks passed." if compatibility.compatible else "Entity compatibility failure detected.",
            )
        )

        # Step 2: Hard Constraints
        constraints = ConstraintEngine.evaluate(proposal)
        decision_trace.append(
            DecisionTraceStep(
                stage="constraints",
                status="PASS" if constraints.feasible else "FAIL",
                details="Hard operational constraints satisfied." if constraints.feasible else f"Hard constraint violations: {', '.join(constraints.violations)}",
            )
        )

        # Step 3: Cargo Allocation
        allocation = CargoAllocator.allocate(proposal)
        decision_trace.append(
            DecisionTraceStep(
                stage="allocation",
                status="PASS" if not allocation.over_capacity else "OVER_CAPACITY",
                details=f"Utilization ratio: {allocation.utilization_ratio:.1%}, Unallocated: {allocation.unallocated_mt} MT.",
            )
        )

        # Step 4: Route Evaluation
        route = RouteOptimizer.evaluate_route(proposal, self.config)
        decision_trace.append(
            DecisionTraceStep(
                stage="route",
                status="PASS" if route.sufficient_buffer else "REVIEW",
                details=route.details,
            )
        )

        # Step 5: Risk Evaluation
        risk = RiskEngine.evaluate(proposal, self.config)
        decision_trace.append(
            DecisionTraceStep(
                stage="risk",
                status=risk.level.value,
                details=f"Calculated risk score: {risk.score} ({risk.level.value}). Triggered factors: {len(risk.factors)}.",
            )
        )

        # Step 6: Resolve Decision Classification (PROCEED / REVIEW / REJECT)
        if not constraints.feasible or not compatibility.compatible:
            decision = DecisionEnum.REJECT
            feasibility_status = FeasibilityStatusEnum.INFEASIBLE
            for check in constraints.checks:
                if not check.passed:
                    reasons.append(f"Hard constraint violation: {check.details}")
            for check in compatibility.checks:
                if not check.passed:
                    reasons.append(f"Compatibility failure: {check.details}")
        elif risk.level in [RiskLevelEnum.HIGH, RiskLevelEnum.MEDIUM]:
            decision = DecisionEnum.REVIEW
            feasibility_status = FeasibilityStatusEnum.CONDITIONAL
            reasons.append("Hard constraints satisfied, but operational proximity risk factors require human review.")
            for factor in risk.factors:
                warnings.append(factor.explanation)
        else:
            decision = DecisionEnum.PROCEED
            feasibility_status = FeasibilityStatusEnum.FEASIBLE
            reasons.append("All hard feasibility constraints passed and calculated risk levels remain low.")

        # Baseline Parameters Summary
        baseline_dict = {
            "vessel_capacity_dwt": proposal.vessel.capacity_dwt,
            "vessel_draft_m": proposal.vessel.draft_m,
            "cargo_quantity_mt": proposal.cargo.quantity_mt,
            "port_max_draft_m": proposal.port.max_draft_m,
            "schedule_margin_days": proposal.schedule_margin_days,
        }

        # Step 7: What-If Simulation
        what_if_results: List[WhatIfScenarioResult] = []
        if scenarios:
            what_if_engine = WhatIfEngine(self.evaluate_proposal)
            for scenario in scenarios:
                res = what_if_engine.run_scenario(proposal, decision, risk, scenario)
                what_if_results.append(res)

        return DecisionEvaluationResponse(
            decision=decision,
            feasibility_status=feasibility_status,
            compatibility=compatibility,
            constraints=constraints,
            allocation=allocation,
            route=route,
            risk=risk,
            baseline=baseline_dict,
            what_if=what_if_results,
            decision_trace=decision_trace,
            reasons=reasons,
            warnings=warnings,
        )