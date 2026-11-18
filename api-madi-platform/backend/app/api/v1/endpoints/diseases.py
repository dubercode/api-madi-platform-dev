
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.disease import Disease
from app.schemas.disease import (
    DiseaseCreate,
    DiseaseResponse,
    DiseaseUpdate,
)


router = APIRouter(
    prefix="/diseases",
    tags=["Diseases"],
)


# CREATE
@router.post(
    "",
    response_model=DiseaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_disease(
    payload: DiseaseCreate,
    db: Session = Depends(get_db),
):

    disease = Disease(**payload.model_dump())

    db.add(disease)

    try:
        db.commit()
        db.refresh(disease)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A disease with this slug already exists",
        )

    return disease


# READ ALL
@router.get(
    "",
    response_model=list[DiseaseResponse],
)
def get_diseases(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):

    if skip < 0 or limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Invalid pagination parameters",
        )

    statement = (
        select(Disease)
        .offset(skip)
        .limit(limit)
        .order_by(Disease.id)
    )

    return db.scalars(statement).all()


# READ BY ID
@router.get(
    "/{disease_id}",
    response_model=DiseaseResponse,
)
def get_disease(
    disease_id: int,
    db: Session = Depends(get_db),
):

    disease = db.get(Disease, disease_id)

    if disease is None:
        raise HTTPException(
            status_code=404,
            detail="Disease not found",
        )

    return disease


# UPDATE
@router.patch(
    "/{disease_id}",
    response_model=DiseaseResponse,
)
def update_disease(
    disease_id: int,
    payload: DiseaseUpdate,
    db: Session = Depends(get_db),
):

    disease = db.get(Disease, disease_id)

    if disease is None:
        raise HTTPException(
            status_code=404,
            detail="Disease not found",
        )

    updates = payload.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(disease, field, value)

    try:
        db.commit()
        db.refresh(disease)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="A disease with this slug already exists",
        )

    return disease


# DELETE
@router.delete(
    "/{disease_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_disease(
    disease_id: int,
    db: Session = Depends(get_db),
):

    disease = db.get(Disease, disease_id)

    if disease is None:
        raise HTTPException(
            status_code=404,
            detail="Disease not found",
        )

    db.delete(disease)
    db.commit()

    return None
