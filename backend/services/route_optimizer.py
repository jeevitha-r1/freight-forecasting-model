"""
Route Optimizer / Evaluator Service — Evaluates voyage scheduling and buffer margins.
"""

from backend.config.decision_config import DEFAULT_DECISION_CONFIG, DecisionConfig
from backend.models.decision_models import RouteEvaluationResult, VoyageProposalModel


class RouteOptimizer:
    """Evaluates voyage parameters and schedule buffers against operational bounds."""

    @staticmethod
    def evaluate_route(
        proposal: VoyageProposalModel, config: DecisionConfig = DEFAULT_DECISION_CONFIG
    ) -> RouteEvaluationResult:
        margin = proposal.schedule_margin_days
        sufficient = margin >= config.schedule_margin_review_threshold_days

        details = (
            f"Schedule margin of {margin:.1f} days meets or exceeds buffer threshold ({config.schedule_margin_review_threshold_days:.1f} days)."
            if sufficient
            else f"Schedule margin of {margin:.1f} days is below recommended buffer threshold ({config.schedule_margin_review_threshold_days:.1f} days)."
        )

        return RouteEvaluationResult(
            schedule_margin_days=margin, sufficient_buffer=sufficient, details=details
        )