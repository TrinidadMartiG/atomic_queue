"""
Database connection pool.

Shared by the API server and workers. Each process creates its own pool —
do not share a pool across processes, only across coroutines within one process.
"""
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool

load_dotenv()

_pool: AsyncConnectionPool | None = None


def _build_conninfo() -> str:
    return (
        f"dbname={os.getenv('DB_NAME')} "
        f"user={os.getenv('DB_USER')} "
        f"password={os.getenv('DB_PASSWORD')} "
        f"host={os.getenv('DB_HOST')} "
        f"port={os.getenv('DB_PORT')}"
    )


async def init_pool() -> None:
    """Call once at process startup (FastAPI lifespan or worker __main__)."""
    global _pool

    _pool = AsyncConnectionPool(
        conninfo=_build_conninfo(),
        min_size=1,
        max_size=5,
        open=True,
        timeout=30,
        )


async def close_pool() -> None:
    """Call on process shutdown for graceful cleanup."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


@asynccontextmanager
async def get_conn():
    """
    Async context manager — borrows a connection from the pool and returns it.

    Usage:
        async with get_conn() as conn:
            await conn.execute("SELECT ...")
    """
    if _pool is None:
        raise RuntimeError("Pool not initialized. Call init_pool() first.")
    async with _pool.connection() as conn:
        yield conn
