from pydantic import BaseModel


class CreateURLInput(BaseModel):
    target_url: str


class CreateURLOutput(BaseModel):
    shortened_url: str
