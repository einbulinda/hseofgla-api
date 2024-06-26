from sqlalchemy import Column, Integer, String
from src.services.extensions import db

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    __table_args__ = {"schema":"aud"}

    id = Column(Integer, primary_key=True)
    jti = Column(String(120), unique=True,nullable=False)

    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls,jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)
