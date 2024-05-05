from sqlalchemy import Column, Integer,Numeric, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src.extensions import db

class Order(db.Model):
    __tablename__ = "orders"
    __table_args__ = {"schema": "dev"}

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('dev.customers.customer_id'))
    total_items_count = Column(Integer, nullable=False)
    total_order_amount = Column(Numeric, nullable=False)
    order_status = Column(String(50), nullable=False)
    order_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    customer = relationship('Customer', foreign_keys=[customer_id])
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])