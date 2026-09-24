from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas

from app.database import get_db
from app.models import User
from app.security import create_access_token, decode_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # O OAuth2 usa o campo "username",
    # mas neste sistema ele representa o CPF.
    cpf = "".join(filter(str.isdigit, form_data.username))

    if len(cpf) != 11:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.cpf == cpf).first()

    if not user or not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário desativado",
        )

    access_token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None or not user.active:
        raise credentials_exception

    return user


def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can perform this action",
        )

    return current_user


@router.get("/me", response_model=schemas.UserOut)
def read_current_user(
    current_user: User = Depends(get_current_user)
):
    return current_user
