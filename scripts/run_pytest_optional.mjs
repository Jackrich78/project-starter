/**
 * run_pytest_optional.mjs
 *
 * Two test lanes behind the one pre-approved `npm test`:
 *   harness  python3 -m pytest tests/harness                        (tests of the harness itself)
 *   project  uv run --frozen pytest tests/unit tests/integration    (the project's own tests)
 *
 * Each lane degrades to a NOTICE and exit 0 when its runtime is absent (no Python or pytest
 * for the harness lane; no pyproject.toml, .venv or uv for the project lane), so a Node-only
 * cloner never gets a red `npm test`. CI runs both lanes directly and never degrades
 * (.github/workflows/validate.yml).
 *
 * Usage:
 *   npm test                          both lanes (harness first; stops on a harness failure)
 *   npm test -- harness [pytest args] one lane, remaining args passed to pytest
 *   npm test -- project [pytest args]
 * Any other leading argument is ignored, so habits like `npm test -- -q` still work.
 * Direct run: node scripts/run_pytest_optional.mjs [lane] [pytest args]
 */

import { spawnSync } from 'child_process';
import { existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const HARNESS_SUITE = 'tests/harness';
const PROJECT_SUITES = ['tests/unit', 'tests/integration'];
const LANES = new Set(['harness', 'project']);

function exitCode(result) {
  // pytest exit 5 = "no tests collected"; an empty suite is not red.
  return result.status === 5 ? 0 : (result.status ?? 1);
}

function works(cmd, args) {
  const r = spawnSync(cmd, args, { stdio: 'ignore', cwd: ROOT });
  return r.status === 0 && r.error == null;
}

function runHarness(extra) {
  if (!existsSync(resolve(ROOT, HARNESS_SUITE))) {
    console.log(`\nNOTICE: ${HARNESS_SUITE} not found - nothing to run.\n`);
    return 0;
  }
  if (!works('python3', ['-m', 'pytest', '--version'])) {
    console.log(
      '\nNOTICE: pytest not found - skipping harness tests.\n' +
      'To run them: pip install pytest pyyaml  then  npm run test:py\n'
    );
    return 0;
  }
  const r = spawnSync('python3', ['-m', 'pytest', HARNESS_SUITE, '-q', ...extra], { stdio: 'inherit', cwd: ROOT });
  return exitCode(r);
}

function runProject(extra) {
  const ready = existsSync(resolve(ROOT, 'pyproject.toml')) && existsSync(resolve(ROOT, '.venv')) && works('uv', ['--version']);
  if (!ready) {
    console.log('\nNOTICE: project tests skipped - add pyproject.toml and run uv sync once\n');
    return 0;
  }
  const suites = PROJECT_SUITES.filter((s) => existsSync(resolve(ROOT, s)));
  if (suites.length === 0) {
    console.log(`\nNOTICE: no project test folders (${PROJECT_SUITES.join(', ')}) - nothing to run.\n`);
    return 0;
  }
  const r = spawnSync('uv', ['run', '--frozen', 'pytest', ...suites, '-q', ...extra], { stdio: 'inherit', cwd: ROOT });
  return exitCode(r);
}

const argv = process.argv.slice(2);
const lane = LANES.has(argv[0]) ? argv[0] : null;
const extra = lane ? argv.slice(1) : [];

if (lane === 'harness') process.exit(runHarness(extra));
if (lane === 'project') process.exit(runProject(extra));

const harness = runHarness([]);
if (harness !== 0) process.exit(harness);
process.exit(runProject([]));
