/**
 * Drizzle schema for D1 database
 */
import { sqliteTable, text, integer } from 'drizzle-orm/sqlite-core';

/**
 * Tasks table - stores queued tasks and their status
 */
export const tasks = sqliteTable('tasks', {
  id: text('id').primaryKey(),
  type: text('type').notNull(),
  payload: text('payload').notNull(), // JSON stringified
  status: text('status').notNull().default('pending'),
  attempts: integer('attempts').notNull().default(0),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull(),
  updatedAt: integer('updated_at', { mode: 'timestamp' }).notNull(),
});

export type Task = typeof tasks.$inferSelect;
export type NewTask = typeof tasks.$inferInsert;
