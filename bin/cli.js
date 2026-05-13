#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');

const EDITORS = {
  cursor:   '.cursor/rules/context-optimizer.mdc',
  windsurf: '.windsurf/rules/context-optimizer.md',
  cline:    '.clinerules/context-optimizer.md',
  claude:   'CLAUDE.md',
};

const EDITOR_NAMES = {
  cursor:   'Cursor',
  windsurf: 'Windsurf',
  cline:    'Cline',
  claude:   'Claude Code',
};

function detect(dir) {
  if (fs.existsSync(path.join(dir, '.cursor')))     return 'cursor';
  if (fs.existsSync(path.join(dir, '.windsurf')))   return 'windsurf';
  if (fs.existsSync(path.join(dir, '.clinerules'))) return 'cline';
  return 'claude';
}

const projectPath = process.argv[2] || '.';
const resolvedPath = path.resolve(projectPath);

if (!fs.existsSync(resolvedPath)) {
  console.error('Error: path not found:', resolvedPath);
  process.exit(1);
}

const editor   = detect(resolvedPath);
const dest     = path.join(resolvedPath, EDITORS[editor]);
const skillSrc = path.join(__dirname, '..', 'skill', 'claude-custom-instructions.md');

if (!fs.existsSync(skillSrc)) {
  console.error('Error: skill file not found at', skillSrc);
  process.exit(1);
}

const skill = fs.readFileSync(skillSrc, 'utf8');
fs.mkdirSync(path.dirname(dest), { recursive: true });

if (editor === 'claude' && fs.existsSync(dest)) {
  const existing = fs.readFileSync(dest, 'utf8');
  if (existing.includes('CONTEXT_MANIFEST.md')) {
    console.log('\n  Already installed in', path.relative(resolvedPath, dest));
  } else {
    fs.appendFileSync(dest, '\n\n' + skill);
    console.log('\n  Appended to', path.relative(resolvedPath, dest));
  }
} else {
  fs.writeFileSync(dest, skill);
  console.log('\n  Written to', path.relative(resolvedPath, dest));
}

console.log('  Editor:   ', EDITOR_NAMES[editor]);
console.log('  Project:  ', resolvedPath);
console.log('\nNext — generate your manifest:\n');
console.log('  python3 tools/context_mapper.py', resolvedPath);
console.log('\nThen upload CONTEXT_MANIFEST.md to your Claude Project or paste into chat.\n');
