from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from src import db

class LoginDetails(db.Model):
    __tablename__ = "login_details"
    __table_args__ = {"schema": "aud"}

    loggin_id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('dev.staff.staff_id'))
    customer_id = Column(Integer, ForeignKey('dev.customers.customer_id'))
    username = Column(String(255), unique=True)
    password = Column(String(255))
    created_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    created_date = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    updated_by = Column(Integer, ForeignKey('dev.staff.staff_id'))
    updated_date = Column(TIMESTAMP)

    created_by_rel = relationship("Staff", foreign_keys=[created_by])
    updated_by_rel = relationship("Staff", foreign_keys=[updated_by])