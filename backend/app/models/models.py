from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

from ..database import Base


class ClaimStatus(str, enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PENDING = "PENDING"


class ActionItemStatus(str, enum.Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    claim_number = Column(String, unique=True, index=True)
    external_id = Column(String, index=True, nullable=True)
    company = Column(String, nullable=True)
    status = Column(String, default=ClaimStatus.OPEN)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    email_threads = relationship("EmailThread", back_populates="claim", cascade="all, delete-orphan")
    action_items = relationship("ActionItem", back_populates="claim", cascade="all, delete-orphan")


class EmailThread(Base):
    __tablename__ = "email_threads"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    subject = Column(String, nullable=True)
    raw_body = Column(Text)
    clean_body = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    claim = relationship("Claim", back_populates="email_threads")
    action_items = relationship("ActionItem", back_populates="email_thread", cascade="all, delete-orphan")


class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    thread_id = Column(Integer, ForeignKey("email_threads.id"), nullable=True)
    description = Column(Text)
    status = Column(String, default=ActionItemStatus.TODO)
    assignee = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    claim = relationship("Claim", back_populates="action_items")
    email_thread = relationship("EmailThread", back_populates="action_items") 