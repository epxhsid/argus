from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ingestion.chunking.chunker import DocumentChunking
from ingestion.database.chunk import ChunkPersistence
from ingestion.database.document import DocumentPersistence
from ingestion.extraction.pdf import PDFExtractor


class IngestionPipeline:
    def __init__(self, session: AsyncSession):
        self.extractor = PDFExtractor()
        self.chunker = DocumentChunking()
        self.documents = DocumentPersistence(session)
        self.chunks = ChunkPersistence(session)
        self.session = session


    async def ingest(self, *, d_id: UUID, fname: str, ctype: str, src_uri: str, path: str) -> None:
        document = self.extractor.extract(
            document_id=d_id,
            filename=fname,
            content_type=ctype,
            source_uri=src_uri,
            path=path,
        )

        chunks = self.chunker.chunk(document)

        async with self.session.begin():
            await self.documents.create(document)
            await self.session.flush()
            await self.chunks.create_many(chunks)
