/**
 * Queue helper utilities
 */

const MAX_BACKOFF = 64; // Maximum backoff in seconds

/**
 * Calculate exponential backoff delay for retry attempts
 * Formula: 2^attempts, capped at MAX_BACKOFF
 *
 * @param attempts - Number of retry attempts (1-based)
 * @returns Delay in seconds
 */
export function backoff(attempts: number): number {
  return Math.min(Math.pow(2, attempts), MAX_BACKOFF);
}

export { MAX_BACKOFF };
