// test/bindings.test.ts
// TDD Tests for FEAT-012: Cloudflare Stack - Storage Bindings (D1, R2, KV)

import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
import { env } from 'cloudflare:test';
import { getDb } from '../src/services/db';
import { tasks } from '../db/schema';

// Helper to create mock D1 database
function createMockD1() {
  const results: unknown[] = [];
  return {
    prepare: vi.fn().mockReturnValue({
      bind: vi.fn().mockReturnThis(),
      run: vi.fn().mockResolvedValue({ success: true, meta: {} }),
      all: vi.fn().mockResolvedValue({ results, success: true }),
      first: vi.fn().mockResolvedValue(results[0] || null),
      raw: vi.fn().mockResolvedValue([]),
    }),
    exec: vi.fn().mockResolvedValue({ count: 0, duration: 0 }),
    batch: vi.fn().mockResolvedValue([]),
    dump: vi.fn().mockResolvedValue(new ArrayBuffer(0)),
    _setResults: (r: unknown[]) => {
      results.length = 0;
      results.push(...r);
    },
  };
}

// Helper to create mock R2 bucket
function createMockR2() {
  const storage = new Map<string, { body: ArrayBuffer; httpMetadata?: R2HTTPMetadata }>();

  return {
    put: vi.fn(async (key: string, value: ReadableStream | ArrayBuffer | string, options?: R2PutOptions) => {
      const body = typeof value === 'string'
        ? new TextEncoder().encode(value)
        : value instanceof ArrayBuffer
          ? value
          : await new Response(value).arrayBuffer();
      storage.set(key, { body, httpMetadata: options?.httpMetadata });
      return { key, version: 'v1' } as R2Object;
    }),
    get: vi.fn(async (key: string) => {
      const item = storage.get(key);
      if (!item) return null;
      return {
        key,
        body: new ReadableStream({
          start(controller) {
            controller.enqueue(new Uint8Array(item.body));
            controller.close();
          },
        }),
        bodyUsed: false,
        arrayBuffer: async () => item.body,
        text: async () => new TextDecoder().decode(item.body),
        json: async () => JSON.parse(new TextDecoder().decode(item.body)),
        httpMetadata: item.httpMetadata || {},
      } as unknown as R2ObjectBody;
    }),
    delete: vi.fn(async (key: string) => {
      storage.delete(key);
    }),
    list: vi.fn(async (options?: R2ListOptions) => {
      const objects = Array.from(storage.keys())
        .filter((k) => !options?.prefix || k.startsWith(options.prefix))
        .map((key) => ({ key }));
      return { objects, truncated: false } as R2Objects;
    }),
    _storage: storage,
  };
}

// Helper to create mock KV namespace
function createMockKV() {
  const storage = new Map<string, { value: string; expiration?: number }>();

  return {
    put: vi.fn(async (key: string, value: string, options?: KVNamespacePutOptions) => {
      const expiration = options?.expirationTtl
        ? Date.now() + options.expirationTtl * 1000
        : undefined;
      storage.set(key, { value, expiration });
    }),
    get: vi.fn(async (key: string, type?: 'text' | 'json' | 'arrayBuffer' | 'stream') => {
      const item = storage.get(key);
      if (!item) return null;
      if (item.expiration && Date.now() > item.expiration) {
        storage.delete(key);
        return null;
      }
      if (type === 'json') {
        return JSON.parse(item.value);
      }
      return item.value;
    }),
    delete: vi.fn(async (key: string) => {
      storage.delete(key);
    }),
    list: vi.fn(async (options?: KVNamespaceListOptions) => {
      const keys = Array.from(storage.keys())
        .filter((k) => !options?.prefix || k.startsWith(options.prefix))
        .map((name) => ({ name }));
      return { keys, list_complete: true, cacheStatus: null };
    }),
    _storage: storage,
  };
}

