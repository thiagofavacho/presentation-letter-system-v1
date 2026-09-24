from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.importers import import_promoters
from app.database import get_db
from app.models import User
from app.routes.auth import require_admin

router = APIRouter(prefix="/promoters", tags=["promoters"])


@router.post("/import")
async def import_promoters_file(
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
        return import_promoters(db, content)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@router.post("/", response_model=schemas.PromoterOut, status_code=status.HTTP_201_CREATED)
def create_promoter(
    promoter_in: schemas.PromoterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return crud.create_promoter(db, promoter_in.model_dump())


@router.get("/", response_model=list[schemas.PromoterOut])
def list_promoters(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return crud.list_promoters(db, skip=skip, limit=limit)


@router.get("/{promoter_id}", response_model=schemas.PromoterOut)
def get_promoter(
    promoter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    promoter = crud.get_promoter(db, promoter_id)
    if not promoter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promoter not found")
    return promoter


@router.patch("/{promoter_id}", response_model=schemas.PromoterOut)
def update_promoter(
    promoter_id: int,
    promoter_in: schemas.PromoterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    promoter = crud.get_promoter(db, promoter_id)
    if not promoter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promoter not found")

    update_data = promoter_in.model_dump(exclude_unset=True)
    return crud.update_promoter(db, promoter, update_data)


@router.delete("/{promoter_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_promoter(
    promoter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    promoter = crud.get_promoter(db, promoter_id)
    if not promoter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promoter not found")
    crud.delete_promoter(db, promoter)
