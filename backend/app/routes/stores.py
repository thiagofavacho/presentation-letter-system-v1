from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.importers import import_stores
from app.database import get_db
from app.models import User
from app.routes.auth import require_admin, get_current_user

router = APIRouter(prefix="/stores", tags=["stores"])


@router.post("/import")
async def import_stores_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    if not (file.filename or "").lower().endswith(".xlsx"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Envie um arquivo .xlsx.")
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="O arquivo deve ter no máximo 10 MB.")
    try:
        return import_stores(db, content)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@router.post("/", response_model=schemas.StoreOut, status_code=status.HTTP_201_CREATED)
def create_store(
    store_in: schemas.StoreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return crud.create_store(db, store_in.model_dump())


@router.get("/", response_model=list[schemas.StoreOut])
def list_stores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return crud.list_stores(db, skip=skip, limit=limit)


@router.get("/{store_id}", response_model=schemas.StoreOut)
def get_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    store = crud.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    return store


@router.get("/code/{code}", response_model=schemas.StoreOut)
def get_store_by_code(
    code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    store = crud.get_store_by_code(db, code)

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loja não encontrada",
        )

    return store


@router.patch("/{store_id}", response_model=schemas.StoreOut)
def update_store(
    store_id: int,
    store_in: schemas.StoreUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    store = crud.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")

    update_data = store_in.model_dump(exclude_unset=True)
    return crud.update_store(db, store, update_data)


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(
    store_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    store = crud.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")
    crud.delete_store(db, store)
