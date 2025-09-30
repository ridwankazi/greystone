from __future__ import annotations

from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.loan import Loan
from app.schemas.loan import (
    AmortizationEntry,
    AmortizationRequest,
    AmortizationSchedule,
    LoanCreate,
    LoanUpdate,
)
from app.services.base import BaseService


class LoanService(BaseService[Loan]):
    def __init__(self, db: Session):
        super().__init__(db, Loan)

    def get_for_user(self, user_id: int):
        stmt = select(Loan).where(Loan.user_id == user_id)
        return self.db.execute(stmt).scalars().all()

    def create(self, data: LoanCreate) -> Loan:
        loan = Loan(
            user_id=data.user_id,
            principal=float(data.principal),
            annual_interest_rate=float(data.annual_interest_rate),
            term_months=int(data.term_months),
            start_date=data.start_date,
            name=data.name,
        )
        return self.add(loan)

    def update(self, loan: Loan, data: LoanUpdate) -> Loan:
        if data.principal is not None:
            loan.principal = float(data.principal)
        if data.annual_interest_rate is not None:
            loan.annual_interest_rate = float(data.annual_interest_rate)
        if data.term_months is not None:
            loan.term_months = int(data.term_months)
        if data.start_date is not None:
            loan.start_date = data.start_date
        if data.name is not None:
            loan.name = data.name
        self.db.commit()
        self.db.refresh(loan)
        return loan

    # --- Amortization ---
    @staticmethod
    def _round(value: Decimal, places: int = 2) -> Decimal:
        q = Decimal(10) ** -places
        return value.quantize(q, rounding=ROUND_HALF_UP)

    def compute_amortization(self, req: AmortizationRequest) -> AmortizationSchedule:
        principal = Decimal(req.principal)
        r_annual = Decimal(req.annual_interest_rate)
        n = int(req.term_months)
        start = req.start_date

        r_monthly = r_annual / Decimal(12)
        if r_monthly == 0:
            payment = principal / Decimal(n)
        else:
            # payment = P * r * (1+r)^n / ((1+r)^n - 1)
            factor = (Decimal(1) + r_monthly) ** n
            payment = principal * r_monthly * factor / (factor - Decimal(1))
        payment = self._round(payment)

        balance = principal
        schedule: list[AmortizationEntry] = []
        total_interest = Decimal(0)

        for period in range(1, n + 1):
            interest = self._round(balance * r_monthly)
            principal_component = payment - interest
            if period == n:
                # Adjust last payment for rounding
                principal_component = balance
                payment_actual = principal_component + interest
            else:
                payment_actual = payment
            balance = self._round(balance - principal_component)

            pay_date = self._add_months(start, period - 1)
            schedule.append(
                AmortizationEntry(
                    period=period,
                    date=pay_date,
                    payment=self._round(payment_actual),
                    principal=self._round(principal_component),
                    interest=self._round(interest),
                    balance=self._round(max(balance, Decimal(0))),
                )
            )
            total_interest += interest

        total_paid = sum((e.payment for e in schedule), Decimal(0))

        return AmortizationSchedule(
            monthly_payment=payment,
            total_interest=self._round(total_interest),
            total_paid=self._round(total_paid),
            schedule=schedule,
        )

    @staticmethod
    def _add_months(d: date, months: int) -> date:
        # Simple month rolling without external deps
        year = d.year + (d.month - 1 + months) // 12
        month = (d.month - 1 + months) % 12 + 1
        day = min(
            d.day,
            [
                31,
                29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                31,
                30,
                31,
                30,
                31,
                31,
                30,
                31,
                30,
                31,
                31,
            ][month - 1],
        )
        return date(year, month, day)
