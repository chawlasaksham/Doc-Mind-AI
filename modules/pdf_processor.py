"""
PDF Document Processor for Doc-Mind AI
Handles text extraction, page breakdown, metadata analysis, and chunking for RAG.
"""
import io
from typing import Dict, Any, List, Union
from pypdf import PdfReader
from config import RAG_CHUNK_SIZE, RAG_CHUNK_OVERLAP


class PDFProcessor:
    def __init__(self, chunk_size: int = RAG_CHUNK_SIZE, chunk_overlap: int = RAG_CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def process_pdf(self, file_source: Union[str, bytes, io.BytesIO], filename: str = "document.pdf") -> Dict[str, Any]:
        """
        Extracts text, metadata, page details, and chunks from a PDF.
        """
        if isinstance(file_source, bytes):
            stream = io.BytesIO(file_source)
        elif isinstance(file_source, str):
            stream = open(file_source, "rb")
        else:
            stream = file_source

        reader = PdfReader(stream)
        num_pages = len(reader.pages)
        pages_content = []
        full_text_list = []

        total_words = 0
        total_chars = 0

        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            # Basic cleanup: normalize multiple spaces
            cleaned_text = " ".join(page_text.split())
            word_count = len(cleaned_text.split())
            char_count = len(cleaned_text)

            total_words += word_count
            total_chars += char_count

            pages_content.append({
                "page_number": idx + 1,
                "text": cleaned_text,
                "raw_text": page_text,
                "word_count": word_count,
                "char_count": char_count,
            })
            if cleaned_text:
                full_text_list.append(f"--- Page {idx + 1} ---\n{cleaned_text}")

        full_text = "\n\n".join(full_text_list)
        chunks = self._chunk_document(pages_content, filename)

        return {
            "filename": filename,
            "total_pages": num_pages,
            "total_words": total_words,
            "total_chars": total_chars,
            "full_text": full_text,
            "pages": pages_content,
            "chunks": chunks,
            "is_empty": total_words < 5,
        }

    def _chunk_document(self, pages_content: List[Dict[str, Any]], filename: str) -> List[Dict[str, Any]]:
        """
        Splits document into sliding window chunks while preserving page provenance.
        """
        chunks = []
        chunk_id = 0

        for page in pages_content:
            page_num = page["page_number"]
            text = page["text"]
            if not text:
                continue

            words = text.split()
            if len(words) <= self.chunk_size:
                chunks.append({
                    "id": f"chunk_{chunk_id}",
                    "source": filename,
                    "page": page_num,
                    "text": text,
                    "word_count": len(words),
                })
                chunk_id += 1
            else:
                # Sliding window over words
                start = 0
                step = max(self.chunk_size - self.chunk_overlap, 50)
                while start < len(words):
                    end = min(start + self.chunk_size, len(words))
                    chunk_text = " ".join(words[start:end])
                    chunks.append({
                        "id": f"chunk_{chunk_id}",
                        "source": filename,
                        "page": page_num,
                        "text": chunk_text,
                        "word_count": end - start,
                    })
                    chunk_id += 1
                    if end == len(words):
                        break
                    start += step

        return chunks
