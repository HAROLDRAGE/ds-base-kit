#!/usr/bin/env node

/**
 * Lint Tokens
 * Validates tokens for syntax, structure, and coverage
 * Wrapper around Python validators with Node.js integration
 */

import fs from 'node:fs';
import { execSync } from 'node:child_process';

class TokenLinter {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.info = [];
  }

  /**
   * Lint token files
   */
  async lint(options = {}) {
    console.log('\n' + '='.repeat(80));
    console.log('🔍 TOKEN LINTER — VALIDATION REPORT');
    console.log('='.repeat(80));

    try {
      // 1. Check JSON syntax
      this.lintJSON();

      // 2. Validate schema
      this.validateSchema();

      // 3. Check coverage
      this.checkCoverage();

      // 4. Print results
      this.printResults();

      // Return exit code
      return this.errors.length > 0 ? 1 : 0;
    } catch (error) {
      console.error(`❌ Linter error: ${error.message}`);
      return 1;
    }
  }

  /**
   * Lint JSON files
   */
  lintJSON() {
    console.log('\n📝 Checking JSON syntax...');

    const tokenFiles = [
      '01-tokens/tokens.dtcg.json',
      '01-tokens/tokens.json',
      '01-tokens/token-metadata.schema.json',
    ];

    let valid = 0;

    for (const file of tokenFiles) {
      if (!fs.existsSync(file)) {
        this.warnings.push(`⚠️  ${file} not found`);
        continue;
      }

      try {
        const content = fs.readFileSync(file, 'utf-8');
        JSON.parse(content);
        valid++;
        this.info.push(`✓ ${file}: Valid JSON`);
      } catch (error) {
        this.errors.push(`❌ ${file}: ${error.message}`);
      }
    }

    console.log(`  ✓ ${valid}/${tokenFiles.length} files have valid JSON`);
  }

  /**
   * Validate schema
   */
  validateSchema() {
    console.log('\n✓ Running schema validation...');

    try {
      const result = execSync(
        'python3 scripts/validate-schema.py 2>&1',
        { encoding: 'utf-8' }
      );

      if (result.includes('FAILED')) {
        this.errors.push('❌ Schema validation failed');
        console.log(result);
      } else {
        this.info.push('✓ Schema validation passed');
        console.log('  ✓ Token schema validation passed');
      }
    } catch (error) {
      this.errors.push(`❌ Schema validation error: ${error.message}`);
    }
  }

  /**
   * Check platform coverage
   */
  checkCoverage() {
    console.log('\n📦 Checking platform coverage...');

    const platforms = [
      { name: 'web', path: 'build/web/css/tokens.css' },
      { name: 'tailwind', path: 'build/tailwind/preset.js' },
      { name: 'ios', path: 'build/ios/Tokens.swift' },
      { name: 'android', path: 'build/android/Tokens.kt' },
      { name: 'storybook', path: 'build/storybook/tokens.js' },
    ];

    let covered = 0;

    for (const platform of platforms) {
      if (fs.existsSync(platform.path)) {
        covered++;
        this.info.push(`✓ ${platform.name}: Covered`);
      } else {
        this.errors.push(`❌ ${platform.name}: No build output at ${platform.path}`);
      }
    }

    console.log(`  ✓ ${covered}/${platforms.length} platforms have output`);
  }

  /**
   * Print results
   */
  printResults() {
    console.log('\n' + '='.repeat(80));
    console.log('📊 SUMMARY');
    console.log('='.repeat(80));

    if (this.errors.length > 0) {
      console.log(`\n❌ Errors: ${this.errors.length}`);
      this.errors.forEach(e => console.log(`  ${e}`));
    }

    if (this.warnings.length > 0) {
      console.log(`\n⚠️  Warnings: ${this.warnings.length}`);
      this.warnings.forEach(w => console.log(`  ${w}`));
    }

    if (this.info.length > 0 && (this.errors.length === 0)) {
      console.log(`\n✓ Info: ${this.info.length}`);
      this.info.slice(0, 5).forEach(i => console.log(`  ${i}`));
      if (this.info.length > 5) {
        console.log(`  ... and ${this.info.length - 5} more`);
      }
    }

    const status = this.errors.length === 0 ? '✅ PASSED' : '❌ FAILED';
    console.log(`\n${status}`);
    console.log('='.repeat(80) + '\n');
  }
}

// Run linter
const linter = new TokenLinter();
linter.lint().then(code => process.exit(code));
