from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.models import User
from app.pdf_generator import generate_letter_pdf
from app.routes.auth import get_current_user

router = APIRouter(prefix="/letters", tags=["letters"])


@router.post("/generate")
def generate_letter(
    request: schemas.LetterGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    promoters = crud.get_promoters_by_identifier(
    db,
    request.promoter_employee_id,
)

    if not promoters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum promotor ativo foi encontrado para a matrícula ou CPF informado.",
        )

    if len(promoters) > 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Há mais de um promotor com este CPF. Solicite a correção cadastral.",
        )

    promoter = promoters[0]

    store = crud.get_store_by_code(db, request.store_code)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found for the given code",
        )

    pdf_bytes = generate_letter_pdf(promoter, store, request.letter_date)

    # Registra no histórico quem gerou, para quem, e quando -- mesmo que o
    # PDF em si não seja salvo em disco, este registro serve de auditoria.
    crud.create_letter_log(db, {
        "user_id": current_user.id,
        "user_name": current_user.name,
        "promoter_id": promoter.id,
        "promoter_name": promoter.name,
        "promoter_employee_id": promoter.employee_id,
        "store_id": store.id,
        "store_code": store.code,
        "store_name": store.name,
        "letter_date": request.letter_date,
        "generated_at": datetime.now(timezone.utc),
    })

    filename = f"carta_{promoter.employee_id}_{store.code}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
    

@router.get("/history", response_model=list[schemas.LetterLogOut])
def get_letter_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Admin vê tudo; usuário comum vê só as próprias cartas geradas.
    user_id_filter = None if current_user.is_admin else current_user.id
    return crud.list_letter_logs(db, user_id=user_id_filter)


@router.get("/report", response_model=schemas.LetterReportOut)
def get_letter_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_id_filter = None if current_user.is_admin else current_user.id

    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = start_of_day - timedelta(days=now.weekday())  # segunda-feira
    start_of_month = start_of_day.replace(day=1)

    return {
        "today": crud.count_letters_since(db, start_of_day, user_id_filter),
        "this_week": crud.count_letters_since(db, start_of_week, user_id_filter),
        "this_month": crud.count_letters_since(db, start_of_month, user_id_filter),
    }