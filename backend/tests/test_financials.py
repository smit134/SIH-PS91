import pytest
from app.services.financial_engine import calculate_emi, calculate_breakeven, simulate_scenario
from app.models.financials import SimulatorInput, OperatingAssumptions

def test_calculate_emi_standard():
    # Principal: 1,00,000, Rate: 10%, Tenure: 12 months
    emi = calculate_emi(100000, 10.0, 12)
    assert emi == 8791.59

def test_calculate_emi_zero_interest():
    emi = calculate_emi(120000, 0.0, 12)
    assert emi == 10000.0

def test_calculate_breakeven():
    # Project cost: 1,00,000. Revenue: 20,000, Costs: 10,000 -> Profit: 10,000
    months = calculate_breakeven(100000, 20000, 10000)
    assert months == 10

def test_calculate_breakeven_never():
    # Costs > Revenue
    months = calculate_breakeven(100000, 10000, 20000)
    assert months is None

def test_simulate_scenario():
    input_data = SimulatorInput(
        project_cost=200000,
        own_contribution=50000,
        interest_rate=12.0,
        tenure_months=24,
        operating_assumptions=OperatingAssumptions(
            monthly_revenue=50000,
            monthly_fixed_costs=15000,
            monthly_variable_costs=10000
        )
    )
    output = simulate_scenario(input_data)
    
    assert output.required_loan == 150000
    assert output.emi == 7061.02
    assert output.monthly_profit == 50000 - (15000 + 10000 + 7061.02)
    assert len(output.repayment_schedule) == 24
