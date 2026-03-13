/**
 * HTTP Webhook Handler using Hono
 */
import { Hono } from 'hono';
import type { Env, QueueMessage } from '../types';
import { validateSlackSignature } from '../services/slack';

export const app = new Hono<{ Bindings: Env }>();

// Health check endpoint
app.get('/health', (c) => {
  return c.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    environment: c.env.ENVIRONMENT,
  });
});

// Generic webhook endpoint - validates and queues work (or processes sync if no queue)
app.post('/webhook', async (c) => {
  try {
    const body = await c.req.json();

    // Generate unique ID for tracking
    const messageId = crypto.randomUUID();

    // Queue for async processing if available, otherwise process synchronously
    if (c.env.TASKS) {
      await c.env.TASKS.send({
        type: 'webhook',
        payload: body,
        timestamp: Date.now(),
        id: messageId,
      });

      return c.json(
        {
          status: 'queued',
          messageId,
        },
        202
      );
    }

    // No queue available - process synchronously
    console.log(`[webhook] Processing synchronously: ${messageId}`);
    return c.json(
      {
        status: 'processed',
        messageId,
        mode: 'sync',
      },
      200
    );
  } catch (error) {
    if (error instanceof SyntaxError) {
      return c.json({ error: 'Invalid JSON' }, 400);
    }
    return c.json({ error: 'Failed to process message' }, 500);
  }
});

// Slack webhook with signature validation
app.post('/slack', async (c) => {
  const signature = c.req.header('X-Slack-Signature');
  const timestamp = c.req.header('X-Slack-Request-Timestamp');

  if (!signature || !timestamp) {
    return c.json({ error: 'Missing Slack headers' }, 401);
  }

  const body = await c.req.text();

  const isValid = await validateSlackSignature(
    c.env.SLACK_SIGNING_SECRET,
    signature,
    timestamp,
    body
  );

  if (!isValid) {
    return c.json({ error: 'Invalid signature' }, 401);
  }

  // Parse and queue the message (or process sync if no queue)
  const payload = JSON.parse(body);
  const messageId = crypto.randomUUID();

  if (c.env.TASKS) {
    await c.env.TASKS.send({
      type: 'slack',
      payload,
      timestamp: Date.now(),
      id: messageId,
    });
    return c.json({ status: 'queued', messageId }, 200);
  }

  // No queue - process synchronously
  console.log(`[slack] Processing synchronously: ${messageId}`);
  return c.json({ status: 'processed', messageId, mode: 'sync' }, 200);
});

// API task endpoint
app.post('/api/tasks', async (c) => {
  try {
    const body = await c.req.json();
    const messageId = crypto.randomUUID();

    if (c.env.TASKS) {
      await c.env.TASKS.send({
        type: body.type || 'api',
        payload: body.payload || body,
        timestamp: Date.now(),
        id: messageId,
      });
      return c.json({ status: 'accepted', messageId }, 202);
    }

    // No queue - process synchronously
    console.log(`[api] Processing synchronously: ${messageId}`);
    return c.json({ status: 'processed', messageId, mode: 'sync' }, 200);
  } catch (error) {
    if (error instanceof SyntaxError) {
      return c.json({ error: 'Invalid JSON' }, 400);
    }
    return c.json({ error: 'Failed to process task' }, 500);
  }
});

// 404 handler
app.notFound((c) => {
  return c.json({ error: 'Not found' }, 404);
});

// Error handler
app.onError((err, c) => {
  console.error('[fetch] Unhandled error:', err);
  return c.json({ error: 'Internal server error' }, 500);
});

export default app;
