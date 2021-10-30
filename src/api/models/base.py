from pydantic import BaseModel, Field
from bson import ObjectId
from bson.decimal128 import Decimal128


class PyObjectId(ObjectId):
    # * https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class DBBaseModel(BaseModel):
    # * https://pydantic-docs.helpmanual.io/usage/model_config/#change-behaviour-globally
    id: PyObjectId = Field(alias="_id", default_factory=PyObjectId)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, Decimal128: str}
