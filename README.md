# context-optimizer

**5â27x fewer tokens. No setup required to start.**

Use the skill alone â no install needed, works anywhere Claude runs.  
Add Python 3.7+ to unlock auto-manifest generation.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

| Tool | What it cuts | Install needed |
|------|-------------|----------------|
| ðª¨ [Caveman](https://github.com/JuliusBrussee/caveman) | Output tokens (~75%) | One command |
| ð¬ [code-review-graph](https://github.com/tirth8205/code-review-graph) | Input tokens (8.2xÂ²) | pip + Python 3.10+ |
| ðï¸ Context Optimizer | Input tokens (see benchmarks) | Zero to start |

Â² [code-review-graph benchmarks](https://github.com/tirth8205/code-review-graph#benchmarks)

## Why This Exists

Claude has a **200K token context window** â but burning 20K tokens just to show a directory structure is wasteful. This toolkit teaches Claude to **fetch only what it needs**, **compress what it sees**, and **reason structurally** instead of reading raw files.

**No API hacks. No leaked code. No reverse engineering.**
Just official Claude features (Custom Instructions + Projects + Knowledge) and a lightweight local indexer.

## Real-World Savings

| Scenario | Before (tokens) | After (tokens) | Reduction |
|----------|----------------|----------------|-----------|
| Code review (3 files) | ~18,000 | ~1,200 | **15x** |
| Debug a function | ~8,000 | ~400 | **20x** |
| Plan a feature (5+ files) | ~35,000 | ~1,800 | **19x** |
| Full monorepo analysis | ~80,000 | ~3,500 | **22x** |

## How it works in practice

Without Context Optimizer, Claude reads every file it thinks
might be relevant â often 10â15 files before answering.

With Context Optimizer, Claude reads the manifest first,
fetches 2â3 targeted files, then answers. Same result.
Fraction of the context.

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
    â
    â¼
context_mapper.py âââº CONTEXT_MANIFEST.md
                            â
                            â¼
                    Claude Project Knowledge
                            â
                            â¼
                    skill/claude-custom-instructions.md
                    (via Custom Instructions or CLAUDE.md)
                            â
                            â¼
                    Token-Efficient Claude Sessions
```

### The Three Pillars

**1. CONTEXT_MANIFEST.md** â A structural index of your codebase: file paths, languages, line counts, import graphs, and blast-radius data. Claude reads this instead of scanning directories.

**2. Core Skill** â Custom instructions that enforce structural reasoning, limit file fetches to 3/turn, and compress all output into a strict format.

**3. Session Activator** â A one-click prompt to paste at the start of any session when you can't use Custom Instructions.

## File Structure

```
context-optimizer/
âââ context-optimizer-skill/
â   âââ SKILL.md                     # Skill with YAML frontmatter (for skill registries)
â   âââ LICENSE.txt
âââ skill/
â   âââ claude-custom-instructions.md  # Paste into Claude Custom Instructions
âââ prompt/
â   âââ one-click-vertical-prompt.md   # Paste at start of any session
âââ scripts/
â   âââ install.sh                   # Full-stack installer (idempotent)
âââ tools/
â   âââ context_mapper.py            # Manifest + dependency graph generator
âââ .claude/
â   âââ COMMON_MISTAKES.md           # Project-specific bug history
â   âââ QUICK_START.md               # Daily commands
â   âââ ARCHITECTURE_MAP.md          # High-level routing & layers
âââ .claudeignore                    # Files excluded from Claude's context
âââ docs/
    âââ learnings/                   # Session insights (gitignored)
    âââ archive/                     # Old versions (gitignored)
```

## Usage Guide

### Option A: Claude Projects (Recommended)
1. Run `python3 tools/context_mapper.py /your/project`
2. Upload `CONTEXT_MANIFEST.md` to a Claude Project as Knowledge
3. Add `skill/claude-custom-instructions.md` to Project Instructions
4. Start chatting â Claude will reason from the manifest automatically

### Option B: Custom Instructions (Global)
1. Go to Claude Settings â Custom Instructions
2. Paste the contents of `skill/claude-custom-instructions.md`
3. For each project, paste `CONTEXT_MANIFEST.md` into the chat or upload it

### Option C: Per-Session Activation
1. Open any Claude chat
2. Paste `prompt/one-click-vertical-prompt.md` as your first message
3. Claude confirms: `â Context Optimizer active.`
4. Upload or paste `CONTEXT_MANIFEST.md` and start your task

### Option D: Claude Code / CLAUDE.md
Run the installer â it auto-detects `.claude/` and injects the skill into `CLAUDE.md`:
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
- `CONTEXT_MANIFEST.md` â Human + AI readable manifest
- `.claude/graph.json` â Machine-readable dependency graph

## Overrides & Controls

| Command | Effect |
|---------|--------|
| `RELOAD CONTEXT OPTIMIZER` | Reset all rules for this session |
| `MAX_FILES: 5` | Allow up to 5 files per turn |
| `BUDGET: 2000` | Raise token budget to 2,000 |
| `COMPRESSION: lite` | Less aggressive compression |
| `TEMP VERBOSE` | One-turn verbose mode, then revert |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome â especially for new language parsers in `context_mapper.py`.

## License

MIT â see [LICENSE](LICENSE).
