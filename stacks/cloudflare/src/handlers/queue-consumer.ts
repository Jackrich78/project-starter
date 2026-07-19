/**
 * Queue Consumer Handler
 */
import type { Env, QueueMessage } from '../types';
import { backoff } from '../lib/queue';

const MAX_RETRIES = 3;

/**
 * Process a batch of queue messages
 */
export async function handleQueueBatch(
  batch: MessageBatch<QueueMessage>,
  env: Env,
  ctx: ExecutionContext
): Promise<void> {
  console.log(`[queue] Received batch of ${batch.messages.length} messages`);

  for (const message of batch.messages) {
    try {
      await processMessage(message.body, env);
      message.ack();
      console.log(`[queue] Successfully processed message ${message.body.id}`);
    } catch (error) {
      console.error(`[queue] Error processing message ${message.body.id}:`, error);

      if (message.attempts < MAX_RETRIES) {
        const delaySeconds = backoff(message.attempts);
        console.log(`[queue] Retrying message ${message.body.id} in ${delaySeconds}s`);
        message.retry({ delaySeconds });
      } else {
        // Max retries exceeded - ack to prevent infinite retry
        console.error(
          `[queue] Max retries exceeded for message ${message.body.id}. Payload:`,
          JSON.stringify(message.body)
        );
        message.ack();
      }
    }
  }
}

/**
 * Process a single message based on type
 */
async function processMessage(message: QueueMessage, env: Env): Promise<void> {
  console.log(`[queue] Processing message ${message.id} (type: ${message.type})`);

  switch (message.type) {
    case 'webhook':
      await processWebhookMessage(message, env);
      break;
    case 'slack':
      await processSlackMessage(message, env);
      break;
    case 'api':
      await processApiMessage(message, env);
      break;
    case 'scheduled':
      await processScheduledMessage(message, env);
      break;
    default:
      console.log(`[queue] Unknown message type: ${message.type}`);
      // Still process - allows for extensibility
      await processGenericMessage(message, env);
  }
}

async function processWebhookMessage(message: QueueMessage, env: Env): Promise<void> {
  console.log(`[queue] Processing webhook message`);
  // Add webhook-specific processing logic here
}

async function processSlackMessage(message: QueueMessage, env: Env): Promise<void> {
  console.log(`[queue] Processing Slack message`);
  // Add Slack-specific processing logic here
}

async function processApiMessage(message: QueueMessage, env: Env): Promise<void> {
  console.log(`[queue] Processing API message`);
  // Add API-specific processing logic here
}

async function processScheduledMessage(message: QueueMessage, env: Env): Promise<void> {
  console.log(`[queue] Processing scheduled message`);
  // Add scheduled-specific processing logic here
}

async function processGenericMessage(message: QueueMessage, env: Env): Promise<void> {
  console.log(`[queue] Processing generic message`);
  // Generic processing for unknown types
}

export { MAX_RETRIES };
