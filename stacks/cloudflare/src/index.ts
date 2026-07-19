/**
 * Cloudflare Worker entry point - Multi-handler pattern
 *
 * Exports fetch, queue, and scheduled handlers for Workers.
 */
import { app } from './handlers/webhook';
import { handleQueueBatch } from './handlers/queue-consumer';
import { handleScheduled } from './handlers/scheduled';
import type { Env, QueueMessage } from './types';

export default {
  fetch: app.fetch,
  queue: handleQueueBatch,
  scheduled: handleScheduled,
};

// Re-export types for external use
export type { Env, QueueMessage };
export { app } from './handlers/webhook';
export { handleQueueBatch } from './handlers/queue-consumer';
export { handleScheduled, CRON_PATTERNS } from './handlers/scheduled';
