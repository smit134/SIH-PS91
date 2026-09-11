import math
from typing import List, Tuple, Optional
from app.models.financials import SimulatorInput, SimulatorOutput, RepaymentScheduleItem

def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> float:
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    if annual_rate == 0:
        return principal / tenure_months
        
    monthly_rate = (annual_rate / 100) / 12
    emi = principal * monthly_rate * math.pow(1 + monthly_rate, tenure_months) / (math.pow(1 + monthly_rate, tenure_months) - 1)
    return round(emi, 2)

def calculate_repayment_schedule(principal: float, annual_rate: float, tenure_months: int) -> Tuple[List[RepaymentScheduleItem], float]:
    schedule = []
    if principal <= 0 or tenure_months <= 0:
        return schedule, 0.0

    emi = calculate_emi(principal, annual_rate, tenure_months)
    monthly_rate = (annual_rate / 100) / 12
    
    balance = principal
    total_interest = 0.0

    for month in range(1, tenure_months + 1):
        interest_payment = balance * monthly_rate
        principal_payment = emi - interest_payment
        
        if principal_payment > balance:
            principal_payment = balance
            emi = principal_payment + interest_payment

        balance -= principal_payment
        if balance < 0.01:  # Handle floating point inaccuracies
            balance = 0.0
            
        total_interest += interest_payment
        
        schedule.append(RepaymentScheduleItem(
            month=month,
            principal_payment=round(principal_payment, 2),
            interest_payment=round(interest_payment, 2),
            total_payment=round(emi, 2),
            remaining_balance=round(balance, 2)
        ))

    return schedule, round(total_interest, 2)

def calculate_breakeven(project_cost: float, monthly_revenue: float, monthly_costs: float) -> Optional[int]:
    monthly_profit = monthly_revenue - monthly_costs
    if monthly_profit <= 0:
        return None # Never breaks even
    return math.ceil(project_cost / monthly_profit)

def simulate_scenario(input_data: SimulatorInput) -> SimulatorOutput:
    required_loan = max(0.0, input_data.project_cost - input_data.own_contribution)
    
    schedule, total_interest = calculate_repayment_schedule(
        required_loan, 
        input_data.interest_rate, 
        input_data.tenure_months
    )
    
    emi = schedule[0].total_payment if schedule else 0.0
    
    total_monthly_costs = (
        input_data.operating_assumptions.monthly_fixed_costs + 
        input_data.operating_assumptions.monthly_variable_costs + 
        emi
    )
    
    monthly_profit = input_data.operating_assumptions.monthly_revenue - total_monthly_costs
    
    break_even = calculate_breakeven(
        input_data.project_cost, 
        input_data.operating_assumptions.monthly_revenue, 
        total_monthly_costs
    )
    
    # Simple risk heuristic
    if monthly_profit < 0:
        risk_level = "High"
    elif break_even and break_even > 36:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    return SimulatorOutput(
        required_loan=round(required_loan, 2),
        emi=round(emi, 2),
        total_interest=total_interest,
        monthly_profit=round(monthly_profit, 2),
        break_even_months=break_even,
        risk_level=risk_level,
        repayment_schedule=schedule
    )
