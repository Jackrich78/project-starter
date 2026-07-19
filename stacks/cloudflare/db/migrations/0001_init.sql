-- Initial migration: Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  payload TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  attempts INTEGER NOT NULL DEFAULT 0,
  created_at INTEGER NOT NULL,
  updated_at INTEGER NOT NULL
);

-- Index for querying by status
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);

-- Index for querying by type
CREATE INDEX IF NOT EXISTS idx_tasks_type ON tasks(type);
