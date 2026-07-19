// test/services.test.ts
// TDD Tests for FEAT-012: Cloudflare Stack - Services Layer

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { env } from 'cloudflare:test';
import {
  validateSlackSignature,
  sendSlackResponse,
  formatSlackBlocks,
  TIMESTAMP_MAX_AGE,
} from '../src/services/slack';
import { backoff, MAX_BACKOFF } from '../src/lib/queue';
import { getDb } from '../src/services/db';

describe('FEAT-012: Services Layer', () => {
  describe('AC-FEAT-012-014: Slack Signature Validation Service', () => {
    const secret = 'test-signing-secret';

    async function generateSignature(
      secret: string,
      timestamp: string,
      body: string
    ): Promise<string> {
      const sigBasestring = `v0:${timestamp}:${body}`;
      const encoder = new TextEncoder();
      const key = await crypto.subtle.importKey(
        'raw',
        encoder.encode(secret),
        { name: 'HMAC', hash: 'SHA-256' },
        false,
        ['sign']
      );
      const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(sigBasestring));
      return (
        'v0=' +
        Array.from(new Uint8Array(sig))
          .map((b) => b.toString(16).padStart(2, '0'))
          .join('')
      );
    }

    it('should validate correct Slack signature', async () => {
      // Given: Request with correct signature, timestamp, and secret
      const timestamp = Math.floor(Date.now() / 1000).toString();
      const body = JSON.stringify({ test: 'payload' });
      const signature = await generateSignature(secret, timestamp, body);

      // When: validateSlackSignature() called
      const result = await validateSlackSignature(secret, signature, timestamp, body);

      // Then: Returns true
      expect(result).toBe(true);
    });

    it('should reject incorrect signature', async () => {
      // Given: Request with wrong signature
      const timestamp = Math.floor(Date.now() / 1000).toString();
      const body = JSON.stringify({ test: 'payload' });
      const wrongSignature = 'v0=invalid-signature-here';

      // When: validateSlackSignature() called
      const result = await validateSlackSignature(secret, wrongSignature, timestamp, body);

      // Then: Returns false
      expect(result).toBe(false);
    });

    it('should reject stale timestamp (> 5 minutes)', async () => {
      // Given: Request with timestamp older than 5 minutes
      const staleTimestamp = (Math.floor(Date.now() / 1000) - 400).toString(); // 6+ minutes old
      const body = JSON.stringify({ test: 'payload' });
      const signature = await generateSignature(secret, staleTimestamp, body);

      // When: validateSlackSignature() called
      const result = await validateSlackSignature(secret, signature, staleTimestamp, body);

      // Then: Returns false (replay attack prevention)
      expect(result).toBe(false);
    });

    it('should use HMAC-SHA256 for signature computation', async () => {
      // Given: Known inputs (secret, timestamp, body)
      const knownSecret = 'known-secret';
      const knownTimestamp = '1234567890';
      const knownBody = 'test-body';

      // When: Signature computed
      const signature = await generateSignature(knownSecret, knownTimestamp, knownBody);

      // Then: Signature starts with 'v0=' (Slack format)
      expect(signature).toMatch(/^v0=[a-f0-9]{64}$/);

      // And validates correctly
      const result = await validateSlackSignature(
        knownSecret,
        signature,
        knownTimestamp,
        knownBody
      );
      // Note: This will fail timestamp check, but we're testing the signature format
      // We need fresh timestamp for actual validation
      const freshTimestamp = Math.floor(Date.now() / 1000).toString();
      const freshSignature = await generateSignature(knownSecret, freshTimestamp, knownBody);
      const freshResult = await validateSlackSignature(
        knownSecret,
        freshSignature,
        freshTimestamp,
        knownBody
      );
      expect(freshResult).toBe(true);
    });
  });

  describe('AC-FEAT-012-015: Slack Response Service', () => {
    it('should send response to response_url', async () => {
      // Given: Valid response_url and message
      const responseUrl = 'https://hooks.slack.com/actions/test';
      const message = 'Hello from worker!';

      // Mock fetch for this test
      const originalFetch = globalThis.fetch;
      let capturedRequest: { url: string; method: string; body: string } | null = null;

      globalThis.fetch = vi.fn(async (url: string, init?: RequestInit) => {
        capturedRequest = {
          url: url.toString(),
          method: init?.method || 'GET',
          body: init?.body?.toString() || '',
        };
        return new Response(JSON.stringify({ ok: true }), { status: 200 });
      }) as unknown as typeof fetch;

      try {
        // When: sendSlackResponse() called
        const response = await sendSlackResponse(responseUrl, message);

        // Then: POST to response_url with message payload
        expect(capturedRequest).not.toBeNull();
        expect(capturedRequest!.url).toBe(responseUrl);
        expect(capturedRequest!.method).toBe('POST');
        expect(response.status).toBe(200);
      } finally {
        globalThis.fetch = originalFetch;
      }
    });

    it('should format message as Slack blocks', async () => {
      // Given: Plain text message
      const text = 'Hello, world!';

      // When: formatSlackBlocks() called
      const result = formatSlackBlocks(text);

      // Then: Message formatted as Slack blocks structure
      expect(result).toHaveProperty('blocks');
      expect(Array.isArray(result.blocks)).toBe(true);
      expect(result.blocks.length).toBeGreaterThan(0);
      expect(result.blocks[0]).toHaveProperty('type', 'section');
      expect(result.blocks[0].text).toHaveProperty('type', 'mrkdwn');
      expect(result.blocks[0].text).toHaveProperty('text', text);
    });
  });

  describe('AC-FEAT-012-016: Database Service (Drizzle)', () => {
    it('should create Drizzle client from D1 binding', async () => {
      // Given: D1 database binding (from env)
      // Note: In vitest-pool-workers, env.DB is available if configured
      // For unit testing, we create a mock D1 binding
      const mockD1 = {
        prepare: vi.fn().mockReturnThis(),
        bind: vi.fn().mockReturnThis(),
        run: vi.fn().mockResolvedValue({ success: true }),
        all: vi.fn().mockResolvedValue({ results: [] }),
        first: vi.fn().mockResolvedValue(null),
        raw: vi.fn().mockResolvedValue([]),
        exec: vi.fn().mockResolvedValue({ count: 0 }),
        batch: vi.fn().mockResolvedValue([]),
        dump: vi.fn().mockResolvedValue(new ArrayBuffer(0)),
      } as unknown as D1Database;

      // When: getDb(env) called
      const db = getDb(mockD1);

      // Then: Returns DrizzleD1Database instance
      expect(db).toBeDefined();
      expect(typeof db.select).toBe('function');
      expect(typeof db.insert).toBe('function');
      expect(typeof db.update).toBe('function');
      expect(typeof db.delete).toBe('function');
    });

    it('should provide type-safe queries', async () => {
      // Given: Drizzle client
      const mockD1 = {
        prepare: vi.fn().mockReturnThis(),
        bind: vi.fn().mockReturnThis(),
        run: vi.fn().mockResolvedValue({ success: true }),
        all: vi.fn().mockResolvedValue({ results: [] }),
        first: vi.fn().mockResolvedValue(null),
        raw: vi.fn().mockResolvedValue([]),
        exec: vi.fn().mockResolvedValue({ count: 0 }),
        batch: vi.fn().mockResolvedValue([]),
        dump: vi.fn().mockResolvedValue(new ArrayBuffer(0)),
      } as unknown as D1Database;

      const db = getDb(mockD1);

      // When: Query builder accessed
      // Then: TypeScript types are available (this is a compile-time check)
      expect(db.select).toBeDefined();

      // Verify the client has expected Drizzle methods
      expect(typeof db.$with).toBe('function');
    });
  });

  describe('AC-FEAT-012-017: Queue Helpers', () => {
    it('should compute exponential backoff correctly', async () => {
      // Given: attempts = 1, 2, 3
      // When: backoff(attempts) called
      // Then: Returns 2, 4, 8 respectively
      expect(backoff(1)).toBe(2);
      expect(backoff(2)).toBe(4);
      expect(backoff(3)).toBe(8);
    });

    it('should cap backoff at maximum value', async () => {
      // Given: Very high attempt count
      // When: backoff(attempts) called
      // Then: Returns capped max value (not overflow)
      expect(backoff(10)).toBe(MAX_BACKOFF); // 2^10 = 1024, should be capped at 64
      expect(backoff(100)).toBe(MAX_BACKOFF);
    });
  });
});
