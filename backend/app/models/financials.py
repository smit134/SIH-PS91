from pydantic import BaseModel, Field
from typing import List, Optional

class OperatingAssumptions(BaseModel):
    monthly_revenue: float = Field(..., description="Estimated monthly revenue")
    monthly_fixed_costs: float = Field(..., description="Estimated monthly fixed costs (rent, salaries, etc.)")
    monthly_variable_costs: float = Field(..., description="Estimated monthly variable costs")

class SimulatorInput(BaseModel):
    project_cost: float = Field(..., description="Total cost of the project")
    own_contribution: float = Field(..., description="Entrepreneur's own capital contribution")
    interest_rate: float = Field(..., description="Annual interest rate in percentage (e.g., 8.5 for 8.5%)")
    tenure_months: int = Field(..., description="Loan tenure in months")
    operating_assumptions: OperatingAssumptions

class RepaymentScheduleItem(BaseModel):
    month: int
    principal_payment: float
    interest_payment: float
    total_payment: float
    remaining_balance: float

class SimulatorOutput(BaseModel):
    required_loan: float
    emi: float
    total_interest: float
    monthly_profit: float
    break_even_months: Optional[int]
    risk_level: str
    repayment_schedule: List[RepaymentScheduleItem]

class UserProfile(BaseModel):
    skills: List[str]
    capital: float
    resources: List[str]
    interests: List[str]
    location: dict

class SchemeMatchItem(BaseModel):
    scheme_name: str
    match_score: float
    reasons: List[str]
    application_route: str
    official_source: str
    scheme_id: Optional[str] = None
    short_code: Optional[str] = None
    nodal_agency: Optional[str] = None
    subsidy_percent: Optional[float] = 0.0
    subsidy_rate_text: Optional[str] = None
    max_project_cost: Optional[float] = None
    estimated_subsidy_amount: Optional[float] = None
    applicable_opportunities: Optional[List[str]] = None
    priority_category: Optional[str] = None
    collateral_free: Optional[bool] = False
    description: Optional[str] = None
    status_tag: Optional[str] = None
    documents_required: Optional[List[str]] = None

