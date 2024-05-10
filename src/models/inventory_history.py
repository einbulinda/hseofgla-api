from sqlalchemy import Column, Integer, Numeric, String, TIMESTAMP, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.services.extensions import db

class InventoryHistory(db.Model):
    __tablename__ = "inventory_history"
    __table_args__ = {"schema":"dev"}

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(Integer, ForeignKey('dev.product_variants.variant_id'), nullable=False)
    warehouse_stock_before = Column(Integer, nullable=False)
    warehouse_stock_after = Column(Integer, nullable=False)
    shop_stock_before = Column(Integer, nullable=False)
    shop_stock_after = Column(Integer, nullable=False)
    change_reason = Column(Text)
    change_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    staff_id = Column(Integer, ForeignKey('dev.staff.staff_id'), nullable=False)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    variant = relationship('ProductVariant')
    staff = relationship('Staff', foreign_keys=[staff_id])
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])