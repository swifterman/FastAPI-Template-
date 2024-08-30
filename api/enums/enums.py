from enum import Enum


class PaymentStatus(Enum):
    PENDING = 'PENDING'
    PAID = 'PAID'
    CANCELLED = 'CANCELLED'
    REFUNDED = 'REFUNDED'
    FAILED = 'FAILED'
