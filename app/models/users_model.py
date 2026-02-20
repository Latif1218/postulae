from sqlalchemy import Column, String, Boolean, TIMESTAMP, text, DateTime, Integer
from datetime import datetime
from ..database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    role = Column(String, default="user")
    plan = Column(String, default="essential")
    status = Column(String, default="active")
    last_activity = Column(DateTime, nullable=True)
    cv_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=datetime.utcnow)
    