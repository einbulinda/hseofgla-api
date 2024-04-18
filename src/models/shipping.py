from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src import db

class ShippingAddresses(db.Model):
    __tablename__ = "shipping_addresses"
    __table_args__ = {"schema": "dev"}

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('dev.customers.customer_id'), nullable=False)
    county = Column(String(100), nullable=False)
    town = Column(String(100), nullable=False)
    landmark = Column(String(255), nullable=False)
    additional_info = Column(String(255))
    is_default = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    customer = relationship('Customers', foreign_keys=customer_id)
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])