from pydantic import BaseModel

from api.enums.enums import PaymentStatus


class PaymentCreate(BaseModel):
    amount: int
    currency: str


class Payment(PaymentCreate):
    id: int
    user_id: int
    status: PaymentStatus

    class Config:
        orm_mode = True


class ChangePaymentStatus(BaseModel):
    id: int
    status: PaymentStatus


class AllPaymentsResponse(BaseModel):
    payments: list[Payment]
