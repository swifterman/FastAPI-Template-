from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    currency = Column(String(200))
    status = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="payments")
