from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from app.models.financials import SimulatorInput, SimulatorOutput
from app.services.financial_engine import (
    simulate_scenario,
    load_financial_templates,
    get_financial_template,
    stress_test_scenario,
)

router = APIRouter(
    prefix="/finance",
    tags=["finance"]
)

@router.post("/simulate", response_model=SimulatorOutput)
def simulate_finances(input_data: SimulatorInput):
    """
    Test project cost, loan requirement, EMI, revenue, expenses, profit and break-even under different scenarios.
    """
    try:
        result = simulate_scenario(input_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/templates")
def list_financial_templates():
    """
    Returns data-driven financial templates for rural micro-enterprises
    derived from MSME invoice transaction datasets.
    """
    return load_financial_templates()


@router.get("/templates/{category_id}")
def get_template(category_id: str):
    """
    Returns sector-specific financial baselines (revenue, expenses, payment delays, working capital ratio).
    """
    tpl = get_financial_template(category_id)
    if not tpl:
        raise HTTPException(status_code=404, detail=f"No financial template found for category: {category_id}")
    return tpl


@router.post("/stress-test")
def stress_test_finances(
    input_data: SimulatorInput,
    category_id: Optional[str] = Query(None, description="Optional business category for sector benchmarking")
):
    """
    Runs multi-scenario sensitivity analysis (Base case, -20% Conservative, +20% Optimistic)
    calibrated against empirical MSME variance.
    """
    try:
        return stress_test_scenario(input_data, category_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
