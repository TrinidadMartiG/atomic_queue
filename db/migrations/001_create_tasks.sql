-- Migration 001: Create tasks table
-- Concept: atomic task claiming with SELECT FOR UPDATE SKIP LOCKED

CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT now(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    worker_id VARCHAR(100),
    result JSONB,
    error TEXT,

    CONSTRAINT valid_status CHECK (status IN ('pending', 'running', 'completed', 'failed'))
);

-- Partial index: only indexes pending tasks (the ones workers query)
-- Workers never query completed/failed tasks, so we skip them in the index
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status) WHERE status = 'pending';
