import asyncio
from pathlib import Path
from uuid import uuid4

from ingestion.database.engine import session_factory
from ingestion.pipeline import IngestionPipeline


async def ingest(path: str) -> None:
    file_path = Path(path)

    if not file_path.exists(): raise FileNotFoundError(file_path)
    if file_path.suffix.lower() != ".pdf": raise ValueError("Only PDF files are supported, for now")

    document_id = uuid4()

    async with session_factory() as session:
        pipeline = IngestionPipeline(session)

        await pipeline.ingest(
            d_id=document_id,
            fname=file_path.name,
            ctype="application/pdf",
            src_uri=f"file://{file_path.resolve()}",
            path=str(file_path),
        )

    print(f"Ingested {file_path.name}")
    print(f"Document ID: {document_id}")

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="process a document into the ingestion service"
    )

    parser.add_argument(
        "path",
        help="Path to the PDF",
    )

    args = parser.parse_args()

    asyncio.run(ingest(args.path))

if __name__ == "__main__":
    main()
