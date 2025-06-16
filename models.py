from datetime import datetime, timezone
from email.policy import default
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Enum, DateTime,Date, Float, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker
from os import environ
from flask_bcrypt import generate_password_hash, check_password_hash
import random
import string
import os


 

db_url = os.environ.get("DB_URL")

engine = create_engine(db_url, pool_pre_ping=True, future=True)
db_session_maker = sessionmaker(engine)

meta = MetaData()
Model = declarative_base(name='Model')
Model.metadata.create_all(bind=engine)



class User(Model):
    __tablename__="users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password_hash = Column(String(100), nullable=False)
    avatar = Column(String(100))
    created_on = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))
    verification_key = Column(String(4), nullable=False)
    verified = Column(Integer, default=0)
    notification_key = Column(String(100))
    account_type = Column(Integer, default=1)
    target_amount = Column(Float)
    target_date = Column(Date)

    incomings = relationship("Incoming", back_populates="user", cascade="all, delete-orphan")
    outgoings = relationship("Outgoing", back_populates="user", cascade="all, delete-orphan")
    savings = relationship("Saving", back_populates="user", cascade="all, delete-orphan")
    daily_spends = relationship("DailySpend", back_populates="user", cascade="all, delete-orphan")

class Incoming(Model):
    __tablename__ = "incomings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(100), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    frequency = Column(Enum("Monthly", "Yearly", "Weekly", "Daily"), nullable=False)
    created_on = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))

    user = relationship("User", back_populates="incomings")

class Outgoing(Model):
    __tablename__ = "outgoings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(100), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    frequency = Column(Enum("Monthly", "Yearly", "Weekly", "Daily"), nullable=False)
    created_on = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))

    user = relationship("User", back_populates="outgoings")

class Saving(Model):
    __tablename__ = "savings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(100), nullable=False)
    current_amount = Column(DECIMAL(10, 2), default=0)
    created_on = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))

    user = relationship("User", back_populates="savings")

class DailySpend(Model):
    __tablename__ = "daily_spends"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(100))
    amount = Column(DECIMAL(10, 2), nullable=False)
    spend_date = Column(Date, nullable=False)
    created_on = Column(DateTime, default=lambda: datetime.now(tz=timezone.utc))

    user = relationship("User", back_populates="daily_spends")
