/**
 * Environment bindings for the Cloudflare Worker
 *
 * All resource bindings are optional - enable in wrangler.toml as needed.
 * The scaffold works without any bindings configured.
 */
export interface Env {
  // Queue for async task processing (requires Workers Paid plan)
  TASKS?: Queue<QueueMessage>;

  // D1 database (uncomment in wrangler.toml to enable)
  DB?: D1Database;

  // R2 object storage (uncomment in wrangler.toml to enable)
  STORAGE?: R2Bucket;

  // KV key-value store (uncomment in wrangler.toml to enable)
  CACHE?: KVNamespace;

  // Environment variables
  SLACK_SIGNING_SECRET: string;
  ENVIRONMENT: string;
}

/**
 * Message structure for queue processing
 */
export interface QueueMessage {
  type: string;
  payload: unknown;
  timestamp: number;
  id: string;
}
