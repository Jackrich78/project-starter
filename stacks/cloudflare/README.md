# Cloudflare Stack

Production-ready Cloudflare Workers template with multi-handler support (HTTP, Queue, Scheduled), D1, R2, KV, and comprehensive test coverage.

## Prerequisites

1. **Cloudflare Account** - [Sign up](https://dash.cloudflare.com/sign-up) (free tier works)
2. **Node.js 18+** - For local development
3. **Wrangler CLI** - Included in devDependencies (no global install needed)

```bash
# Login to Cloudflare (one-time)
npx wrangler login
```

## Free Tier vs Paid Plan

This scaffold works on both free and paid Cloudflare plans:

| Feature | Free Plan | Paid Plan ($5/mo) |
|---------|-----------|-------------------|
| HTTP endpoints | Sync processing | Sync processing |
| Queues | Fallback to sync | Async processing |
| Scheduled/Cron | Works | Works |
| D1 Database | Works | Works |
| R2 Storage | Works | Works |
| KV Store | Works | Works |

**Without queues:** Webhooks process synchronously. The code automatically detects if `env.TASKS` is available and falls back gracefully.

**Testing note:** All 59 tests pass locally regardless of plan. Tests use Cloudflare's vitest-pool-workers which simulates queue behavior in the test environment.

## Fresh Session Checklist

For AI assistants or developers starting fresh:

1. **Copy scaffold** to new project directory
2. **npm install** - Install dependencies
3. **Copy .dev.vars** - `cp .dev.vars.example .dev.vars` (required for local dev)
4. **npx wrangler login** - Authenticate with Cloudflare (one-time)
5. **npm test** - Verify 59 tests pass
6. **npm run dev** - Start local server at localhost:8787
7. **curl localhost:8787/health** - Confirm it's running
8. **Edit wrangler.toml** - Update worker name, add resource IDs
9. **Deploy** - See "Deployment Patterns" below

For Cloudflare-specific questions, invoke the specialist agent (see `.claude/agents/cloudflare-specialist.md`).

## Deployment Patterns

This boilerplate supports two deployment workflows. Choose based on your team size.

### Solo Developer (1 person)

```
Local Dev → Tests Pass → Deploy to Production
```

```bash
npm run dev        # Develop locally
npm test           # Verify tests pass
npm run deploy     # Ship to production
```

**Why this is safe:**
- Cloudflare keeps previous versions (instant rollback)
- Low traffic = low blast radius
- You control the testing discipline

**Rollback if needed:**
```bash
npx wrangler rollback
```

### Team (2+ people)

```
Local Dev → Tests Pass → Staging → Verify → Production
```

```bash
npm run dev              # Develop locally
npm test                 # Verify tests pass
npm run deploy:staging   # Deploy to staging
# ... verify staging works ...
npm run deploy           # Ship to production
```

**When to add staging:** When your team grows to 2+ people deploying code.
See "Adding Staging" section below for setup.

---

## Environments

### Configuration Overview

| Command | Target | Config Used |
|---------|--------|-------------|
| `npm run dev` | Local | Top-level + .dev.vars |
| `npm test` | Test runner | [env.test] |
| `npm run deploy` | Production | Top-level |
| `npm run deploy:staging` | Staging | [env.staging] |

### Local Development

Local dev uses `.dev.vars` for secrets (never committed):

```bash
cp .dev.vars.example .dev.vars
# Edit .dev.vars with your values
npm run dev
```

### Adding Staging

When your team grows to 2+ people:

1. Create staging resources:
   ```bash
   npx wrangler d1 create my-database-staging
   npx wrangler kv namespace create CACHE_STAGING
   ```

2. Uncomment `[env.staging]` in wrangler.toml and add resource IDs

3. Deploy to staging:
   ```bash
   npm run deploy:staging
   ```

### Why No `[env.production]`?

Wrangler has a known bug ([Issue #3392](https://github.com/cloudflare/workers-sdk/issues/3392))
where `wrangler deploy` ignores `[env.production]` and uses top-level config.
We keep production at top-level to avoid this trap.

## Quick Start

### 1. Copy Stack to Your Project

**Full Harness + Stack** (recommended - keeps AI workflow):
```bash
# From project-starter root
mkdir /path/to/your-project
cp -r . /path/to/your-project/
cd /path/to/your-project
cp -r stacks/cloudflare/* .
cp -r stacks/cloudflare/.claude/agents/* .claude/agents/
cp stacks/cloudflare/.gitignore .
cp stacks/cloudflare/.dev.vars.example .
rm -rf stacks/ spikes/
rm -rf node_modules package-lock.json  # Fresh install
```

**Stack Only** (just the worker code):
```bash
mkdir /path/to/your-project && cd /path/to/your-project
cp -r /path/to/project-starter/stacks/cloudflare/* .
cp -r /path/to/project-starter/stacks/cloudflare/.* . 2>/dev/null
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Run Tests

```bash
npm test
```

All 59 tests should pass.

### 4. Start Local Dev Server

```bash
npm run dev
```

Test the health endpoint:
```bash
curl http://localhost:8787/health
# {"status":"ok","timestamp":"2026-01-25T12:00:00.000Z","environment":"production"}
```

### 5. Create Cloudflare Resources (Optional)

Create resources as needed. The stack works without any of these for basic webhook processing:

```bash
# Create D1 database (optional)
npx wrangler d1 create my-database
# Note the database_id from output

# Create KV namespace (optional)
npx wrangler kv namespace create CACHE
# Note the id from output

# Create R2 bucket (optional)
npx wrangler r2 bucket create my-bucket

# Create Queue (requires Workers Paid plan - optional)
npx wrangler queues create tasks
```

### 6. Configure wrangler.toml

Update `wrangler.toml` with your resource IDs:

```toml
name = "my-worker"  # Change to your worker name

# Uncomment and add your IDs:
[[kv_namespaces]]
binding = "CACHE"
id = "your-kv-namespace-id"

[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-d1-database-id"

[[r2_buckets]]
binding = "STORAGE"
bucket_name = "my-bucket"

[vars]
SLACK_SIGNING_SECRET = "your-actual-slack-secret"  # If using Slack
```

### 7. Run D1 Migrations

```bash
# Local (for testing)
npx wrangler d1 execute my-database --local --file=db/migrations/0001_init.sql

# Remote (production)
npx wrangler d1 execute my-database --file=db/migrations/0001_init.sql
```

### 8. Deploy

```bash
npm run deploy
# or
npx wrangler deploy
```

## End-to-End Validation

After deployment, verify your worker is running:

### Health Check
```bash
curl https://my-worker.your-subdomain.workers.dev/health
```

Expected:
```json
{"status":"ok","timestamp":"...","environment":"production"}
```

### Webhook Endpoint
```bash
curl -X POST https://my-worker.your-subdomain.workers.dev/webhook \
  -H "Content-Type: application/json" \
  -d '{"type":"test","data":{"hello":"world"}}'
```

Expected (with queue):
```json
{"status":"queued","messageId":"uuid-here"}
```

Expected (without queue - free tier):
```json
{"status":"processed","messageId":"uuid-here","mode":"sync"}
```

### API Tasks Endpoint
```bash
curl -X POST https://my-worker.your-subdomain.workers.dev/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"type":"process","payload":{"task":"example"}}'
```

Expected (with queue):
```json
{"status":"accepted","messageId":"uuid-here"}
```

Expected (without queue - free tier):
```json
{"status":"processed","messageId":"uuid-here","mode":"sync"}
```

### Test Scheduled Handler
```bash
# Local only - triggers cron manually
npm run dev:scheduled
```

### View Queue Messages
```bash
npx wrangler tail
# Watch real-time logs including queue processing
```

## Architecture

```
cloudflare/
├── src/
│   ├── index.ts              # Multi-handler entry point
│   ├── types.ts              # Env and QueueMessage types
│   ├── handlers/
│   │   ├── webhook.ts        # Hono HTTP routes
│   │   ├── queue-consumer.ts # Queue processor with retry
│   │   └── scheduled.ts      # Cron job handlers
│   ├── services/
│   │   ├── slack.ts          # Slack signature validation
│   │   └── db.ts             # Drizzle D1 wrapper
│   └── lib/
│       └── queue.ts          # Exponential backoff helper
├── db/
│   ├── schema.ts             # Drizzle schema
│   └── migrations/
│       └── 0001_init.sql     # Initial migration
├── test/
│   ├── webhook.test.ts       # HTTP handler tests (12)
│   ├── queue.test.ts         # Queue consumer tests (11)
│   ├── scheduled.test.ts     # Cron handler tests (12)
│   ├── services.test.ts      # Services layer tests (10)
│   └── bindings.test.ts      # D1/R2/KV tests (14)
├── wrangler.toml             # Cloudflare config
├── vitest.config.ts          # Test configuration
├── tsconfig.json             # TypeScript config
└── package.json              # Dependencies and scripts
```

## Handlers

### HTTP (fetch)
Routes via Hono:
- `GET /health` - Health check
- `POST /webhook` - Generic webhook, queues payload
- `POST /slack` - Slack webhook with signature validation
- `POST /api/tasks` - Queue tasks programmatically

### Queue (queue)
**Requires Workers Paid plan.** Without queue, webhooks process synchronously.

When enabled, processes messages with:
- Type-based routing (webhook, slack, api, scheduled)
- Exponential backoff retry (2s, 4s, 8s)
- Max 3 retries before dead-letter
- Error isolation (one failure doesn't stop batch)

To enable queues, uncomment the queue section in `wrangler.toml` and create the queue:
```bash
npx wrangler queues create tasks
```

### Scheduled (scheduled)
Cron patterns:
- `0 8 * * *` - Daily digest at 8 AM
- `0 */4 * * *` - Price check every 4 hours

## Customization

### Add a New HTTP Route

Edit `src/handlers/webhook.ts`:
```typescript
app.post('/my-endpoint', async (c) => {
  const body = await c.req.json();
  // Your logic here
  return c.json({ success: true });
});
```

### Add a New Message Type

Edit `src/handlers/queue-consumer.ts`:
```typescript
case 'my-type':
  await processMyType(message, env);
  break;
```

### Add a New Cron Job

1. Update `wrangler.toml`:
```toml
[triggers]
crons = ["0 8 * * *", "0 */4 * * *", "0 12 * * *"]  # Add new pattern
```

2. Update `src/handlers/scheduled.ts`:
```typescript
case '0 12 * * *':
  await runNoonTask(env, ctx);
  break;
```

### Add Database Tables

1. Create migration in `db/migrations/0002_add_users.sql`
2. Update `db/schema.ts` with Drizzle schema
3. Apply migration:
```bash
npx wrangler d1 execute my-database --file=db/migrations/0002_add_users.sql
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ENVIRONMENT` | development/production | Yes |
| `SLACK_SIGNING_SECRET` | Slack app signing secret | If using Slack |

Set secrets:
```bash
npx wrangler secret put SLACK_SIGNING_SECRET
# Enter your secret when prompted
```

## Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start local dev server |
| `npm run dev:scheduled` | Dev server with cron testing |
| `npm test` | Run all tests |
| `npm run test:watch` | Run tests in watch mode |
| `npm run deploy` | Deploy to production |
| `npm run deploy:staging` | Deploy to staging environment |

## Troubleshooting

### Tests fail with "nodejs_compat" error
Ensure `wrangler.toml` has:
```toml
compatibility_flags = ["nodejs_compat"]
```

### Queue messages not processing
1. Queues require Workers Paid plan ($5/month)
2. Ensure queue is uncommented in `wrangler.toml`:
```toml
[[queues.producers]]
binding = "TASKS"
queue = "tasks"

[[queues.consumers]]
queue = "tasks"
```
3. Create the queue: `npx wrangler queues create tasks`
4. Without queues, webhooks work in sync mode (no queuing)

### D1 queries fail
1. Verify database exists: `npx wrangler d1 list`
2. Run migrations: `npx wrangler d1 execute my-database --file=db/migrations/0001_init.sql`

### Slack signature validation fails
1. Check `SLACK_SIGNING_SECRET` is set correctly
2. Verify timestamp is within 5 minutes
3. Check raw body matches what Slack sent

## Test Coverage

59 tests covering:
- AC-001 to AC-005: HTTP webhook handler
- AC-006 to AC-009: Queue consumer
- AC-010 to AC-013: Scheduled handler
- AC-014 to AC-017: Services layer (Slack, DB, Queue helpers)
- AC-018 to AC-020: Storage bindings (D1, R2, KV)

Run specific test file:
```bash
npm test -- test/webhook.test.ts
```

## Related Documentation

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
- [D1 Database](https://developers.cloudflare.com/d1/)
- [R2 Storage](https://developers.cloudflare.com/r2/)
- [Queues](https://developers.cloudflare.com/queues/)
- [Hono Framework](https://hono.dev/)
- [Drizzle ORM](https://orm.drizzle.team/)
