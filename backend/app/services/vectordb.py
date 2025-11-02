import psycopg2
from psycopg2.extras import execute_values, Json
from typing import List, Tuple, Optional
from app.core.settings import settings
from tenacity import retry, stop_after_attempt, wait_fixed

class VectorDBService:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=settings.pgvector_db,
            user=settings.pgvector_user,
            password=settings.pgvector_password,
            host=settings.pgvector_host,
            port=settings.pgvector_port
        )
        self._ensure_table()

    def _ensure_table(self):
        with self.conn, self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            cur.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id SERIAL PRIMARY KEY,
                    doc_id TEXT,
                    chunk_idx INT,
                    chunk TEXT,
                    embedding VECTOR(384),
                    metadata JSONB
                );
            ''')

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def insert_embeddings(self, doc_id: str, chunks: List[str], embeddings: List[List[float]], metadata: Optional[List[dict]] = None):
        if metadata is None:
            metadata = [{} for _ in chunks]

        # Build values converting embedding list to pgvector literal and metadata dict to JSON
        values = []
        for idx, (chunk, embedding, meta) in enumerate(zip(chunks, embeddings, metadata)):
            vector_literal = '[' + ','.join(f'{x:.8f}' for x in embedding) + ']'
            values.append((doc_id, idx, chunk, vector_literal, Json(meta)))

        with self.conn, self.conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO documents (doc_id, chunk_idx, chunk, embedding, metadata)
                VALUES %s
                """,
                values,
                template="(%s,%s,%s,%s::vector,%s)"
            )

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def query_similar(self, query_embedding: List[float], top_k: int = 3) -> List[Tuple[str, int, str, float, dict]]:
        # Convert embedding to pgvector literal string
        vector_literal = '[' + ','.join(f'{x:.8f}' for x in query_embedding) + ']'
        with self.conn, self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT doc_id, chunk_idx, chunk, embedding <#> %s::vector AS distance, metadata
                FROM documents
                ORDER BY embedding <#> %s::vector ASC
                LIMIT %s
                """,
                (vector_literal, vector_literal, top_k)
            )
            return cur.fetchall()

    def delete_embeddings(self, doc_id: str) -> int:
        """Delete all embeddings for a given doc_id. Returns number of rows deleted."""
        with self.conn, self.conn.cursor() as cur:
            cur.execute("DELETE FROM documents WHERE doc_id = %s", (doc_id,))
            return cur.rowcount