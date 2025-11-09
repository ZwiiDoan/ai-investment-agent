import uuid

from psycopg2.extras import Json
from psycopg2.pool import SimpleConnectionPool

from app.core.settings import settings
from app.models import Document

# Connection pool (min 1, max 5 connections for dev)
_pool = SimpleConnectionPool(
    1,
    5,
    dbname=settings.pgvector_db,
    user=settings.pgvector_user,
    password=settings.pgvector_password,
    host=settings.pgvector_host,
    port=settings.pgvector_port,
)


def _get_conn():
    return _pool.getconn()


def _put_conn(conn):
    _pool.putconn(conn)


def _init_schema():
    conn = _get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS raw_documents (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    text TEXT NOT NULL,
                    metadata JSONB,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                );
                """
            )
            cur.execute(
                "CREATE INDEX IF NOT EXISTS idx_raw_documents_title ON raw_documents(title);"
            )
    finally:
        _put_conn(conn)


_init_schema()


def save_document(doc: Document) -> Document:
    if not doc.id:
        doc.id = str(uuid.uuid4())
    conn = _get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO raw_documents (id, title, text, metadata)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET title = EXCLUDED.title, text = EXCLUDED.text, metadata = EXCLUDED.metadata
                """,
                (doc.id, doc.title, doc.text, Json(doc.metadata) if doc.metadata else None),
            )
        return doc
    finally:
        _put_conn(conn)


def get_document(doc_id: str) -> Document | None:
    conn = _get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, text, metadata FROM raw_documents WHERE id = %s",
                (doc_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            _id, title, text, metadata = row
            return Document(id=_id, title=title, text=text, metadata=metadata)
    finally:
        _put_conn(conn)


def delete_document(doc_id: str) -> bool:
    conn = _get_conn()
    try:
        with conn, conn.cursor() as cur:
            cur.execute("DELETE FROM raw_documents WHERE id = %s", (doc_id,))
            return cur.rowcount > 0
    finally:
        _put_conn(conn)


def list_documents(title_filter: str | None = None, limit: int = 50) -> list[Document]:
    conn = _get_conn()
    try:
        with conn, conn.cursor() as cur:
            if title_filter:
                cur.execute(
                    "SELECT id, title, text, metadata FROM raw_documents WHERE title ILIKE %s LIMIT %s",
                    (f"%{title_filter}%", limit),
                )
            else:
                cur.execute(
                    "SELECT id, title, text, metadata FROM raw_documents ORDER BY created_at DESC LIMIT %s",
                    (limit,),
                )
            rows = cur.fetchall()
            return [Document(id=r[0], title=r[1], text=r[2], metadata=r[3]) for r in rows]
    finally:
        _put_conn(conn)
