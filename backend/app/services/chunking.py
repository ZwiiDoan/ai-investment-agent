from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

    def chunk_text(self, text: str) -> list[str]:
        """Split a single document into text chunks."""
        return self.splitter.split_text(text)

    def chunk_documents(self, docs: list[str]) -> list[list[str]]:
        """Split multiple documents into chunks."""
        return [self.chunk_text(doc) for doc in docs]
