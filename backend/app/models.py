from sqlalchemy import Boolean, Column, DateTime, Integer, String
from datetime import datetime

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    username = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )
    
    cpf = Column(
        String(11),
        unique=True,
        nullable=True,
        index=True
    )

    password_hash = Column(String(255), nullable=False)

    is_admin = Column(
        Boolean,
        default=False,
        nullable=False
    )

    active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class Promoter(Base):
    __tablename__ = "promoters"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False
    )

    employee_id = Column(
        String(50),
        nullable=False,
        index=True
    )

    cpf = Column(String(20))

    rg = Column(String(30))

    ctps = Column(String(50))

    pis = Column(String(50))

    address = Column(String(300))

    neighborhood = Column(String(150))

    city = Column(String(100))

    state = Column(String(2))

    cep = Column(String(10))

    admission_date = Column(DateTime)

    position = Column(
        String(100),
        default="PROMOTOR"
    )

    period = Column(
        String(50),
        default="INDETERMINADO"
    )

    company = Column(
        String(150),
        default="SB SERVICOS TEMPORARIOS LTDA"
    )

    active = Column(
        Boolean,
        default=True
    )


class Store(Base):
    __tablename__ = "stores"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String(200),
        nullable=False
    )

    address = Column(
        String(300)
    )

    neighborhood = Column(
        String(150)
    )

    city = Column(
        String(100)
    )

    state = Column(
        String(2)
    )

    client = Column(
        String(150)
    )

    active = Column(
        Boolean,
        default=True
    )


class LetterLog(Base):
    __tablename__ = "letter_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False
    )

    user_name = Column(
        String(150),
        nullable=False
    )

    promoter_id = Column(
        Integer,
        nullable=False
    )

    promoter_name = Column(
        String(150),
        nullable=False
    )

    promoter_employee_id = Column(
        String(50),
        nullable=False
    )

    store_id = Column(
        Integer,
        nullable=False
    )

    store_code = Column(
        String(50),
        nullable=False
    )

    store_name = Column(
        String(200),
        nullable=False
    )

    letter_date = Column(
        DateTime,
        nullable=False
    )

    generated_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )