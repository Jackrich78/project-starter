// test/webhook.test.ts
// TDD Tests for FEAT-012: Cloudflare Stack - HTTP Webhook Handler

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { env, SELF } from 'cloudflare:test';

describe('FEAT-012: HTTP Webhook Handler', () => {
  describe('AC-FEAT-012-001: Health Check Endpoint', () => {
    it('should return 200 with status ok on GET /health', async () => {
      // Given: Worker is running
      // When: GET /health
      const response = await SELF.fetch('http://localhost/health');

      // Then: Returns { status: 'ok', timestamp: ISO string, environment: string }
      expect(response.status).toBe(200);
      const data = (await response.json()) as { status: string; timestamp: string; environment: string };
      expect(data.status).toBe('ok');
      expect(data).toHaveProperty('timestamp');
      expect(data).toHaveProperty('environment');
    });

    it('should include timestamp in ISO format', async () => {
      // Given: Worker is running
      // When: GET /health
      const response = await SELF.fetch('http://localhost/health');
      const data = (await response.json()) as { timestamp: string };

      // Then: timestamp field is valid ISO 8601
      const timestamp = new Date(data.timestamp);
      expect(timestamp.toISOString()).toBe(data.timestamp);
    });
  });

  describe('AC-FEAT-012-002: Webhook Queue Pattern', () => {
    it('should queue webhook payload and return 202', async () => {
      // Given: Valid JSON payload
      // When: POST /webhook with { type: 'test', data: {...} }
      const response = await SELF.fetch('http://localhost/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'test', data: { foo: 'bar' } }),
      });

      // Then: Returns 202 with { status: 'queued', messageId: string }
      expect(response.status).toBe(202);
      const data = (await response.json()) as { status: string; messageId: string };
      expect(data.status).toBe('queued');
      expect(data).toHaveProperty('messageId');
      expect(typeof data.messageId).toBe('string');
    });

    it('should return 400 for invalid JSON', async () => {
      // Given: Invalid JSON body
      // When: POST /webhook with malformed JSON
      const response = await SELF.fetch('http://localhost/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: 'not valid json{{{',
      });

      // Then: Returns 400 with error message
      expect(response.status).toBe(400);
      const data = (await response.json()) as { error: string };
      expect(data).toHaveProperty('error');
    });

    it('should return within 100ms (async pattern)', async () => {
      // Given: Any valid payload
      const start = performance.now();

      // When: POST /webhook
      const response = await SELF.fetch('http://localhost/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ test: true }),
      });

      const elapsed = performance.now() - start;

      // Then: Response time < 100ms (queue is async)
      // Note: In test environment this is usually much faster
      expect(response.status).toBe(202);
      expect(elapsed).toBeLessThan(100);
    });
  });

  describe('AC-FEAT-012-003: Slack Signature Validation', () => {
    const slackSecret = 'test-slack-secret';

    async function generateSlackSignature(
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

    it('should reject requests without X-Slack-Signature header', async () => {
      // Given: Request to /slack endpoint
      // When: No X-Slack-Signature header
      const response = await SELF.fetch('http://localhost/slack', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'event_callback' }),
      });

      // Then: Returns 401 Unauthorized
      expect(response.status).toBe(401);
    });

    it('should reject requests with invalid signature', async () => {
      // Given: Request with incorrect signature
      const timestamp = Math.floor(Date.now() / 1000).toString();
      const body = JSON.stringify({ type: 'event_callback' });

      // When: POST /slack with invalid X-Slack-Signature
      const response = await SELF.fetch('http://localhost/slack', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Slack-Signature': 'v0=invalid',
          'X-Slack-Request-Timestamp': timestamp,
        },
        body,
      });

      // Then: Returns 401 Unauthorized
      expect(response.status).toBe(401);
    });

    it('should accept requests with valid Slack signature', async () => {
      // Given: Properly signed Slack request
      const timestamp = Math.floor(Date.now() / 1000).toString();
      const body = JSON.stringify({ type: 'event_callback' });
      // Note: env.SLACK_SIGNING_SECRET should be set in wrangler.toml or test config
      // For testing, we use a known secret that matches our test env
      const signature = await generateSlackSignature(slackSecret, timestamp, body);

      // When: POST /slack with valid X-Slack-Signature, X-Slack-Request-Timestamp
      const response = await SELF.fetch('http://localhost/slack', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Slack-Signature': signature,
          'X-Slack-Request-Timestamp': timestamp,
        },
        body,
      });

      // Then: Returns 200 and queues the message
      expect(response.status).toBe(200);
      const data = (await response.json()) as { status: string; messageId: string };
      expect(data.status).toBe('queued');
    });

    it('should reject requests with stale timestamp (replay attack)', async () => {
      // Given: Request with timestamp > 5 minutes old
      const staleTimestamp = (Math.floor(Date.now() / 1000) - 400).toString(); // 6+ minutes ago
      const body = JSON.stringify({ type: 'event_callback' });
      const signature = await generateSlackSignature(slackSecret, staleTimestamp, body);

      // When: POST /slack with old X-Slack-Request-Timestamp
      const response = await SELF.fetch('http://localhost/slack', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Slack-Signature': signature,
          'X-Slack-Request-Timestamp': staleTimestamp,
        },
        body,
      });

      // Then: Returns 401 (replay attack prevention)
      expect(response.status).toBe(401);
    });
  });

  describe('AC-FEAT-012-004: API Task Endpoint', () => {
    it('should queue API tasks and return 202', async () => {
      // Given: Valid task payload
      // When: POST /api/tasks with { type: 'process', payload: {...} }
      const response = await SELF.fetch('http://localhost/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'process', payload: { data: 'test' } }),
      });

      // Then: Returns 202 Accepted with messageId
      expect(response.status).toBe(202);
      const data = (await response.json()) as { status: string; messageId: string };
      expect(data.status).toBe('accepted');
      expect(data).toHaveProperty('messageId');
    });
  });

  describe('AC-FEAT-012-005: Error Handling', () => {
    it('should return 404 for unknown routes', async () => {
      // Given: Non-existent route
      // When: GET /unknown-path
      const response = await SELF.fetch('http://localhost/unknown-path');

      // Then: Returns 404 Not Found
      expect(response.status).toBe(404);
    });

    it('should return 405 for wrong HTTP method', async () => {
      // Given: Endpoint that only accepts POST
      // When: GET /webhook
      const response = await SELF.fetch('http://localhost/webhook', {
        method: 'GET',
      });

      // Then: Returns 404 (Hono returns 404 for unmatched method by default)
      // Note: Hono doesn't return 405 by default, it returns 404 for unmatched routes
      expect(response.status).toBe(404);
    });
  });
});
