from pydantic import BaseModel


class Document(BaseModel):
    id: str | None = None
    title: str
    text: str
    metadata: dict | None = None
