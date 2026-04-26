# Context Optimizer

> **Reduce token consumption by 5x–27x** in Claude Desktop/Web using prompt-native workflows + a lightweight local manifest generator.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Why This Exists

Claude has a **200K token context window** — but burning 20K tokens just to show a directory structure is wasteful. This toolkit teaches Claude to **fetch only what it needs**, **compress what it sees**, and **reason structurally** instead of reading raw files.

**No API hacks. No leaked code. No reverse engineering.**
Just official Claude features (Custom Instructions + Projects + Knowledge) and a lightweight local indexer.

## Real-World Savings

| Scenario | Before (tokens) | After (tokens) | Reduction |
|----------|----------------|----------------|-----------|
| Code review (3 files) | ~18,000 | ~1,200 | **15x** |
| Debug a function | ~8,000 | ~400 | **20x** |
| Plan a feature (5+ files) | ~35,000 | ~1,800 | **19x** |
| Full monorepo analysis | ~80,000 | ~3,500 | **22x** |

## Quick Start (30 seconds)

```bash
# 1. Clone the repo
git clone https://github.com/anshmajumdar121/context-optimizer.git
cd context-optimizer

# 2. Run the installer (idempotent, safe to re-run)
chmod +x scripts/install.sh
./scripts/install.sh /path/to/your/project

# 3. Generate a structural manifest of your project
python3 tools/context_mapper.py /path/to/your/project

# 4. Upload CONTEXT_MANIFEST.md to a Claude Project (optional but recommended)

# 5. Paste the one-click prompt into Claude Desktop/Web
cat prompt/one-click-vertical-prompt.md | pbcopy  # macOS
cat prompt/one-click-vertical-prompt.md | xclip   # Linux
```

## How It Works

```
Your Project
    │
    ▼
context_mapper.py ──► CONTEXT_MANIFEST.md
                            │
                            ▼
                    Claude Project Knowledge
                            │
                            ▼
                    skill/claude-custom-instructions.md
                    (via Custom Instructions or CLAUDE.md)
                            │
                            ▼
                    Token-Efficient Claude Sessions
```

### The Three Pillars

**1. CONTEXT_MANIFEST.md** — A structural index of your codebase: file paths, languages, line counts, import graphs, and blast-radius data. Claude reads this instead of scanning directories.

**2. Core Skill** — Custom instructions that enforce structural reasoning, limit file fetches to 3/turn, and compress all output into a strict format.

**3. Session Activator** — A one-click prompt to paste at the start of any session when you can't use Custom Instructions.

## File Structure

```
context-optimizer/
├── context-optimizer-skill/
│   ├── SKILL.md                     # Skill with YAML frontmatter (for skill registries)
│   └── LICENSE.txt
├── skill/
│   └── claude-custom-instructions.md  # Paste into Claude Custom Instructions
├── prompt/
│   └── one-click-vertical-prompt.md   # Paste at start of any session
├── scripts/
│   └── install.sh                   # Full-stack installer (idempotent)
├── tools/
│   └── context_mapper.py            # Manifest + dependency graph generator
├── .claude/
│   ├── COMMON_MISTAKES.md           # Project-specific bug history
│   ├── QUICK_START.md               # Daily commands
│   └── ARCHITECTURE_MAP.md          # High-level routing & layers
├── .claudeignore                    # Files excluded from Claude's context
└── docs/
    ├── learnings/                   # Session insights (gitignored)
    └── archive/                     # Old versions (gitignored)
```

## Usage Guide

### Option A: Claude Projects (Recommended)
1. Run `python3 tools/context_mapper.py /your/project`
2. Upload `CONTEXT_MANIFEST.md` to a Claude Project as Knowledge
3. Add `skill/claude-custom-instructions.md` to Project Instructions
4. Start chatting — Claude will reason from the manifest automatically

### Option B: Custom Instructions (Global)
1. Go to Claude Settings → Custom Instructions
2. Paste the contents of `skill/claude-custom-instructions.md`
3. For each project, paste `CONTEXT_MANIFEST.md` into the chat or upload it

### Option C: Per-Session Activation
1. Open any Claude chat
2. Paste `prompt/one-click-vertical-prompt.md` as your first message
3. Claude confirms: `✅ Context Optimizer active.`
4. Upload or paste `CONTEXT_MANIFEST.md` and start your task

### Option D: Claude Code / CLAUDE.md
Run the installer — it auto-detects `.claude/` and injects the skill into `CLAUDE.md`:
```bash
./scripts/install.sh /your/project
```

## Manifest Generator

```bash
# Basic usage
python3 tools/context_mapper.py /path/to/project

# Blast-radius analysis (find all files affected by a change)
python3 tools/context_mapper.py /path/to/project --blast-radius src/auth.py,src/models.py
```

**Output files:**
- `CONTEXT_MANIFEST.md` — Human + AI readable manifest
- `.claude/graph.json` — Machine-readable dependency graph

## Overrides & Controls

| Command | Effect |
|---------|--------|
| `RELOAD CONTEXT OPTIMIZER` | Reset all rules for this session |
| `MAX_FILES: 5` | Allow up to 5 files per turn |
| `BUDGET: 2000` | Raise token budget to 2,000 |
| `COMPRESSION: lite` | Less aggressive compression |
| `TEMP VERBOSE` | One-turn verbose mode, then revert |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome — especially for new language parsers in `context_mapper.py`.

## License

MIT — see [LICENSE](LICENSE).
