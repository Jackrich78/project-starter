// .github/tests/validate-workflow.test.ts
// TDD Tests for FEAT-010: CI/CD Integration - Workflow Validation

import { describe, it, expect } from 'vitest';
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { parse as parseYaml } from 'yaml';

const ROOT = join(__dirname, '../..');
const WORKFLOWS_DIR = join(ROOT, '.github/workflows');

describe('FEAT-010: CI/CD Integration', () => {
  describe('AC-FEAT-010-001: Base Workflow Exists', () => {
    it('should have validate.yml in .github/workflows/', () => {
      // Given: A fresh clone of the repository
      // When: I check .github/workflows/
      // Then: A validate.yml workflow file exists
      const workflowPath = join(WORKFLOWS_DIR, 'validate.yml');

      expect(existsSync(workflowPath)).toBe(true);
    });
  });

  describe('AC-FEAT-010-002: Markdown Linting Runs', () => {
    it('should include markdownlint-cli2 action in validate workflow', () => {
      // Given: A PR with markdown changes
      // When: CI runs
      // Then: markdownlint-cli2 executes and reports issues (non-blocking)

      const workflow = parseYaml(readFileSync(join(WORKFLOWS_DIR, 'validate.yml'), 'utf-8'));
      const steps = workflow.jobs?.validate?.steps || [];
      const markdownlintStep = steps.find((s: any) =>
        s.uses?.includes('markdownlint-cli2-action')
      );
      expect(markdownlintStep).toBeDefined();
      expect(markdownlintStep['continue-on-error']).toBe(true);
    });
  });

  describe('AC-FEAT-010-003: YAML Validation Runs', () => {
    it('should include actionlint in validate workflow', () => {
      // Given: A PR with changes to .yml or .yaml files
      // When: CI runs
      // Then: Invalid YAML fails the build with clear error message

      const workflow = parseYaml(readFileSync(join(WORKFLOWS_DIR, 'validate.yml'), 'utf-8'));
      const steps = workflow.jobs?.validate?.steps || [];
      const actionlintStep = steps.find((s: any) =>
        s.name?.toLowerCase().includes('yaml') ||
        s.name?.toLowerCase().includes('actionlint') ||
        s.run?.includes('actionlint')
      );
      expect(actionlintStep).toBeDefined();
    });
  });

  describe('AC-FEAT-010-004: Hook Syntax Check Runs', () => {
    it('should include Python syntax check in validate workflow', () => {
      // Given: A PR with changes to .claude/hooks/*.py
      // When: CI runs
      // Then: Python syntax errors fail the build

      const workflow = parseYaml(readFileSync(join(WORKFLOWS_DIR, 'validate.yml'), 'utf-8'));
      const steps = workflow.jobs?.validate?.steps || [];
      const pythonStep = steps.find((s: any) =>
        s.run?.includes('py_compile') || s.run?.includes('python')
      );
      expect(pythonStep).toBeDefined();
    });
  });

  describe('AC-FEAT-010-005: Template Structure Validated', () => {
    it('should include template structure validation step', () => {
      // Given: A PR that deletes CLAUDE.md
      // When: CI runs
      // Then: The build fails indicating missing required file

      const workflow = parseYaml(readFileSync(join(WORKFLOWS_DIR, 'validate.yml'), 'utf-8'));
      const steps = workflow.jobs?.validate?.steps || [];
      const structureStep = steps.find((s: any) =>
        s.name?.toLowerCase().includes('template') || s.run?.includes('validate-template')
      );
      expect(structureStep).toBeDefined();
    });

    it('should have validate-structure.sh script', () => {
      // Given: The repository structure
      // When: Checking .github/tests directory
      // Then: validate-structure.sh exists

      expect(existsSync(join(ROOT, '.github/tests/validate-structure.sh'))).toBe(true);
    });
  });

  describe('AC-FEAT-010-006: Stack Tests Path-Filtered', () => {
    it('should have cloudflare stack workflow with path filter', () => {
      // Given: A PR that only changes stacks/cloudflare/
      // When: CI runs
      // Then: Only the cloudflare stack workflow executes

      const workflowPath = join(WORKFLOWS_DIR, 'stack-cloudflare.yml');
      expect(existsSync(workflowPath)).toBe(true);
      const workflow = parseYaml(readFileSync(workflowPath, 'utf-8'));
      const pushPaths = workflow.on?.push?.paths || [];
      const prPaths = workflow.on?.pull_request?.paths || [];
      expect(pushPaths).toContain('stacks/cloudflare/**');
      expect(prPaths).toContain('stacks/cloudflare/**');
    });
  });

  describe('AC-FEAT-010-007: Stack Tests Run on Change', () => {
    it('should run npm test in stack workflow', () => {
      // Given: A PR with changes to stacks/cloudflare/src/
      // When: The cloudflare stack workflow runs
      // Then: npm test executes in stacks/cloudflare/

      const workflow = parseYaml(readFileSync(join(WORKFLOWS_DIR, 'stack-cloudflare.yml'), 'utf-8'));
      const steps = workflow.jobs?.test?.steps || [];
      const testStep = steps.find((s: any) => s.run?.includes('npm test'));
      expect(testStep).toBeDefined();
    });
  });

  describe('AC-FEAT-010-009: Workflow Customization Documented', () => {
    it('should include customization comments in validate.yml', () => {
      // Given: A user reading .github/workflows/validate.yml
      // When: They look for customization guidance
      // Then: Inline comments mark where to add stack-specific steps

      const content = readFileSync(join(WORKFLOWS_DIR, 'validate.yml'), 'utf-8');
      expect(content).toContain('# CUSTOMIZATION:');
    });
  });
});

describe('FEAT-010: Markdownlint Configuration', () => {
  it('should have .markdownlint.json in repository root', () => {
    // Given: The repository structure
    // When: Checking root directory
    // Then: .markdownlint.json exists with valid config

    const configPath = join(ROOT, '.markdownlint.json');
    expect(existsSync(configPath)).toBe(true);
    const config = JSON.parse(readFileSync(configPath, 'utf-8'));
    expect(config.default).toBe(true);
  });
});
