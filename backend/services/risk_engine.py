"""
Risk Engine Service — Deterministic calculation of prototype operational risk scores and factors.
"""

from typing import List
from backend.config.decision_config import DEFAULT_DECISION_CONFIG, DecisionConfig
from backend.models.decision_models import RiskEvaluation, RiskFactor, RiskLevelEnum, VoyageProposalModel


class RiskEngine:
    """Calculates operational risk score based on proximity to operational bounds."""

    @staticmethod
    def evaluate(
        proposal: VoyageProposalModel, config: DecisionConfig = DEFAULT_DECISION_CONFIG
    ) -> RiskEvaluation:
        factors: List[RiskFactor] = []
        total_score = 0.0

        capacity = max(proposal.vessel.capacity_dwt, 0.0001)

        # 1. Capacity Utilization Proximity
        utilization = proposal.cargo.quantity_mt / capacity
        if utilization > config.capacity_utilization_review_threshold:
            excess_ratio = (utilization - config.capacity_utilization_review_threshold) / (
                1.0 - config.capacity_utilization_review_threshold
            )
            contribution = round(min(excess_ratio, 1.0) * config.weight_capacity_utilization, 2)
            total_score += contribution
            factors.append(
                RiskFactor(
                    factor="High Capacity Utilization",
                    value=round(utilization, 4),
                    threshold=config.capacity_utilization_review_threshold,
                    contribution=contribution,
                    explanation=(
                        f"Capacity utilization ({utilization:.1%}) exceeds review threshold "
                        f"({config.capacity_utilization_review_threshold:.1%})."
                    ),
                )
            )

        # 2. Draft Clearance Margin Proximity
        draft_margin = proposal.port.max_draft_m - proposal.vessel.draft_m
        if draft_margin < config.draft_margin_review_threshold_m:
            deficit_ratio = (
                config.draft_margin_review_threshold_m - max(draft_margin, 0.0)
            ) / config.draft_margin_review_threshold_m
            contribution = round(min(deficit_ratio, 1.0) * config.weight_draft_margin, 2)
            total_score += contribution
            factors.append(
                RiskFactor(
                    factor="Low Draft Clearance Margin",
                    value=round(draft_margin, 2),
                    threshold=config.draft_margin_review_threshold_m,
                    contribution=contribution,
                    explanation=(
                        f"Draft clearance margin ({draft_margin:.2f}m) is below threshold "
                        f"({config.draft_margin_review_threshold_m:.2f}m)."
                    ),
                )
            )

        # 3. Schedule Margin Proximity
        if proposal.schedule_margin_days < config.schedule_margin_review_threshold_days:
            schedule_deficit = (
                config.schedule_margin_review_threshold_days
                - max(proposal.schedule_margin_days, 0.0)
            ) / config.schedule_margin_review_threshold_days
            contribution = round(min(schedule_deficit, 1.0) * config.weight_schedule_margin, 2)
            total_score += contribution
            factors.append(
                RiskFactor(
                    factor="Tight Schedule Margin",
                    value=round(proposal.schedule_margin_days, 2),
                    threshold=config.schedule_margin_review_threshold_days,
                    contribution=contribution,
                    explanation=(
                        f"Schedule margin ({proposal.schedule_margin_days:.1f} days) is below threshold "
                        f"({config.schedule_margin_review_threshold_days:.1f} days)."
                    ),
                )
            )

        total_score = min(round(total_score, 2), 100.0)

        if total_score >= config.risk_score_high_threshold:
            level = RiskLevelEnum.HIGH
        elif total_score >= config.risk_score_medium_threshold or len(factors) > 0:
            level = RiskLevelEnum.MEDIUM
        else:
            level = RiskLevelEnum.LOW

        return RiskEvaluation(level=level, score=total_score, factors=factors)