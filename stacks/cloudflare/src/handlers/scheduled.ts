/**
 * Scheduled Handler for cron triggers
 */
import type { Env } from '../types';

// Cron patterns for routing
export const CRON_PATTERNS = {
  DAILY_DIGEST: '0 8 * * *',
  PRICE_CHECK: '0 */4 * * *',
} as const;

/**
 * Handle scheduled cron events
 */
export async function handleScheduled(
  event: ScheduledEvent,
  env: Env,
  ctx: ExecutionContext
): Promise<void> {
  console.log(`[scheduled] Cron triggered: ${event.cron}`);
  console.log(`[scheduled] Scheduled time: ${new Date(event.scheduledTime).toISOString()}`);

  try {
    // Route by cron pattern
    switch (event.cron) {
      case CRON_PATTERNS.DAILY_DIGEST:
        await runDailyDigest(env, ctx);
        break;
      case CRON_PATTERNS.PRICE_CHECK:
        await runPriceCheck(env, ctx);
        break;
      default:
        console.log(`[scheduled] Running default task for pattern: ${event.cron}`);
        await runDefaultTask(event, env, ctx);
    }
  } catch (error) {
    // Log errors but don't throw - prevents batch failures
    console.error(`[scheduled] Error in cron ${event.cron}:`, error);
  }
}

/**
 * Daily digest task - runs at 8 AM
 */
async function runDailyDigest(env: Env, ctx: ExecutionContext): Promise<void> {
  console.log('[scheduled] Running daily digest task');

  // Example: Access bindings
  // const db = env.DB;
  // const cache = env.CACHE;

  // Add your daily digest logic here
}

/**
 * Price check task - runs every 4 hours
 */
async function runPriceCheck(env: Env, ctx: ExecutionContext): Promise<void> {
  console.log('[scheduled] Running price check task');

  // Add your price check logic here
}

/**
 * Default task for unrecognized cron patterns
 */
async function runDefaultTask(
  event: ScheduledEvent,
  env: Env,
  ctx: ExecutionContext
): Promise<void> {
  console.log(`[scheduled] Default task executed at: ${new Date().toISOString()}`);
}

export { runDailyDigest, runPriceCheck };
