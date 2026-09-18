"""
Data schemas for FreightIQ Decision, Risk, Route, Allocation, and What-If Engine.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DecisionEnum(str, Enum):
    PROCEED = "PROCEED"
    REVIEW = "REVIEW"
    REJECT = "REJECT"


class FeasibilityStatusEnum(str, Enum):
    FEASIBLE = "FEASIBLE"
    CONDITIONAL = "CONDITIONAL"
    INFEASIBLE = "INFEASIBLE"


class RiskLevelEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class VesselModel(BaseModel):
    vessel_id: str
    capacity_dwt: float = Field(..., gt=0, description="Vessel deadweight capacity in MT")
    draft_m: float = Field(..., gt=0, description="Vessel operational draft in meters")


class CargoModel(BaseModel):
    cargo_id: str
    quantity_mt: float = Field(..., ge=0, description="Cargo weight in MT")


class PortModel(BaseModel):
    port_id: str
    max_draft_m: float = Field(..., gt=0, description="Maximum allowable port draft in meters")


class VoyageProposalModel(BaseModel):
    proposal_id: str
    vessel: VesselModel
    cargo: CargoModel
    port: PortModel
    schedule_margin_days: float = Field(default=0.0, ge=0, description="Schedule buffer days")


class CheckResult(BaseModel):
    check_name: str
    passed: bool
    details: str


class CompatibilityResult(BaseModel):
    compatible: bool
    checks: List[CheckResult]
    warnings: List[str] = []


class ConstraintResult(BaseModel):
    feasible: bool
    violations: List[str] = []
    checks: List[CheckResult]


class AllocationResult(BaseModel):
    allocated_mt: float
    unallocated_mt: float
    capacity_dwt: float
    utilization_ratio: float
    over_capacity: bool


class RouteEvaluationResult(BaseModel):
    schedule_margin_days: float
    sufficient_buffer: bool
    details: str


class RiskFactor(BaseModel):
    factor: str
    value: float
    threshold: float
    contribution: float
    explanation: str


class RiskEvaluation(BaseModel):
    level: RiskLevelEnum
    score: float = Field(ge=0.0, le=100.0)
    factors: List[RiskFactor]


class WhatIfScenarioRequest(BaseModel):
    scenario_id: str
    overrides: Dict[str, Any]


class WhatIfScenarioResult(BaseModel):
    scenario_id: str
    modified_parameters: Dict[str, Any]
    decision: DecisionEnum
    feasibility_status: FeasibilityStatusEnum
    risk_level: RiskLevelEnum
    risk_score: float
    decision_changed: bool
    risk_changed: bool
    triggered_factors: List[str]
    explanation: str


class DecisionTraceStep(BaseModel):
    stage: str
    status: str
    details: str


class DecisionEvaluationResponse(BaseModel):
    decision: DecisionEnum
    feasibility_status: FeasibilityStatusEnum
    compatibility: CompatibilityResult
    constraints: ConstraintResult
    allocation: AllocationResult
    route: RouteEvaluationResult
    risk: RiskEvaluation
    baseline: Dict[str, Any]
    what_if: List[WhatIfScenarioResult] = []
    decision_trace: List[DecisionTraceStep]
    reasons: List[str]
    warnings: List[str]