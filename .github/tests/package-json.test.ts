// .github/tests/package-json.test.ts
// Root package.json must carry a non-empty description.

import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { join } from 'path';

const ROOT = join(__dirname, '../..');

describe('root package.json', () => {
  it('should have a non-empty string description', () => {
    // Given: the root package.json (not .github/tests/package.json)
    const pkg = JSON.parse(readFileSync(join(ROOT, 'package.json'), 'utf-8'));

    // When: I read its description field
    const description = pkg.description;

    // Then: it is a string with non-whitespace content
    expect(
      typeof description === 'string' && description.trim().length > 0,
      'root package.json must have a non-empty "description" field'
    ).toBe(true);
  });
});
