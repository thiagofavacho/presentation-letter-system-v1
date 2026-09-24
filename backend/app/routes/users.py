from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.models import User
from app.routes.auth import require_admin

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if crud.get_user_by_username(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já está em uso",
        )

    cpf = "".join(filter(str.isdigit, user_in.cpf))

    if len(cpf) != 11:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF deve conter 11 dígitos",
        )

    if db.query(User).filter(User.cpf == cpf).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF já está cadastrado",
        )

    user = crud.create_user(
        db=db,
        name=user_in.name,
        username=user_in.username,
        cpf=cpf,
        password=user_in.password,
        is_admin=user_in.is_admin,
    )

    return user


@router.get("/", response_model=list[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return crud.get_users(db)


@router.patch("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    update_data = user_in.model_dump(exclude_unset=True)

    # Evita username duplicado, caso esteja sendo alterado.
    if "username" in update_data and update_data["username"] != user.username:
        if crud.get_user_by_username(db, update_data["username"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already in use",
            )

    return crud.update_user(db, user, update_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    crud.delete_user(db, user)