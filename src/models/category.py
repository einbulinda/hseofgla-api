from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from src.services.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = {"schema":"dev"}

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), nullable=False)
    parent_category_id = Column(Integer, ForeignKey('dev.categories.category_id'), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'), nullable=False)
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'), nullable=True)
    updated_date = Column(TIMESTAMP, nullable=True)

    subcategories = relationship("Category", backref=backref('parent_category', remote_side=[category_id]),
                                 cascade="all, delete-orphan")
    creator = relationship("Staff", foreign_keys=[created_by], backref="category_creations")
    updater = relationship("Staff", foreign_keys=[updated_by], backref="category_updates")