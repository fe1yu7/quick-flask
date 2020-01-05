from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, DateTime, Integer
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship, backref

from ext import db


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True)
    phone = Column(VARCHAR(20), nullable=True)
    nickname = Column(VARCHAR(30))
    is_able = Column(TINYINT, nullable=False, default=1, comment="是否启用")
    salt = Column(VARCHAR(30), comment="密码加盐")
    password = Column(VARCHAR(61))


class UserInfo(db.Model):
    __tablename__ = "user_info"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    unique_id = Column(VARCHAR(8), unique=True, nullable=False)
    birth_date = Column(DateTime, nullable=True)
    head_url = Column(VARCHAR(50), server_default="")
    gender = Column(TINYINT, comment="0 female 1 male")

    user = relationship("User", backref=backref(""), lazy="select")


class UserPhoneCode(db.Model):
    __tablename__ = "user_phone_code"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    code = Column(VARCHAR(6))
    create_time = Column(Integer)
    update_time = Column(Integer)
    valid_time = Column(Integer)
    position = Column(VARCHAR(30))


