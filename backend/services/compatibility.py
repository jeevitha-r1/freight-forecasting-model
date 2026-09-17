"""
Compatibility Service — Evaluates pair-wise entity compatibility (Vessel <-> Port, Vessel <-> Cargo).
"""

from typing import List
from backend.models.decision_models import CheckResult, CompatibilityResult, VoyageProposalModel


class CompatibilityEngine:
    """Checks physical and operational compatibility between entities."""

    @staticmethod
    def evaluate(proposal: VoyageProposalModel) -> CompatibilityResult:
        checks: List[CheckResult] = []
        warnings: List[str] = []
        compatible = True

        # 1. Vessel <-> Port Draft Compatibility
        draft_ok = proposal.vessel.draft_m <= proposal.port.max_draft_m
        checks.append(
            CheckResult(
                check_name="Vessel-Port Draft Compatibility",
                passed=draft_ok,
                details=(
                    f"Vessel draft ({proposal.vessel.draft_m}m) is compatible with port draft limit ({proposal.port.max_draft_m}m)."
                    if draft_ok
                    else f"Vessel draft ({proposal.vessel.draft_m}m) exceeds port max draft ({proposal.port.max_draft_m}m)."
                ),
            )
        )
        if not draft_ok:
            compatible = False

        # 2. Vessel <-> Cargo Quantity Compatibility
        capacity_ok = proposal.cargo.quantity_mt <= proposal.vessel.capacity_dwt
        checks.append(
            CheckResult(
                check_name="Vessel-Cargo Capacity Compatibility",
                passed=capacity_ok,
                details=(
                    f"Cargo quantity ({proposal.cargo.quantity_mt} MT) fits vessel capacity ({proposal.vessel.capacity_dwt} DWT)."
                    if capacity_ok
                    else f"Cargo quantity ({proposal.cargo.quantity_mt} MT) exceeds vessel deadweight capacity ({proposal.vessel.capacity_dwt} DWT)."
                ),
            )
        )
        if not capacity_ok:
            compatible = False

        return CompatibilityResult(compatible=compatible, checks=checks, warnings=warnings)