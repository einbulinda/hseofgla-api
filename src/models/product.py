from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src.services.extensions import db


class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'dev'}

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('dev.categories.category_id'))
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False)
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    category = relationship("Category")
    variants = relationship('ProductVariant', backref='product',lazy='dynamic', cascade="all, delete-orphan")
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])