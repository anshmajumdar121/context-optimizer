# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes    |
| < 1.0   | ❌ No     |

## Reporting a Vulnerability

**Do NOT report security vulnerabilities through public GitHub issues.**

Instead, please email us at [INSERT SECURITY EMAIL] with:

- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact

You can expect:

| Response | Time |
|----------|------|
| Acknowledgment | Within 24 hours |
| Preliminary assessment | Within 48 hours |
| Fix or mitigation | Within 7 days (if critical) |

## Security Best Practices for Users

When using Context Optimizer:

1. **Never paste secrets into chat** — Claude doesn't need your API keys
2. **Run `context_mapper.py` only on trusted codebases**
3. **Review `CONTEXT_MANIFEST.md`** before uploading — it only contains structural info (no code bodies), but verify
4. **Use Claude Projects with knowledge** rather than pasting manifest content directly

## This Tool's Security Boundaries

Context Optimizer:

- ✅ Runs **entirely locally** — no network calls
- ✅ **Does not store** or transmit your code
- ✅ Uses **only standard library** — no risk of compromised dependencies
- ✅ Manifest contains **no full source code** — just file paths + line numbers + structural keywords

## Known Limitations

- Manifest can show sensitive **function/class names** if your codebase uses descriptive identifiers
- Line numbers might reveal code structure to Anthropic (same as any Claude conversation)

## Responsible Disclosure

We follow [responsible disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure) practices. If you find a vulnerability, report it privately first, give us time to fix it, then we'll coordinate public disclosure.

---

**Together we keep AI-assisted coding secure.**
