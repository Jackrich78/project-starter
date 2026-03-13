/**
 * Slack integration services
 */

const TIMESTAMP_MAX_AGE = 300; // 5 minutes in seconds

/**
 * Validate Slack request signature using HMAC-SHA256
 *
 * @param secret - Slack signing secret
 * @param signature - X-Slack-Signature header value
 * @param timestamp - X-Slack-Request-Timestamp header value
 * @param body - Raw request body
 * @returns true if signature is valid
 */
export async function validateSlackSignature(
  secret: string,
  signature: string,
  timestamp: string,
  body: string
): Promise<boolean> {
  // Check timestamp freshness (replay attack prevention)
  const timestampSeconds = parseInt(timestamp, 10);
  if (isNaN(timestampSeconds)) {
    return false;
  }

  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - timestampSeconds) > TIMESTAMP_MAX_AGE) {
    return false;
  }

  // Compute HMAC-SHA256 signature
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
  const computed =
    'v0=' +
    Array.from(new Uint8Array(sig))
      .map((b) => b.toString(16).padStart(2, '0'))
      .join('');

  // Timing-safe comparison (constant time)
  if (computed.length !== signature.length) {
    return false;
  }

  let result = 0;
  for (let i = 0; i < computed.length; i++) {
    result |= computed.charCodeAt(i) ^ signature.charCodeAt(i);
  }

  return result === 0;
}

/**
 * Slack block message structure
 */
export interface SlackBlock {
  type: string;
  text?: {
    type: string;
    text: string;
  };
}

/**
 * Slack message payload structure
 */
export interface SlackMessage {
  blocks: SlackBlock[];
  response_type?: 'in_channel' | 'ephemeral';
}

/**
 * Format a plain text message as Slack blocks
 *
 * @param text - Plain text message
 * @returns Formatted Slack message with blocks
 */
export function formatSlackBlocks(text: string): SlackMessage {
  return {
    blocks: [
      {
        type: 'section',
        text: {
          type: 'mrkdwn',
          text,
        },
      },
    ],
  };
}

/**
 * Send a response to Slack's response_url
 *
 * @param responseUrl - The response_url from Slack's payload
 * @param message - Message text or formatted SlackMessage
 * @returns Response from Slack
 */
export async function sendSlackResponse(
  responseUrl: string,
  message: string | SlackMessage
): Promise<Response> {
  const payload = typeof message === 'string' ? formatSlackBlocks(message) : message;

  return fetch(responseUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
}

export { TIMESTAMP_MAX_AGE };
