"""
FastAPI router for Decision Engine evaluations.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from backend.models.decision_models import (
    DecisionEvaluationResponse,
    VoyageProposalModel,
    WhatIfScenarioRequest,
)
from backend.services.decision_engine import DecisionEngine

router = APIRouter(prefix="/decision", tags=["Charter Decision Intelligence"])
decision_engine = DecisionEngine()


class EvaluationPayload(BaseModel):
    proposal: VoyageProposalModel
    what_if_scenarios: Optional[List[WhatIfScenarioRequest]] = None


@router.post("/evaluate", response_model=DecisionEvaluationResponse, status_code=status.HTTP_200_OK)
def evaluate_charter_proposal(payload: EvaluationPayload):
    """
    Evaluates a charter proposal deterministically through compatibility, constraints, allocation,
    route, risk, and what-if simulation layers.
    """
    try:
        return decision_engine.evaluate_proposal(payload.proposal, payload.what_if_scenarios)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An evaluation error occurred. Details suppressed for security.",
        )