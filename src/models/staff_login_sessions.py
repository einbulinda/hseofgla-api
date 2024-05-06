from sqlalchemy import Column, Integer, TIMESTAMP, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.services.extensions import db

class StaffLoginSessions(db.Model):
    __tablename__ = "staff_login_sessions"
    __table_args__ = {"schema": "aud"}

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    staff_id = Column(Integer, ForeignKey('dev.staff.staff_id'), nullable=False)
    login_timestamp = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())
    logout_timestamp = Column(TIMESTAMP)
    ip_address = Column(String(255))
    device_info = Column(Text)

    staff = relationship('Staff', foreign_keys=staff_id)