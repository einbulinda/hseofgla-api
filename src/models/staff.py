from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src.extensions import db



class Staff(db.Model):
    __tablename__ = "staff"
    __table_args__ = {"schema":"dev"}
    
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    mobile_number = Column(String(15))
    email = Column(String(255))
    role = Column(String(255), nullable=False)
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    created_by_staff = relationship('Staff', remote_side=[staff_id], foreign_keys=[created_by])
    updated_by_staff = relationship('Staff', remote_side=[staff_id], foreign_keys=[updated_by])