from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src import db

class ProductVariants(db.Model):
    __tablename__ = 'product_variants'
    __table_args__ = {'schema': 'dev'}

    variant_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('dev.products.product_id'), nullable=False)
    sku = Column(String(255), unique=True, nullable=False)
    price = Column(Numeric, nullable=False)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False)
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    product = relationship("Products")
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])