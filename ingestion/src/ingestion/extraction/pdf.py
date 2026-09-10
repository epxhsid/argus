from typing import Any, cast

import pymupdf4llm

from ingestion.models.document import Document, DocumentPage


class PDFExtractor:
    def extract(self, *, document_id, filename: str, content_type: str, source_uri: str, path: str) -> Document:
        result = cast(
            list[dict[str, Any]],
            pymupdf4llm.to_markdown(path, page_chunks=True),
        )

        pages = [
            DocumentPage(
                number=index + 1,
                text=page["text"],
            )
            for index, page in enumerate(result)
        ]

        return Document(
            id=document_id,
            filename=filename,
            content_type=content_type,
            source_uri=source_uri,
            pages=pages,
            metadata={
                "page_count": len(result),
            },
        )
