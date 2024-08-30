#copilot:ignore-start
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.enums.enums import PaymentStatus
from api.payment import models
from api.public.public_response import not_found_exception
from api.token.main import get_current_user
from api.user_management.schemas import User
from api.payment.schemas import Payment, PaymentCreate, AllPaymentsResponse, ChangePaymentStatus
from database.database import get_db

router = APIRouter(prefix='/payment', tags=['Payment'], responses={400: {'description': 'Bad Request'}})


@router.post('/create', response_model=Payment)
def create_a_payment(new_payment: PaymentCreate,
                     current_user: Annotated[User, Depends(get_current_user)],
                     db: Session = Depends(get_db)):
    try:
        db_new_payment = models.Payment(amount=new_payment.amount,
                                        status=PaymentStatus.PENDING.value,
                                        currency=new_payment.currency,
                                        user_id=current_user.id)
        db.add(db_new_payment)
        db.commit()
        db.refresh(db_new_payment)
        return db_new_payment
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all", response_model=AllPaymentsResponse)
def get_all_payments_of_user(current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    try:
        payments = db.query(models.Payment).filter(models.Payment.user_id == current_user.id).all()
        return {"payments": payments}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/change", response_model=Payment)
def change_payment_status(payment: ChangePaymentStatus, current_user: Annotated[User, Depends(get_current_user)],
                          db: Session = Depends(get_db)):
    exist_payment = db.query(models.Payment).filter(models.Payment.id == payment.id).first()
    if exist_payment:
        exist_payment.status = payment.status.value
        try:
            db.add(exist_payment)
            db.commit()
            db.refresh(exist_payment)
            return exist_payment
        except Exception as x:
            raise HTTPException(status_code=400, detail=str(x))
    not_found_exception('Selected Payment not found')
