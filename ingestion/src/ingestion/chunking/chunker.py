import re

from ingestion.models.document import Chunk, Document


class DocumentChunking:
    def __init__(self, *, max_characters: int = 2000, overlap_characters: int = 200):


        self.max_characters = max_characters
        self.overlap_characters = overlap_characters

    # chunks documents into manageable chunks as LLM readable segments
    def chunk(self, document: Document) -> list[Chunk]:
        chunks: list[Chunk] = []

        # only splits large paragraphs in the case that the
        # max characters of a paragraph has exceeded its limit
        for page in document.pages:
            paragraphs = self._split_paragraphs(page.text)

            for paragraph in paragraphs:
                if len(paragraph) <= self.max_characters:
                    chunks.append(
                        Chunk(
                            document_id=document.id,
                            content=paragraph,
                            chunk_index=len(chunks),
                            metadata={
                                "page_start": page.number,
                                "page_end": page.number,
                            }
                        )
                    )
                else:
                    chunks.extend(
                        self._split_large_paragraph(
                            document_id=document.id,
                            text=paragraph,
                            page_number=page.number,
                            starting_index=len(chunks),
                        )
                    )

        return chunks



    # splits text by double linebreaks (including lines with only spaces)
    # filters out empty matches caused by consecutive line breaks.
    @staticmethod
    def _split_paragraphs(text: str) -> list[str]:
        return [
            paragraph.strip()
            # \n = matches the newline character at the end of the first paragraph
            # \s* = matches zero or more whitespace characters (such as spaces or tabs) on the blank line
            # \n = matches the newline character that starts the next paragraph
            for paragraph in re.split(r"\n\s*\n", text)
            if paragraph.strip()
        ]

    # this method breaks down paragraphs into chunks, and ensures that no chunk exceeds a maximum character limit
    # while maintaining text overlap between consecutive chunks so no context is lost, as defined by init definition
    def _split_large_paragraph(self, *, document_id, text: str, page_number: int, starting_index: int) -> list[Chunk]:
        chunks: list[Chunk] = []
        start = 0
        text_len = len(text)

        # it calculates the target and end position for the given chunk (end = start + max.characters)
        # It extracts that section of text (text[start:end]) and cleans up any trailing spaces using .strip().
        while start < text_len:
            end = start + self.max_characters

            if end < text_len:
                space_index = text.rfind(" ", start, end)
                if space_index != -1 and space_index > start:
                    end = space_index

            chunk_text = text[start:end].strip()

            # appends the chunk into the list
            # each chunk gets a unique sequential ID (starting_index + len(chunks)
            # given if the sentence argument has more text left,
            # it moves the start pointer forward, but subtracts the self.overlap_characters
            if chunk_text:
                chunks.append(
                    Chunk(
                        document_id=document_id,
                        content=chunk_text,
                        chunk_index=starting_index + len(chunks),
                        metadata={
                            "page_start": page_number,
                            "page_end": page_number,
                        },
                    )
                )

            if end >= text_len:
                break

            next_start = end - self.overlap_characters
            if next_start <= start:
                start = end
            else:
                start = next_start

        return chunks
