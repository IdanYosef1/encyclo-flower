from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from models.helpers import observation_id_generator, gen_uuid, gen_image_file_name
from models.generic import Coordinates, ImageLocationText, ImagePreview
from models.custom_types import (
    HebMonthLiteral,
    LocationHebLiteral,
    ImageContentCategoryLiteral,
)
from models.user import BaseUserOut


class Observation(BaseModel):
    observation_text: str = Field(min_length=5, max_length=2000)


class ObservationInResponse(BaseModel):
    """
    response for added new observation.
    """

    observation_id: str


class ObservationImageMeta(ImageLocationText):
    description: str | None = None
    content_category: ImageContentCategoryLiteral | None = None
    month_taken: Optional[HebMonthLiteral | None] = Field(
        None, description="Hebrew month"
    )
    location_name: LocationHebLiteral | None = None
    plant_id: Optional[None | str] = Field(
        None,
        example=None,
        description="Plant ID",
        nullable=True,
    )


class ObservationImageInDB(ObservationImageMeta):
    # TODO: merge this class with QuestionImageInDB - if possible
    image_id: str = Field(default_factory=gen_uuid)
    coordinates: Coordinates = Coordinates(lat=0, lon=0, alt=0)
    orig_file_name: str = Field(default="image1.jpg")
    file_name: str | None = None
    created_dt: datetime = Field(default_factory=datetime.utcnow)

    @validator("file_name", pre=True, always=True)
    def set_file_name(cls, v, values):
        if not v:
            return gen_image_file_name(values["orig_file_name"])
        return v


class ObservationImageOut(ObservationImageMeta):
    image_id: str
    file_name: str


class ObservationImageInDB_w_oid(BaseModel):
    observation_id: str
    image: ObservationImageMeta


class ObservationInDB(Observation):
    observation_id: str = Field(default_factory=observation_id_generator)
    images: List[ObservationImageInDB] = []
    user_id: str
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    submitted: bool = False
    deleted: bool = False


class ObservationOut(ObservationInDB):
    user_data: BaseUserOut


class ObservationPreviewBase(BaseModel):
    observation_id: str
    observation_text: str
    image: ImagePreview | None
    created_dt: datetime


class ObservationsPreview(ObservationPreviewBase):
    user_id: str
    username: str
