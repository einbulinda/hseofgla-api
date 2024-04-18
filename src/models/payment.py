from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP,ForeignKey
from sqlalchemy.orm import relationship
from src import db

class Payment(db.Model):
    __tablename__ = "payments"
    __table_args__ = {"schema": "dev"}

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('dev.orders.order_id'))
    amount_paid = Column(Numeric, nullable=False)
    payment_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    payment_method = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    order = relationship('Order', foreign_keys=[order_id])
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])