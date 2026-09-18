"""
Constraint Engine Service — Evaluates hard operational constraints independently from risk.
"""

from typing import List
from backend.models.decision_models import CheckResult, ConstraintResult, VoyageProposalModel


class ConstraintEngine:
    """Evaluates strict pass/fail constraints that govern voyage feasibility."""

    @staticmethod
    def evaluate(proposal: VoyageProposalModel) -> ConstraintResult:
        checks: List[CheckResult] = []
        violations: List[str] = []
        feasible = True

        # Hard Constraint 1: Cargo capacity violation
        if proposal.cargo.quantity_mt > proposal.vessel.capacity_dwt:
            feasible = False
            msg = f"Cargo requirement ({proposal.cargo.quantity_mt} MT) exceeds vessel capacity ({proposal.vessel.capacity_dwt} DWT)."
            violations.append(msg)
            checks.append(CheckResult(check_name="Hard Capacity Constraint", passed=False, details=msg))
        else:
            checks.append(
                CheckResult(
                    check_name="Hard Capacity Constraint",
                    passed=True,
                    details=f"Cargo weight ({proposal.cargo.quantity_mt} MT) is within vessel capacity ({proposal.vessel.capacity_dwt} DWT).",
                )
            )

        # Hard Constraint 2: Port draft restriction
        if proposal.vessel.draft_m > proposal.port.max_draft_m:
            feasible = False
            msg = f"Vessel draft ({proposal.vessel.draft_m}m) exceeds port draft limit ({proposal.port.max_draft_m}m)."
            violations.append(msg)
            checks.append(CheckResult(check_name="Hard Draft Constraint", passed=False, details=msg))
        else:
            checks.append(
                CheckResult(
                    check_name="Hard Draft Constraint",
                    passed=True,
                    details=f"Vessel draft ({proposal.vessel.draft_m}m) satisfies port draft limit ({proposal.port.max_draft_m}m).",
                )
            )

        return ConstraintResult(feasible=feasible, violations=violations, checks=checks)