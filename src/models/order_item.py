from sqlalchemy import Column, Integer, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from src.services.extensions import db

class OrderItem(db.Model):
    __tablename__ = "order_items"
    __table_args__ = {"schema":"dev"}

    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('dev.orders.order_id'))
    variant_id = Column(Integer, ForeignKey('dev.product_variants.variant_id'))
    quantity = Column(Integer, nullable=False, default=0)
    discount_rate = Column(Numeric, default=0)
    discount_amount = Column(Numeric, default=0)
    price_at_purchase = Column(Numeric, nullable=False)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)	

    order = relationship('Order', foreign_keys=order_id)
    product_variants = relationship('ProductVariant', foreign_keys=variant_id)
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])