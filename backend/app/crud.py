import re

from sqlalchemy import func
from typing import Optional

from sqlalchemy.orm import Session
from datetime import datetime

from app.models import LetterLog, Promoter, Store, User
from app.security import hash_password


def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session) -> list[User]:
    return db.query(User).all()


def normalize_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf)


def create_user(
    db: Session,
    name: str,
    username: str,
    cpf: str,
    password: str,
    is_admin: bool = False,
) -> User:
    
    cpf = normalize_cpf(cpf)
    
    user = User(
        name=name,
        username=username,
        cpf=cpf,
        password_hash=hash_password(password),
        is_admin=is_admin,
        active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user: User, data: dict) -> User:
    # Se uma nova senha foi enviada, ela precisa virar hash antes de
    # gravar -- por isso tratamos esse campo separado dos demais.
    if "password" in data:
        password = data.pop("password")
        user.password_hash = hash_password(password)

    for field, value in data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    user.active = False
    db.commit()


def get_promoter(db: Session, promoter_id: int) -> Optional[Promoter]:
    return db.query(Promoter).filter(Promoter.id == promoter_id).first()


def get_promoter_by_employee_id(db: Session, employee_id: str) -> Optional[Promoter]:
    return db.query(Promoter).filter(
        Promoter.employee_id == employee_id,
        Promoter.active == True,
    ).first()


def list_promoters(db: Session, skip: int = 0, limit: int = 100) -> list[Promoter]:
    return db.query(Promoter).offset(skip).limit(limit).all()


def create_promoter(db: Session, data: dict) -> Promoter:
    promoter = Promoter(**data)
    db.add(promoter)
    db.commit()
    db.refresh(promoter)
    return promoter


def update_promoter(db: Session, promoter: Promoter, data: dict) -> Promoter:
    for field, value in data.items():
        setattr(promoter, field, value)
    db.commit()
    db.refresh(promoter)
    return promoter


def delete_promoter(db: Session, promoter: Promoter) -> None:
    promoter.active = False
    db.commit()
    

def get_promoters_by_identifier(
    db: Session,
    identifier: str,
) -> list[Promoter]:
    identifier = identifier.strip()

    # Matrícula tem prioridade e já é única no banco.
    promoter = (
        db.query(Promoter)
        .filter(
            Promoter.employee_id == identifier,
            Promoter.active == True,
        )
        .first()
    )

    if promoter:
        return [promoter]

    # CPF pode ser informado com ou sem pontos e hífen.
    cpf_digits = re.sub(r"\D", "", identifier)

    if len(cpf_digits) != 11:
        return []

    return (
        db.query(Promoter)
        .filter(
            Promoter.active == True,
            func.regexp_replace(Promoter.cpf, r"\D", "", "g") == cpf_digits,
        )
        .all()
    )


def get_store(db: Session, store_id: int) -> Optional[Store]:
    return db.query(Store).filter(Store.id == store_id).first()


def get_store_by_code(db: Session, code: str) -> Optional[Store]:
    return db.query(Store).filter(
        Store.code == code,
        Store.active == True,
    ).first()


def list_stores(db: Session, skip: int = 0, limit: int = 100) -> list[Store]:
    return db.query(Store).offset(skip).limit(limit).all()


def create_store(db: Session, data: dict) -> Store:
    store = Store(**data)
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


def update_store(db: Session, store: Store, data: dict) -> Store:
    for field, value in data.items():
        setattr(store, field, value)
    db.commit()
    db.refresh(store)
    return store


def delete_store(db: Session, store: Store) -> None:
    store.active = False
    db.commit()
    

def create_letter_log(db: Session, data: dict) -> LetterLog:
    letter_log = LetterLog(**data)
    db.add(letter_log)
    db.commit()
    db.refresh(letter_log)
    return letter_log


def list_letter_logs(db: Session, user_id: Optional[int] = None) -> list[LetterLog]:
    query = db.query(LetterLog).order_by(LetterLog.generated_at.desc())
    if user_id is not None:
        query = query.filter(LetterLog.user_id == user_id)
    return query.all()


def count_letters_since(db: Session, since: datetime, user_id: Optional[int] = None) -> int:
    query = db.query(LetterLog).filter(LetterLog.generated_at >= since)
    if user_id is not None:
        query = query.filter(LetterLog.user_id == user_id)
    return query.count()