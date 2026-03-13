/**
 * Database service using Drizzle ORM
 */
import { drizzle, DrizzleD1Database } from 'drizzle-orm/d1';

/**
 * Create a Drizzle client from D1 binding
 *
 * @param d1 - D1 database binding
 * @returns Drizzle D1 database client
 */
export function getDb(d1: D1Database): DrizzleD1Database {
  return drizzle(d1);
}
