from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

class ChunkingService:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def chunk_text(self, text: str) -> List[str]:
        """Split a single document into text chunks."""
        return self.splitter.split_text(text)

    def chunk_documents(self, docs: List[str]) -> List[List[str]]:
        """Split multiple documents into chunks."""
        return [self.chunk_text(doc) for doc in docs]
