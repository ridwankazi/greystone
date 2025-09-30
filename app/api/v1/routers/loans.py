from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.loan import (
    AmortizationRequest,
    AmortizationSchedule,
    LoanCreate,
    LoanRead,
    LoanUpdate,
)
from app.services.loans import LoanService

router = APIRouter()


@router.post("/", response_model=LoanRead, status_code=status.HTTP_201_CREATED)
def create_loan(payload: LoanCreate, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.create(payload)
    return loan


@router.get("/", response_model=list[LoanRead])
def list_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = LoanService(db)
    return service.list(skip=skip, limit=limit)


@router.get("/{loan_id}", response_model=LoanRead)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan


@router.put("/{loan_id}", response_model=LoanRead)
def update_loan(loan_id: int, payload: LoanUpdate, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return service.update(loan, payload)


@router.delete("/{loan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_loan(loan_id: int, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    service.delete(loan)
    return None


@router.get("/{loan_id}/amortization", response_model=AmortizationSchedule)
def amortization_for_loan(loan_id: int, db: Session = Depends(get_db)):
    service = LoanService(db)
    loan = service.get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    req = AmortizationRequest(
        principal=loan.principal,
        annual_interest_rate=loan.annual_interest_rate,
        term_months=loan.term_months,
        start_date=loan.start_date,
    )
    return service.compute_amortization(req)


@router.post("/amortization", response_model=AmortizationSchedule)
def amortization_adhoc(payload: AmortizationRequest, db: Session = Depends(get_db)):
    service = LoanService(db)
    return service.compute_amortization(payload)
