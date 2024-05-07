from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src.services.extensions import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    __table_args__ = {'schema': 'dev'}

    inventory_id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(Integer, ForeignKey('dev.product_variants.variant_id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    warehouse_stock = Column(Integer, nullable=False)
    shop_stock = Column(Integer, nullable=False)
    reorder_level = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False)
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    variant = relationship("ProductVariants")
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])