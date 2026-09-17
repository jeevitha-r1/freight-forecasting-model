"""
Comprehensive unit test suite for FreightIQ Decision Engine and sub-services.
"""

import pytest
from backend.models.decision_models import (
    CargoModel,
    DecisionEnum,
    FeasibilityStatusEnum,
    PortModel,
    RiskLevelEnum,
    VesselModel,
    VoyageProposalModel,
    WhatIfScenarioRequest,
)
from backend.services.decision_engine import DecisionEngine


@pytest.fixture
def base_proposal():
    return VoyageProposalModel(
        proposal_id="PROP-001",
        vessel=VesselModel(vessel_id="V-100", capacity_dwt=50000.0, draft_m=11.0),
        cargo=CargoModel(cargo_id="C-200", quantity_mt=35000.0),
        port=PortModel(port_id="P-300", max_draft_m=13.0),
        schedule_margin_days=5.0,
    )


def test_valid_feasible_case_proceed(base_proposal):
    engine = DecisionEngine()
    result = engine.evaluate_proposal(base_proposal)

    assert result.decision == DecisionEnum.PROCEED
    assert result.feasibility_status == FeasibilityStatusEnum.FEASIBLE
    assert result.compatibility.compatible is True
    assert result.constraints.feasible is True
    assert result.allocation.utilization_ratio == 0.70
    assert result.risk.level == RiskLevelEnum.LOW
    assert len(result.decision_trace) == 5


def test_capacity_violation_reject(base_proposal):
    engine = DecisionEngine()
    base_proposal.cargo.quantity_mt = 55000.0
    result = engine.evaluate_proposal(base_proposal)

    assert result.decision == DecisionEnum.REJECT
    assert result.feasibility_status == FeasibilityStatusEnum.INFEASIBLE
    assert result.constraints.feasible is False
    assert result.allocation.over_capacity is True
    assert len(result.constraints.violations) > 0


def test_draft_violation_reject(base_proposal):
    engine = DecisionEngine()
    base_proposal.vessel.draft_m = 14.0
    result = engine.evaluate_proposal(base_proposal)

    assert result.decision == DecisionEnum.REJECT
    assert result.feasibility_status == FeasibilityStatusEnum.INFEASIBLE
    assert result.compatibility.compatible is False


def test_high_utilization_review(base_proposal):
    engine = DecisionEngine()
    base_proposal.cargo.quantity_mt = 44000.0  # 88% utilization (> 85% review threshold)
    result = engine.evaluate_proposal(base_proposal)

    assert result.decision == DecisionEnum.REVIEW
    assert result.feasibility_status == FeasibilityStatusEnum.CONDITIONAL
    assert result.risk.level in [RiskLevelEnum.MEDIUM, RiskLevelEnum.HIGH]


def test_what_if_changes_decision_and_preserves_baseline(base_proposal):
    engine = DecisionEngine()
    original_cargo = base_proposal.cargo.quantity_mt

    scenario = WhatIfScenarioRequest(
        scenario_id="INCREASE_CARGO", overrides={"cargo_quantity_mt": 48000.0}
    )

    result = engine.evaluate_proposal(base_proposal, scenarios=[scenario])

    assert result.decision == DecisionEnum.PROCEED
    assert base_proposal.cargo.quantity_mt == original_cargo

    assert len(result.what_if) == 1
    scen_res = result.what_if[0]
    assert scen_res.decision == DecisionEnum.REVIEW
    assert scen_res.decision_changed is True
    assert scen_res.risk_changed is True


def test_unknown_what_if_parameter_raises_error(base_proposal):
    engine = DecisionEngine()
    scenario = WhatIfScenarioRequest(scenario_id="BAD_PARAM", overrides={"unsupported_field": 100})

    with pytest.raises(ValueError) as excinfo:
        engine.evaluate_proposal(base_proposal, scenarios=[scenario])

    assert "Invalid what-if parameter" in str(excinfo.value)


def test_determinism(base_proposal):
    engine = DecisionEngine()
    res1 = engine.evaluate_proposal(base_proposal)
    res2 = engine.evaluate_proposal(base_proposal)

    assert res1.model_dump() == res2.model_dump()