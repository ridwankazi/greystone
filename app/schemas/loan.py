from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class LoanBase(BaseModel):
    user_id: int
    principal: Decimal = Field(gt=0)
    annual_interest_rate: Decimal = Field(ge=0)
    term_months: int = Field(gt=0)
    start_date: date
    name: str | None = None


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    principal: Decimal | None = Field(default=None, gt=0)
    annual_interest_rate: Decimal | None = Field(default=None, ge=0)
    term_months: int | None = Field(default=None, gt=0)
    start_date: date | None = None
    name: str | None = None


class LoanRead(LoanBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AmortizationRequest(BaseModel):
    principal: Decimal = Field(gt=0)
    annual_interest_rate: Decimal = Field(ge=0)
    term_months: int = Field(gt=0)
    start_date: date


class AmortizationEntry(BaseModel):
    period: int
    date: date
    payment: Decimal
    principal: Decimal
    interest: Decimal
    balance: Decimal


class AmortizationSchedule(BaseModel):
    monthly_payment: Decimal
    total_interest: Decimal
    total_paid: Decimal
    schedule: list[AmortizationEntry]
