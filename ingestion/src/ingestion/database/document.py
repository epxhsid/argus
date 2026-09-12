from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ingestion.database.models import DocumentModel
from ingestion.models.document import Document


class DocumentPersistence:
    def __init__(self, session: AsyncSession): self.session = session

    async def create(self, document: Document) -> None:
        model = DocumentModel(
            id=document.id,
            filename=document.filename,
            content_type=document.content_type,
            source_uri=document.source_uri,
            metadata_=document.metadata,
        )

        self.session.add(model)

    async def get(self, document_id: UUID) -> Document | None:
        result = await self.session.execute(select(DocumentModel).where(DocumentModel.id == document_id))

        model = result.scalar_one_or_none()
        if model is None: return None

        return Document(
            id=model.id,
            filename=model.filename,
            content_type=model.content_type,
            source_uri=model.source_uri,
            metadata=model.metadata_,
        )

    async def delete(self, document_id: UUID) -> None:
        await self.session.execute(delete(DocumentModel).where(DocumentModel.id == document_id))
