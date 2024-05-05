from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, backref
from src.extensions import db

class Categories(db.Model):
    __tablename__ = 'categories'
    __table_args__ = {"schema":"dev"}

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), nullable=False)
    parent_category_id = Column(Integer, ForeignKey('dev.categories.category_id'), nullable=True)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'), nullable=False)
    created_date = Column(TIMESTAMP, nullable=False)
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'), nullable=True)
    updated_date = Column(TIMESTAMP, nullable=True)

    subcategories = relationship("Categories", backref=backref('parent_category', remote_side=[category_id]),
                                 cascade="all, delete-orphan")
    creator = relationship("Staff", foreign_keys=[created_by], backref="category_creations")
    updater = relationship("Staff", foreign_keys=[updated_by], backref="category_updates")