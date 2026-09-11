from fastapi import APIRouter, HTTPException
from app.models.financials import SimulatorInput, SimulatorOutput
from app.services.financial_engine import simulate_scenario

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
