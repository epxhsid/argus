from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DocumentPage(BaseModel):
    number: int
    text: str

class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    filename: str
    content_type: str
    source_uri: str
    pages: list[DocumentPage] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class Chunk(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    document_id: UUID
    content: str
    chunk_index: int
    metadata: dict[str, Any] = Field(default_factory=dict)
