from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DiseaseBase(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=150,
    )

    slug: str = Field(
        min_length=3,
        max_length=180,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    summary: str = Field(
        min_length=10,
        max_length=500,
    )

    description: str = Field(
        min_length=20,
    )


class DiseaseCreate(DiseaseBase):
    pass


class DiseaseUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=150,
    )

    slug: str | None = Field(
        default=None,
        min_length=3,
        max_length=180,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    summary: str | None = Field(
        default=None,
        min_length=10,
        max_length=500,
    )

    description: str | None = Field(
        default=None,
        min_length=20,
    )

    is_published: bool | None = None


class DiseaseResponse(DiseaseBase):

    id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)