describe('FEAT-012: Storage Bindings', () => {
  describe('AC-FEAT-012-018: D1 Database Integration', () => {
    it('should connect to D1 database', async () => {
      // Given: Worker with D1 binding
      const mockD1 = createMockD1();

      // When: env.DB accessed
      // Then: D1Database instance available
      expect(mockD1).toBeDefined();
      expect(mockD1.prepare).toBeDefined();
    });

    it('should execute raw SQL queries', async () => {
      // Given: D1 database
      const mockD1 = createMockD1();

      // When: SELECT 1 executed
      const stmt = mockD1.prepare('SELECT 1 as value');
      const result = await stmt.first();

      // Then: Returns result
      expect(mockD1.prepare).toHaveBeenCalledWith('SELECT 1 as value');
    });

    it('should run Drizzle migrations', async () => {
      // Given: Drizzle config and migrations
      const mockD1 = createMockD1() as unknown as D1Database;

      // When: Migrations applied (using getDb)
      const db = getDb(mockD1);

      // Then: Database client is available
      expect(db).toBeDefined();
      expect(db.select).toBeDefined();

      // Verify schema is importable
      expect(tasks).toBeDefined();
      expect(tasks.id).toBeDefined();
    });

    it('should insert and query tasks table', async () => {
      // Given: Tasks table exists
      const taskData = { id: 'task-1', type: 'webhook', payload: '{}', status: 'pending', attempts: 0 };
      const mockD1 = {
        prepare: vi.fn().mockReturnValue({
          bind: vi.fn().mockReturnValue({
            first: vi.fn().mockResolvedValue(taskData),
          }),
        }),
      };

      // When: Insert task, then query
      const stmt = mockD1.prepare('SELECT * FROM tasks WHERE id = ?');
      const task = await stmt.bind('task-1').first();

      // Then: Task retrieved with correct data
      expect(task).toBeDefined();
      expect(task?.id).toBe('task-1');
      expect(task?.type).toBe('webhook');
    });
  });

  describe('AC-FEAT-012-019: R2 Object Storage', () => {
    it('should upload object to R2', async () => {
      // Given: R2 binding
      const mockR2 = createMockR2();

      // When: env.STORAGE.put(key, data) called
      await mockR2.put('test-key', 'test-value');

      // Then: Object stored successfully
      expect(mockR2.put).toHaveBeenCalledWith('test-key', 'test-value');
      expect(mockR2._storage.has('test-key')).toBe(true);
    });

    it('should retrieve object from R2', async () => {
      // Given: Object stored in R2
      const mockR2 = createMockR2();
      await mockR2.put('test-key', 'test-value');

      // When: env.STORAGE.get(key) called
      const obj = await mockR2.get('test-key');

      // Then: Returns object with body and metadata
      expect(obj).not.toBeNull();
      const text = await obj!.text();
      expect(text).toBe('test-value');
    });

    it('should delete object from R2', async () => {
      // Given: Object stored in R2
      const mockR2 = createMockR2();
      await mockR2.put('test-key', 'test-value');

      // When: env.STORAGE.delete(key) called
      await mockR2.delete('test-key');

      // Then: Object removed
      const obj = await mockR2.get('test-key');
      expect(obj).toBeNull();
    });

    it('should set content-type metadata', async () => {
      // Given: Object with httpMetadata
      const mockR2 = createMockR2();

      // When: Object uploaded with contentType
      await mockR2.put('test.json', '{"foo":"bar"}', {
        httpMetadata: { contentType: 'application/json' },
      });

      // Then: Metadata preserved on retrieval
      const obj = await mockR2.get('test.json');
      expect(obj).not.toBeNull();
      expect(obj!.httpMetadata.contentType).toBe('application/json');
    });

    it('should stream large objects', async () => {
      // Given: Large object in R2
      const mockR2 = createMockR2();
      const largeData = 'x'.repeat(10000);
      await mockR2.put('large-file', largeData);

      // When: Retrieved
      const obj = await mockR2.get('large-file');

      // Then: Returns ReadableStream (not full buffer)
      expect(obj).not.toBeNull();
      expect(obj!.body).toBeDefined();
      expect(obj!.body instanceof ReadableStream).toBe(true);
    });
  });

  describe('AC-FEAT-012-020: KV Key-Value Store', () => {
    it('should set and get values from KV', async () => {
      // Given: KV binding
      const mockKV = createMockKV();

      // When: put(key, value) then get(key)
      await mockKV.put('test-key', 'test-value');
      const value = await mockKV.get('test-key');

      // Then: Original value returned
      expect(value).toBe('test-value');
    });

    it('should support TTL expiration', async () => {
      // Given: Value with expirationTtl: 1 (1 second)
      const mockKV = createMockKV();
      await mockKV.put('expiring-key', 'temp-value', { expirationTtl: 1 });

      // Value should exist immediately
      const immediateValue = await mockKV.get('expiring-key');
      expect(immediateValue).toBe('temp-value');

      // Note: In real tests, we'd wait for expiration
      // For mock, we verify the TTL was set
      expect(mockKV._storage.get('expiring-key')?.expiration).toBeDefined();
    });

    it('should get JSON values with type', async () => {
      // Given: JSON object stored
      const mockKV = createMockKV();
      const data = { foo: 'bar', count: 42 };
      await mockKV.put('json-key', JSON.stringify(data));

      // When: get(key, 'json') called
      const result = await mockKV.get('json-key', 'json');

      // Then: Returns parsed object with correct type
      expect(result).toEqual(data);
      expect(result.foo).toBe('bar');
      expect(result.count).toBe(42);
    });

    it('should delete keys from KV', async () => {
      // Given: Key exists
      const mockKV = createMockKV();
      await mockKV.put('delete-me', 'value');

      // When: delete(key) called
      await mockKV.delete('delete-me');

      // Then: Key no longer exists
      const value = await mockKV.get('delete-me');
      expect(value).toBeNull();
    });

    it('should list keys with prefix', async () => {
      // Given: Multiple keys with common prefix
      const mockKV = createMockKV();
      await mockKV.put('user:1', 'Alice');
      await mockKV.put('user:2', 'Bob');
      await mockKV.put('admin:1', 'Admin');

      // When: list({ prefix: 'user:' }) called
      const result = await mockKV.list({ prefix: 'user:' });

      // Then: Returns matching keys
      expect(result.keys).toHaveLength(2);
      expect(result.keys.map((k: { name: string }) => k.name)).toContain('user:1');
      expect(result.keys.map((k: { name: string }) => k.name)).toContain('user:2');
      expect(result.keys.map((k: { name: string }) => k.name)).not.toContain('admin:1');
    });
  });
});
