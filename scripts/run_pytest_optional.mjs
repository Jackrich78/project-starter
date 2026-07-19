/**
 * run_pytest_optional.mjs
 *
 * Runs "pytest test/unit/FEAT-035/ -v" if pytest is available.
 * Degrades gracefully (exit 0 + notice) when pytest or Python is absent,
 * so a Node-only cloner never gets a red npm test for a missing optional runtime.
 *
 * Used by: npm test (root package.json)
 * Direct run: node scripts/run_pytest_optional.mjs
 */

import { spawnSync } from 'child_process';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

function hasPytest() {
  const result = spawnSync('python3', ['-m', 'pytest', '--version'], {
    stdio: 'ignore',
    cwd: ROOT,
  });
  return result.status === 0 && result.error == null;
}

if (!hasPytest()) {
  console.log(
    '\nNOTICE: pytest not found — skipping Python tests.\n' +
    'To run them: pip install pytest  then  npm run test:py\n'
  );
  process.exit(0);
}

const result = spawnSync(
  'python3',
  ['-m', 'pytest', 'test/unit/FEAT-035/', '-v'],
  { stdio: 'inherit', cwd: ROOT }
);

process.exit(result.status ?? 1);
