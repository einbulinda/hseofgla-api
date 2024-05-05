from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.orm import relationship
from src.extensions import db


class Discount(db.Model):
    __tablename__ = "discounts"
    __table_args__ = {"schema": "dev"}
    
    discount_id = Column(Integer, primary_key=True, autoincrement=True)
    discount_name = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey('dev.products.product_id'))
    variant_id = Column(Integer, ForeignKey('dev.product_variants.variant_id'))
    discount_rate = Column(Numeric, nullable=False, default=0)
    discount_amount = Column(Numeric, nullable=False, default=0)
    start_date = Column(TIMESTAMP)
    expiry_date = Column(TIMESTAMP)
    description = Column(String(255))
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)
	
    product = relationship('Product', foreign_keys=product_id)
    product_variant = relationship('ProductVariants', foreign_keys=variant_id)
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])