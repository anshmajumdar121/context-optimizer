# 🦀 Example: Rust CLI Project

## Project Structure

```
my-rust-cli/
├── src/
│   ├── main.rs
│   ├── commands/
│   │   ├── mod.rs
│   │   ├── build.rs
│   │   └── deploy.rs
│   └── utils/
│       ├── mod.rs
│       └── config.rs
├── Cargo.toml
└── tests/
    └── integration_tests.rs
```

## Manifest Snippet

```markdown
📄 src/main.rs
L1: use clap::{Parser, Subcommand};
L8: #[derive(Parser)]
L9: struct Cli {
L15: fn main() {
L20: match cli.command {

📄 src/commands/build.rs
L3: pub fn execute(args: BuildArgs) -> Result<(), Box<dyn Error>> {
L8: fn compile_project(config: &Config) -> Result<PathBuf, Error> {
L15: fn validate_output(path: &Path) -> bool {

📄 src/utils/config.rs
L5: pub struct Config {
L8: impl Config {
L12: pub fn from_file(path: &Path) -> Result<Self, ConfigError> {
```

## Query

**User:** "Build command fails with 'config file not found' but I'm passing --config"

**Claude:**
```
📍 Scope: Checking manifest for build command and config handling...

Found:
- src/commands/build.rs (L3-15)
- src/utils/config.rs (L8-12)

Can you show me:
- src/commands/build.rs lines 3-20 (execute function)
- src/utils/config.rs lines 12-25 (from_file function)
- How you're calling the CLI (the exact command)
```

**User:** [Pastes code]

```rust
// src/commands/build.rs L3-12
pub fn execute(args: BuildArgs) -> Result<(), Box<dyn Error>> {
    let config = Config::from_file(&args.config)?;
    let output = compile_project(&config)?;
    Ok(())
}

// src/utils/config.rs L12-20
pub fn from_file(path: &Path) -> Result<Self, ConfigError> {
    let contents = fs::read_to_string(path)?;
    let config: Config = toml::from_str(&contents)?;
    Ok(config)
}
```

**Claude:**
```
📍 Scope: build.rs L3-12, config.rs L12-20
🧠 Analysis:
- L4 in build.rs: Config::from_file called with args.config
- L14 in config.rs: fs::read_to_string fails if file doesn't exist
- Issue: Error propagates without helpful context

⚠️ Impact:
- User sees generic "file not found" without knowing which file
- No suggestion of where config should be
- --config might be parsed incorrectly (check main.rs argument handling)

✅ Next:
1. Check src/main.rs L15-25 — how is --config parsed?
2. Add explicit check: if !path.exists() { return Err(...) }
3. Show default config location in error message

Show me src/main.rs lines 8-20 (Cli struct and argument parsing).
```

**Token savings: ~12x**

## Key Rust-Specific Patterns

The manifest captures:
- `fn ` for functions
- `impl ` for implementations
- `struct ` and `enum ` for types
- `mod ` for modules
- `trait ` for traits

This gives Claude the structural overview without the implementation details.
