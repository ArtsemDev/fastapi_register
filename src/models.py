from sqlalchemy import Column, INT, VARCHAR, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    id = Column(INT, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(VARCHAR(128), nullable=False)
    is_active = Column(BOOLEAN, default=False)


class UserSession(Base):
    id = Column(VARCHAR(128), primary_key=True)
    user_id = Column(INT, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User')


class UserEmailVerify(Base):
    id = Column(VARCHAR(128), primary_key=True)
    user_id = Column(INT, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User')
