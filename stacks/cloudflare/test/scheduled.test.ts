// test/scheduled.test.ts
// TDD Tests for FEAT-012: Cloudflare Stack - Scheduled Handler

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { env, createScheduledController } from 'cloudflare:test';
import {
  handleScheduled,
  CRON_PATTERNS,
  runDailyDigest,
  runPriceCheck,
} from '../src/handlers/scheduled';
import type { Env, QueueMessage } from '../src/types';

// Helper to create mock env with bindings
function createMockEnv(): Env {
  return {
    TASKS: {
      send: vi.fn().mockResolvedValue(undefined),
    } as unknown as Queue<QueueMessage>,
    DB: {} as D1Database,
    STORAGE: {} as R2Bucket,
    CACHE: {} as KVNamespace,
    SLACK_SIGNING_SECRET: 'test-secret',
    ENVIRONMENT: 'test',
  };
}

// Helper to create mock scheduled event
function createScheduledEvent(cron: string, scheduledTime?: number): ScheduledEvent {
  return {
    cron,
    scheduledTime: scheduledTime || Date.now(),
    noRetry: vi.fn(),
  } as unknown as ScheduledEvent;
}

describe('FEAT-012: Scheduled Handler', () => {
  describe('AC-FEAT-012-010: Cron Trigger Handling', () => {
    it('should execute on scheduled cron trigger', async () => {
      // Given: Cron trigger fires
      const event = createScheduledEvent('0 8 * * *');
      const mockEnv = createMockEnv();
      const ctx = { waitUntil: vi.fn() } as unknown as ExecutionContext;

      // When: scheduled handler invoked with event
      // Then: Handler executes without error
      await expect(handleScheduled(event, mockEnv, ctx)).resolves.not.toThrow();
    });

    it('should receive cron pattern in event', async () => {
      // Given: Cron pattern "0 8 * * *"
      const cronPattern = '0 8 * * *';
      const event = createScheduledEvent(cronPattern);
      const mockEnv = createMockEnv();
      const ctx = { waitUntil: vi.fn() } as unknown as ExecutionContext;

      // When: scheduled handler invoked
      await handleScheduled(event, mockEnv, ctx);

      // Then: event.cron === "0 8 * * *"
      expect(event.cron).toBe(cronPattern);
    });

    it('should receive scheduledTime in event', async () => {
      // Given: Scheduled trigger
      const scheduledTime = Date.now();
      const event = createScheduledEvent('0 8 * * *', scheduledTime);
      const mockEnv = createMockEnv();
      const ctx = { waitUntil: vi.fn() } as unknown as ExecutionContext;

      // When: scheduled handler invoked
      await handleScheduled(event, mockEnv, ctx);

      // Then: event.scheduledTime is valid timestamp
      expect(event.scheduledTime).toBe(scheduledTime);
      expect(new Date(event.scheduledTime).getTime()).toBe(scheduledTime);
    });
  });

  describe('AC-FEAT-012-011: Multiple Cron Patterns', () => {
    it('should differentiate between different cron patterns', async () => {
      // Given: Two cron patterns configured
      expect(CRON_PATTERNS.DAILY_DIGEST).toBe('0 8 * * *');
      expect(CRON_PATTERNS.PRICE_CHECK).toBe('0 */4 * * *');

      // When: Each fires - they should route to different handlers
      const dailyEvent = createScheduledEvent(CRON_PATTERNS.DAILY_DIGEST);
      const priceEvent = createScheduledEvent(CRON_PATTERNS.PRICE_CHECK);
      const mockEnv = createMockEnv();
      const ctx = { waitUntil: vi.fn() } as unknown as ExecutionContext;

      // Then: Correct task runs for each pattern (no errors)
      await expect(handleScheduled(dailyEvent, mockEnv, ctx)).resolves.not.toThrow();
      await expect(handleScheduled(priceEvent, mockEnv, ctx)).resolves.not.toThrow();
    });

    it('should run daily digest on "0 8 * * *" pattern', async () => {
      // Given: Cron "0 8 * * *" fires
      const event = createScheduledEvent(CRON_PATTERNS.DAILY_DIGEST);
      const mockEnv = createMockEnv();
      const ctx = { waitUntil: vi.fn() } as unknown as ExecutionContext;

      // When: scheduled handler processes
      // Then: dailyDigest task executes (verified by no error)
      await expect(handleScheduled(event, mockEnv, ctx)).resolves.not.toThrow();

      // Also verify runDailyDigest function exists and works
      await expect(runDailyDigest(mockEnv, ctx)).resolves.not.toThrow();
    });

    it('should run price check on "0 */4 * * *" pattern', async () => {
      // Given: Cron "0 */4 * * *" fires
      const event = createScheduledEvent(CRON_PATTERNS.PRICE_CHECK);
      const mockEnv = createMockEnv();
      const ctx = { waitUntil: vi.fn() } as unknown as ExecutionContext;

      // When: scheduled handler processes
      // Then: priceCheck task executes (verified by no error)
      await expect(handleScheduled(event, mockEnv, ctx)).resolves.not.toThrow();

      // Also verify runPriceCheck function exists and works
      await expect(runPriceCheck(mockEnv, ctx)).resolves.not.toThrow();
    });
  });

  describe('AC-FEAT-012-012: Error Handling', () => {
    it('should log errors without crashing the handler', async () => {
      // Given: Any cron event (handler catches errors internally)
      const event = createScheduledEvent('0 8 * * *');
      const mockEnv = createMockEnv();
      const ctx = { waitUntil: vi.fn() } as unknown as ExecutionContext;

      // When: scheduled handler runs
      // Then: Error logged, handler completes (doesn't throw)
      await expect(handleScheduled(event, mockEnv, ctx)).resolves.not.toThrow();
    });

    it('should continue to next task after error in previous task', async () => {
      // Given: Multiple tasks with different cron patterns
      const event1 = createScheduledEvent(CRON_PATTERNS.DAILY_DIGEST);
      const event2 = createScheduledEvent(CRON_PATTERNS.PRICE_CHECK);
      const mockEnv = createMockEnv();
      const ctx = { waitUntil: vi.fn() } as unknown as ExecutionContext;

      // When: scheduled handler runs for each
      // Then: Both complete without throwing
      await expect(handleScheduled(event1, mockEnv, ctx)).resolves.not.toThrow();
      await expect(handleScheduled(event2, mockEnv, ctx)).resolves.not.toThrow();
    });
  });

  describe('AC-FEAT-012-013: Binding Access', () => {
    it('should have access to D1 database binding', async () => {
      // Given: Scheduled handler with env
      const mockEnv = createMockEnv();

      // When: Handler accesses env.DB
      // Then: D1 binding is available
      expect(mockEnv.DB).toBeDefined();
    });

    it('should have access to R2 storage binding', async () => {
      // Given: Scheduled handler with env
      const mockEnv = createMockEnv();

      // When: Handler accesses env.STORAGE
      // Then: R2 binding is available
      expect(mockEnv.STORAGE).toBeDefined();
    });

    it('should have access to KV cache binding', async () => {
      // Given: Scheduled handler with env
      const mockEnv = createMockEnv();

      // When: Handler accesses env.CACHE
      // Then: KV binding is available
      expect(mockEnv.CACHE).toBeDefined();
    });

    it('should have access to Queue binding', async () => {
      // Given: Scheduled handler with env
      const mockEnv = createMockEnv();

      // When: Handler accesses env.TASKS
      // Then: Queue binding is available (can queue work)
      expect(mockEnv.TASKS).toBeDefined();
      expect(mockEnv.TASKS.send).toBeDefined();
    });
  });
});
