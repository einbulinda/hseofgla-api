from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src.services.extensions import db

class ProductImage(db.Model):
    __tablename__ = "product_images"
    __table_args__ = {"schema": "dev"}

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(Integer, ForeignKey('dev.product_variants.variant_id'), nullable=False)
    image_name = Column(String(255), nullable=False)
    image_url = Column(Text, nullable=False)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    # variant = relationship('ProductVariant', foreign_keys=variant_id)
    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])