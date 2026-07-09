#!/usr/bin/env node

/**
 * Token Build Script — PHASE 2
 * Multi-platform token generation using Style Dictionary v4+
 * 
 * Generates:
 * - Web: CSS + JavaScript/TypeScript
 * - Tailwind: Preset config
 * - iOS: Swift enums
 * - Android: Kotlin objects
 * - Storybook: Theme + Manager head
 */

import StyleDictionary from 'style-dictionary';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import chalk from 'chalk';
import { exec } from 'child_process';
import { promisify } from 'util';

const execPromise = promisify(exec);
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Parse arguments
const args = process.argv.slice(2);
const isWatch = args.includes('--watch');
const isPlatform = args.find(arg => arg.startsWith('--platform='));
const targetPlatform = isPlatform ? isPlatform.split('=')[1] : null;

// Configuration
const config = {
  watch: isWatch,
  targetPlatform: targetPlatform,
  buildDir: path.resolve(__dirname, '..', 'build'),
  configPath: path.resolve(__dirname, '..', 'style-dictionary.config.js'),
  logFile: path.resolve(__dirname, '..', 'logs', 'build-tokens.log')
};

// Ensure logs directory exists
fs.mkdirSync(path.dirname(config.logFile), { recursive: true });

// Logger
function log(level, message) {
  const timestamp = new Date().toISOString();
  const logEntry = `[${timestamp}] [${level}] ${message}`;
  console.log(logEntry);
  fs.appendFileSync(config.logFile, logEntry + '\n');
}

async function buildTokens() {
  try {
    log('INFO', '🔨 Starting token build process...');
    log('INFO', `Mode: ${config.watch ? 'WATCH' : 'SINGLE BUILD'}`);
    
    if (config.targetPlatform) {
      log('INFO', `Target platform: ${config.targetPlatform}`);
    }

    // Import config
    const configModule = await import(`file://${config.configPath}`);
    const sdConfig = configModule.default;

    // Initialize Style Dictionary
    const sd = new StyleDictionary(sdConfig);
    
    // Select platforms
    let platformsToBuild;
    if (config.targetPlatform) {
      if (!sdConfig.platforms[config.targetPlatform]) {
        throw new Error(`Unknown platform: ${config.targetPlatform}`);
      }
      platformsToBuild = [config.targetPlatform];
    } else {
      platformsToBuild = Object.keys(sdConfig.platforms);
    }

    // Build each platform
    log('INFO', `Building platforms: ${platformsToBuild.join(', ')}`);
    
    const results = {};
    for (const platform of platformsToBuild) {
      try {
        log('INFO', `  → Building ${platform}...`);
        const startTime = Date.now();
        
        sd.buildPlatform(platform);
        
        const buildTime = Date.now() - startTime;
        results[platform] = {
          status: '✅',
          time: `${buildTime}ms`
        };
        
        log('INFO', `  ✅ ${platform} built in ${buildTime}ms`);
      } catch (err) {
        results[platform] = {
          status: '❌',
          error: err.message
        };
        log('ERROR', `  ❌ ${platform} failed: ${err.message}`);
      }
    }

    // Generate summary
    const successCount = Object.values(results).filter(r => r.status === '✅').length;
    const totalCount = Object.keys(results).length;

    log('INFO', `\n${'='}{50}`);
    log('INFO', `Build Summary: ${successCount}/${totalCount} platforms successful`);
    log('INFO', `${'='}{50}\n`);

    // Platform-specific logs
    for (const [platform, result] of Object.entries(results)) {
      if (result.status === '✅') {
        log('INFO', `✅ ${platform}: ${result.time}`);
      } else {
        log('ERROR', `❌ ${platform}: ${result.error}`);
      }
    }

    // Output directory
    log('INFO', `Build output: ${config.buildDir}`);
    
    // Sync to 01-tokens/ for backward compatibility
    log('INFO', 'Syncing build output to 01-tokens/...');
    await syncBuildOutput();

    // Print to console
    console.log('\n' + chalk.green('✅ Token build complete!'));
    console.log(chalk.gray(`Build directory: ${config.buildDir}`));
    
    if (config.watch) {
      console.log(chalk.yellow('📁 Watching for changes...'));
      watchTokens(sdConfig);
    }

  } catch (err) {
    log('ERROR', `Build failed: ${err.message}`);
    console.error(chalk.red(`❌ Build error: ${err.message}`));
    process.exit(1);
  }
}

async function syncBuildOutput() {
  try {
    // Copy Web CSS to 01-tokens/
    const cssSource = path.resolve(config.buildDir, 'web', 'css', 'tokens.css');
    const cssDest = path.resolve(__dirname, '..', '01-tokens', 'tokens.css');
    
    if (fs.existsSync(cssSource)) {
      fs.copyFileSync(cssSource, cssDest);
      log('INFO', `Synced: web/css/tokens.css → 01-tokens/tokens.css`);
    }

    // Copy Web JS to 01-tokens/
    const jsSource = path.resolve(config.buildDir, 'web', 'js', 'tokens.js');
    const jsDest = path.resolve(__dirname, '..', '01-tokens', 'tokens.js');
    
    if (fs.existsSync(jsSource)) {
      fs.copyFileSync(jsSource, jsDest);
      log('INFO', `Synced: web/js/tokens.js → 01-tokens/tokens.js`);
    }

    // Copy Web JSON to 01-tokens/
    const jsonSource = path.resolve(config.buildDir, 'web', 'json', 'tokens.json');
    const jsonDest = path.resolve(__dirname, '..', '01-tokens', 'tokens.json');
    
    if (fs.existsSync(jsonSource)) {
      fs.copyFileSync(jsonSource, jsonDest);
      log('INFO', `Synced: web/json/tokens.json → 01-tokens/tokens.json`);
    }

  } catch (err) {
    log('ERROR', `Sync failed: ${err.message}`);
  }
}

function watchTokens(sdConfig) {
  // Watch source tokens
  fs.watch(path.resolve(__dirname, '..', '01-tokens', 'tokens.dtcg.json'), async () => {
    console.log(chalk.blue('📝 Tokens changed, rebuilding...'));
    await buildTokens();
  });

  // Watch config
  fs.watch(config.configPath, async () => {
    console.log(chalk.blue('⚙️ Config changed, rebuilding...'));
    await buildTokens();
  });
}

// Run build
buildTokens().catch(err => {
  log('ERROR', `Fatal error: ${err.message}`);
  console.error(chalk.red(`Fatal error: ${err.message}`));
  process.exit(1);
});
