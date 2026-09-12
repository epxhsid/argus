from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, select

from ingestion.database.models import ChunkModel
from ingestion.models.document import UUID, Chunk


class ChunkPersistence:
    def __init__(self, session: AsyncSession): self.session = session

    async def create_many(self, chunks: list[Chunk]) -> None:
        models = [
            ChunkModel(
                id=chunk.id,
                document_id=chunk.document_id,
                content=chunk.content,
                chunk_index=chunk.chunk_index,
                metadata_=chunk.metadata,
            )
            for chunk in chunks
        ]

        self.session.add_all(models)

    async def get_by_document(self, document_id: UUID) -> list[Chunk]:
        result = await self.session.execute(
            select(ChunkModel)
            .where(ChunkModel.document_id == document_id)
            .order_by(ChunkModel.chunk_index)
        )

        return [
            Chunk(
                id=model.id,
                document_id=model.document_id,
                content=model.content,
                chunk_index=model.chunk_index,
                metadata=model.metadata_,
            )
            for model in result.scalars()
        ]

    async def delete_by_document(self, document_id: UUID) -> None:
        await self.session.execute(
            delete(ChunkModel).where(ChunkModel.document_id == document_id)
        )
