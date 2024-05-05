from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from src.extensions import db


class Customer(db.Model):
    __tablename__ = "customers"
    __table_args__ = {"schema": "dev"}

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    mobile_number = Column(String(15))
    email = Column(String(255))
    credit_balance = Column(Numeric, default=0)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)
    
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])
