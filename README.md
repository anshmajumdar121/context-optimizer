# 🧠 Context Optimizer for Claude AI

> **Reduce token consumption by 5x–27x** in Claude Desktop/Web using prompt-native workflows + a lightweight local manifest generator.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Claude Compatible](https://img.shields.io/badge/Claude-3.5+-green.svg)](https://claude.ai)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

🌐 **[Live Preview](https://anshmajumdar121.github.io/context-optimizer/)** — See the interactive documentation

---

## ✨ Why This Exists

Claude has a **200K token context window** — but burning 20K tokens just to show a directory structure is wasteful. This toolkit teaches Claude to **fetch only what it needs**, **compress what it sees**, and **reason structurally** instead of reading raw files.

**No API hacks. No leaked code. No reverse engineering.**  
Just official Claude features (Custom Instructions + Projects + Knowledge) and a lightweight local indexer.

### 😱 The Problem

Most AI tools waste tokens by reading your entire project. Context Optimizer uses a structural graph to fetch only what matters.

![The Token Problem](https://sc01.alicdn.com/kf/S19c0bac015d54cb59f50bf6c198971f7u.png)

*Comparison: Without Graph (13,205 tokens) vs With Graph (1,928 tokens)*

---

## 📊 Real-World Savings

| Scenario | Before (tokens) | After (tokens) | Reduction |
|----------|----------------|----------------|-----------|
| Code review (3 files) | ~18,000 | ~1,200 | **15x** |
| Debug a function | ~8,000 | ~400 | **20x** |
| Plan a feature (5+ files) | ~35,000 | ~1,800 | **19x** |
| Full monorepo analysis | ~80,000 | ~3,500 | **22x** |

*Measured on Claude 3.5 Sonnet with typical prompts*

---

## 🚀 Quick Start (30 seconds)

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/context-optimizer.git
cd context-optimizer

# 2. Generate a structural manifest of your project
python tools/context_mapper.py /path/to/your/project

# 3. Upload CONTEXT_MANIFEST.md to a Claude Project (optional but recommended)

# 4. Paste the one-click prompt into Claude Desktop/Web
cat prompt/one-click-vertical-prompt.md | pbcopy  # macOS
# or manually copy-paste
```

That's it. Claude will now ask for specific files, not entire directories.

---

## ⚙️ How It Works

Your code is parsed into a persistent graph. We calculate the "blast radius" of changes to give your AI precise context instantly.

### The Pipeline

![How It Works - Pipeline](https://sc01.alicdn.com/kf/S6bc5b4bfc5c24d7abb49d0f0e03eaf40O.png)

*Repository → Tree-sitter Parser → SQLite Graph → Blast Radius → Minimal Review Set*

### Blast Radius Visualization

![Blast Radius Network](https://sc01.alicdn.com/kf/S5073b20c8ca74ba19b6551fcaaa7e1bcc.png)

*Network graph showing how a change in `auth.py: login()` affects connected components*

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     YOUR CODEBASE                            │
└─────────────────────┬───────────────────────────────────────┘
                      │ (Run once or on major changes)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  context_mapper.py → generates CONTEXT_MANIFEST.md          │
│  (compressed structural index: 5-15KB for 10K+ files)       │
└─────────────────────┬───────────────────────────────────────┘
                      │ (Upload to Claude Project or paste)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  CLAUDE SKILL (Custom Instructions)                         │
│  • Enforces fetch-on-demand                                  │
│  • Compresses every response                                 │
│  • Tracks token budget                                       │
└─────────────────────┬───────────────────────────────────────┘
                      │ (During chat)
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Claude → Requests only needed files → Returns structured   │
│  output (Summary, Impact, Next Steps)                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 💻 Installation

One command sets up everything. The installer auto-detects your AI tools and injects the correct configuration.

![One Install Every Platform](https://sc01.alicdn.com/kf/S66ffcffbb3804ed2ba50201de11c4755C.png)

*Supported platforms: Claude Code, Cursor, Windsurf, Zed, Continue, OpenCode, Antigravity*

### Quick Install

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/anshmajumdar121/context-optimizer/main/scripts/install.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/anshmajumdar121/context-optimizer/main/scripts/install.ps1 | iex
```

### Manual Install

```bash
git clone https://github.com/anshmajumdar121/context-optimizer.git
cd context-optimizer
python tools/context_mapper.py /path/to/your/project
```

---

## 📦 What's Inside

| Path | Purpose |
|------|---------|
| `skill/claude-custom-instructions.md` | Persistent workflow for ALL Claude sessions |
| `prompt/one-click-vertical-prompt.md` | Instant token-saving mode for single chats |
| `tools/context_mapper.py` | Zero-dependency Python indexer |
| `docs/usage-guide.md` | Step-by-step with screenshots |
| `docs/benchmarks.md` | Real token measurements |
| `examples/` | Language-specific demos |

---

## 🎯 Supported Languages

The indexer automatically detects these extensions:

| Language | Extensions |
|----------|------------|
| Python | `.py` |
| JavaScript/TypeScript | `.js`, `.ts`, `.jsx`, `.tsx` |
| Rust | `.rs` |
| Go | `.go` |
| Java/Kotlin | `.java`, `.kt` |
| C/C++ | `.c`, `.cpp`, `.h` |
| Ruby | `.rb` |
| PHP | `.php` |
| Swift | `.swift` |

Add more in 2 seconds — edit `INDEX_EXTENSIONS` in `context_mapper.py`

---

## 🛠️ Customization

```python
# In skill/claude-custom-instructions.md
MAX_FILES_PER_TURN: 3        # Lower = more savings
PREFER_SNIPPETS_OVER_FULL: true
ENABLE_RISK_SCORING: true    # Security warnings on API changes

# In tools/context_mapper.py
INDEX_EXTENSIONS = {".py", ".js", ".ts", ".rs", ".go"}  # Add yours
SKIP_DIRS = {"node_modules", ".git", "dist"}            # Skip build artifacts
```

---

## 🔒 Ethical & Legal Compliance

| ✅ We Do | ❌ We Don't |
|----------|-------------|
| Use official Claude features | Reverse-engineer APIs |
| Generate clean-room code | Leak proprietary prompts |
| Publish under MIT License | Bypass rate limits |
| Work entirely locally | Require cloud dependencies |

Zero copyrighted Anthropic code. This is 100% original implementation.

---

## 🏗️ Architecture Deep Dive

See how Context Optimizer hooks into the loop. Skills and MCP tools ensure Claude queries the graph instead of scanning files manually.

![How Claude Code Uses the Graph](https://sc01.alicdn.com/kf/Saf9783ee7e334b979c5492de692b569ej.png)

*Vertical flowchart: User → Claude Code → MCP Server → graph.db → Precise Review*

---

## 📖 Documentation

- [Usage Guide](docs/usage-guide.md) — Get running in 5 minutes
- [Customization](docs/customization.md) — Tailor for your stack
- [Benchmarks](docs/benchmarks.md) — Real token measurements
- [Troubleshooting](docs/troubleshooting.md) — Common issues
- [Architecture Deep Dive](docs/architecture.md) — How it works

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

All contributions must be original (no leaked code). By contributing, you agree to the MIT License.

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 🐛 Reporting Issues

Open an issue with:
- Claude version (Desktop/Web, 3.5 Sonnet/Opus)
- Your project size (files, languages)
- Expected vs actual token usage
- Steps to reproduce

---

## 💬 Support

- **Discussions:** GitHub Discussions tab
- **Documentation:** `/docs` folder
- **Quick questions:** Open a Discussion with `Q&A` label

---

## 🙏 Acknowledgments

- Claude team for building a capable, steerable model
- Open source community for clean-room inspiration
- Early testers who reported real token savings

---

## 📜 License

MIT License — use it anywhere, modify freely, contribute back if you can.

---

Built with ❤️ by developers who care about token efficiency.

[Report Bug](https://github.com/anshmajumdar121/context-optimizer/issues) · [Request Feature](https://github.com/anshmajumdar121/context-optimizer/issues) · [Read Docs](docs/usage-guide.md)
