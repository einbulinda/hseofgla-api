from sqlalchemy import Column, Integer, String, Numeric, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src.services.extensions import db

class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    __table_args__ = {'schema': 'dev'}

    variant_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('dev.products.product_id'), nullable=False)
    sku = Column(String(255), unique=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False)
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    # product = relationship("Product")
    attributes = relationship('ProductAttribute', backref='variant', cascade='all, delete-orphan')
    images = relationship('ProductImage', backref='variant',cascade='all, delete-orphan')
    
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])