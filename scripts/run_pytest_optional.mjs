/**
 * run_pytest_optional.mjs
 *
 * Runs the harness test-suite (`pytest tests/harness`) when pytest is available.
 * Degrades gracefully (exit 0 + notice) when Python or pytest is absent, so a
 * Node-only cloner never gets a red `npm test` for a missing optional runtime.
 * CI always installs pytest, so the gates still run there.
 *
 * Used by: npm test (root package.json). Direct run: node scripts/run_pytest_optional.mjs
 */

import { spawnSync } from 'child_process';
import { existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SUITE = 'tests/harness';

function hasPytest() {
  const r = spawnSync('python3', ['-m', 'pytest', '--version'], { stdio: 'ignore', cwd: ROOT });
  return r.status === 0 && r.error == null;
}

if (!existsSync(resolve(ROOT, SUITE))) {
  console.log(`\nNOTICE: ${SUITE} not found - nothing to run.\n`);
  process.exit(0);
}

if (!hasPytest()) {
  console.log(
    '\nNOTICE: pytest not found - skipping harness tests.\n' +
    'To run them: pip install pytest pyyaml  then  npm run test:py\n'
  );
  process.exit(0);
}

const result = spawnSync('python3', ['-m', 'pytest', SUITE, '-q'], { stdio: 'inherit', cwd: ROOT });

// pytest exit 5 = "no tests collected"; treat as success so an empty suite is not red.
process.exit(result.status === 5 ? 0 : (result.status ?? 1));
