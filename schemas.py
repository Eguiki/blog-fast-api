from pydantic import BaseModel, ConfigDict

class PostCreate(BaseModel):
    title: str
    text: str

class PostResponse(BaseModel):
    id: int
    title: str
    text: str

    model_config = ConfigDict(from_attributes=True)
