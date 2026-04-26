#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────────────────────
# Context Optimizer — Full-Stack Installer
# Local-first • Idempotent • Zero external dependencies
# ─────────────────────────────────────────────────────────────

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()     { echo -e "${BLUE}[context-optimizer]${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
warn()    { echo -e "${YELLOW}⚠ $1${NC}"; }
error()   { echo -e "${RED}✗ $1${NC}"; exit 1; }

# ── Project Root ─────────────────────────────────────────────
PROJECT_ROOT="${1:-.}"
cd "$PROJECT_ROOT" || error "Failed to enter directory: $PROJECT_ROOT"
PROJECT_ROOT="$(pwd)"
log "Working in: $PROJECT_ROOT"

# ── Directory Structure ──────────────────────────────────────
mkdir -p .claude/completions .claude/sessions docs/learnings docs/archive skill prompt tools

# ── .claudeignore ────────────────────────────────────────────
CLAUDEIGNORE=".claudeignore"
if [[ ! -f "$CLAUDEIGNORE" ]]; then
  cat > "$CLAUDEIGNORE" << 'EOF'
# Session & history bloat (0 tokens until explicitly requested)
.claude/completions/
.claude/sessions/
docs/archive/
docs/learnings/
*.md.backup
*.original.md

# Build/artifacts (double-guarded)
node_modules/
dist/
build/
.venv/
__pycache__/
target/
.next/
.output/
EOF
  success "Created $CLAUDEIGNORE"
else
  warn "$CLAUDEIGNORE already exists. Skipping."
fi

# ── Core .claude/ Files ─────────────────────────────────────
create_if_missing() {
  local file="$1" content="$2"
  if [[ ! -f "$file" ]]; then
    printf "%s\n" "$content" > "$file"
    success "Created $file"
  else
    warn "$file exists. Skipping."
  fi
}

create_if_missing ".claude/COMMON_MISTAKES.md" \
"# Common Mistakes
<!-- Add bugs that took >1hr to debug. Keep it short. -->
- "

create_if_missing ".claude/QUICK_START.md" \
"# Quick Start
<!-- Daily commands: dev, db, test, deploy -->
- "

create_if_missing ".claude/ARCHITECTURE_MAP.md" \
"# Architecture Map
<!-- High-level routing, layers, entry points -->
- "

# ── Skill & Prompt Files ────────────────────────────────────
cat > skill/claude-custom-instructions.md << 'SKILL_EOF'
# Context Optimizer — Core Skill
# Attach to: Claude Desktop/Web/Code → Settings → Custom Instructions
# Requires: CONTEXT_MANIFEST.md in project root or Claude Project Knowledge

## PRIMARY DIRECTIVE
You are a structural, token-minimal code assistant. NEVER dump files or directories. ALWAYS reason from CONTEXT_MANIFEST.md first. Fetch only what is strictly necessary. Compress all output. Preserve 100% technical accuracy.

## CONTEXT RULES (HARD LIMITS)
1. CONTEXT_MANIFEST.md is the ONLY source for dependency/context discovery.
2. MAX 3 files per turn. Snippets (10–30 lines) preferred over full files.
3. NEVER scan directories, list files, or read unrequested paths.
4. If context is missing, ask for ONE specific file/path. Do not guess.
5. Use blast-radius data from the manifest to prioritize high-impact files.

## OUTPUT FORMAT (STRICT)
Every response MUST begin with this exact structure:

**Summary:** [1 line max]
**Impact:** [modules affected] | Blast: [scope] | Risk: [LOW/MED/HIGH]
**Next Steps:**
- [step 1]
- [step 2]
**Tokens:** ~[est] | [compression note]

Rules:
- Use diffs/patches. Show only changed/relevant lines with `// ...` or `# ...`.
- Drop filler, pleasantries, hedging, and step-by-step narration.
- Code, commands, paths, and technical terms: UNTOUCHED.
- If format drifts, self-correct immediately.

## RISK GUARDS
Auto-flag when changes affect:
- Public APIs/interfaces
- Auth, security, or data layers
- Cross-module dependencies

Format: `⚠️ [RISK LEVEL] — [1-line reason] → [test/rollback step]`

## TOKEN BUDGET
- Target ≤1,200 output tokens per response.
- If approaching limit, truncate explanations, output checkpoint, and ask to continue.
- NEVER exceed budget without explicit user override.

## ABSOLUTE PROHIBITIONS
- NO directory listings or recursive reads
- NO unrequested full-file dumps
- NO verbose explanations or filler
- NO bypassing CONTEXT_MANIFEST.md
- NO ignoring format or budget rules

## OVERRIDES & RESET
- Reset skill: "RELOAD CONTEXT OPTIMIZER"
- Adjust limits: "MAX_FILES: X", "BUDGET: X", "COMPRESSION: lite/full"
- Verbose mode: "TEMP VERBOSE" (reverts after 1 turn)
SKILL_EOF
success "Created skill/claude-custom-instructions.md"

cat > prompt/one-click-vertical-prompt.md << 'PROMPT_EOF'
# Context Optimizer — Session Activator
# Paste this at the start of any Claude chat to enforce token-efficient workflow.

Activate Context Optimizer mode. Follow these rules strictly for this entire session:

1. Use CONTEXT_MANIFEST.md as the sole dependency graph. Never scan directories.
2. Fetch max 3 files/turn. Prefer 10–30 line snippets. Ask for exact paths if missing.
3. Respond ONLY in this format:
   **Summary:** [1 line]
   **Impact:** [modules] | Blast: [scope] | Risk: [LOW/MED/HIGH]
   **Next Steps:**
   - [step 1]
   - [step 2]
   **Tokens:** ~[est] | [note]
4. Keep responses ≤1,200 tokens. Compress aggressively. Use diffs. Drop filler.
5. Flag API/auth/cross-module changes with risk level + rollback tip.
6. NO directory dumps, NO unrequested files, NO verbose narration, NO format drift.

Acknowledge with: "✅ Context Optimizer active. Awaiting task + CONTEXT_MANIFEST.md."
PROMPT_EOF
success "Created prompt/one-click-vertical-prompt.md"

# ── Agent Detection & Safe Injection ────────────────────────
SKILL_CONTENT="$(cat skill/claude-custom-instructions.md)"
MARKER_START="<!-- CONTEXT-OPTIMIZER-SKILL-START -->"
MARKER_END="<!-- CONTEXT-OPTIMIZER-SKILL-END -->"

inject_if_detected() {
  local target="$1" agent="$2"
  mkdir -p "$(dirname "$target")"
  if grep -q "$MARKER_START" "$target" 2>/dev/null; then
    warn "$agent rules already contain Context Optimizer. Skipping."
    return
  fi
  {
    echo ""
    echo "$MARKER_START"
    echo "$SKILL_CONTENT"
    echo "$MARKER_END"
  } >> "$target"
  success "Injected into $target ($agent)"
}

log "Detecting AI agents & injecting skill..."
DETECTED=0

[[ -d ".cursor" || -f ".cursorrules" ]] && { inject_if_detected ".cursor/rules/context-optimizer.mdc" "Cursor"; DETECTED=1; }
[[ -d ".windsurf" ]] && { inject_if_detected ".windsurf/rules/context-optimizer.md" "Windsurf"; DETECTED=1; }
[[ -f ".clinerules" || -d ".cline" ]] && { inject_if_detected ".clinerules/context-optimizer.md" "Cline"; DETECTED=1; }
[[ -d ".github" ]] && { inject_if_detected ".github/copilot-instructions.md" "Copilot"; DETECTED=1; }
[[ -f "CLAUDE.md" || -d ".claude" ]] && { inject_if_detected "CLAUDE.md" "Claude Code"; DETECTED=1; }

if [[ $DETECTED -eq 0 ]]; then
  warn "No AI agent directories detected. Skill saved to skill/claude-custom-instructions.md"
  log "Manually attach it in your editor's settings or paste prompt/one-click-vertical-prompt.md per session."
fi

# ── Manifest Generation ─────────────────────────────────────
log "Generating CONTEXT_MANIFEST.md..."
if command -v python3 &> /dev/null && [[ -f "tools/context_mapper.py" ]]; then
  python3 tools/context_mapper.py "$PROJECT_ROOT" || warn "Manifest generation failed. Run manually: python3 tools/context_mapper.py ."
else
  warn "Python3 or tools/context_mapper.py not found. Skipping manifest generation."
  log "Generate later: python3 tools/context_mapper.py ."
fi

# ── Done ────────────────────────────────────────────────────
echo ""
success "Setup complete!"
log "Next steps:"
log "1. Edit .claude/QUICK_START.md & COMMON_MISTAKES.md with your project specifics"
log "2. Open your AI editor and start a new session"
log "3. Skill auto-activates. If not, paste: cat prompt/one-click-vertical-prompt.md"
log "4. Type 'RELOAD CONTEXT OPTIMIZER' anytime to reset behavior"
log "5. Re-run this script after major refactors to refresh CONTEXT_MANIFEST.md"
