from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from psycopg.rows import dict_row
from db.connection import get_conn
from api.models import TaskCreate, TaskResponse

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    sql = """
        INSERT INTO tasks (task_type, payload)
        VALUES (%s, %s)
        RETURNING *
    """
    async with get_conn() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(sql, [task.task_type, task.payload])
            row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return row

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: UUID):
    sql = "SELECT * FROM tasks WHERE id = %s"
    async with get_conn() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(sql, [str(task_id)])
            row = await cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return row


@router.get("/tasks", response_model=list[TaskResponse])
async def list_tasks(status: str | None = Query(default=None)):
    if status:
        sql = "SELECT * FROM tasks WHERE status = %s ORDER BY created_at DESC"
        params = [status]
    else:
        sql = "SELECT * FROM tasks ORDER BY created_at DESC"
        params = []
    async with get_conn() as conn:
        async with conn.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(sql, params)
            rows = await cursor.fetchall()
    return rows
