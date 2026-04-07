# Usage Guide

Get started with Context Optimizer in 5 minutes.

## Prerequisites

- Python 3.8+ installed
- A codebase to analyze
- Claude Desktop or Web access

## Step 1: Generate a Manifest

Navigate to your project and run the mapper:

```bash
# Clone the context-optimizer repo
git clone https://github.com/yourusername/context-optimizer.git
cd context-optimizer

# Generate manifest for your project
python tools/context_mapper.py /path/to/your/project
```

This creates `CONTEXT_MANIFEST.md` in your current directory.

### Example Output

```
✅ Manifest generated: CONTEXT_MANIFEST.md
   Files indexed: 47
   Symbols found: 312
   Size: ~8KB
```

## Step 2: Upload to Claude

### Option A: Claude Projects (Recommended)

1. Go to [claude.ai](https://claude.ai)
2. Create a new Project
3. Click "Project Knowledge" → "Add Content"
4. Upload `CONTEXT_MANIFEST.md`
5. Add the Custom Instructions (see Step 3)

### Option B: Direct Chat

1. Start a new chat
2. Paste the contents of `CONTEXT_MANIFEST.md`
3. Add the one-click prompt (see Step 3)

## Step 3: Add the Skill

### For Projects (Persistent)

1. Go to Project Settings
2. Find "Custom Instructions"
3. Copy the contents of `skill/claude-custom-instructions.md`
4. Paste into the Custom Instructions field
5. Save

### For Single Chat

1. Copy the contents of `prompt/one-click-vertical-prompt.md`
2. Paste at the start of your chat
3. Add your question after the prompt

## Step 4: Start Chatting

Now when you ask questions, Claude will:

1. Check the manifest for relevant files
2. Request specific line ranges (not full files)
3. Provide compressed, structured responses

### Example Interaction

**You:** "Why is authentication failing?"

**Claude:**
```
📍 Scope: Checking CONTEXT_MANIFEST.md for auth-related files...

Found: src/auth/login.py (L12-45)

Can you show me:
- Lines 15-30 (the authenticate function)
- Lines 40-45 (error handling)
```

**You:** [Pastes the requested lines]

**Claude:**
```
📍 Scope: src/auth/login.py L15-30, L40-45
🧠 Analysis:
- L24: Returns None on JWTError (generic)
- L27: Also returns None on ExpiredSignatureError
- Issue: Caller can't distinguish invalid vs expired tokens

⚠️ Impact:
- Breaks refresh token flows
- Security: Can't enforce expiration-based policies

✅ Next:
Change to raise specific exceptions or return error codes.
Show me lines 50-55 where verify_token is called.
```

## Tips for Best Results

### 1. Keep Manifest Updated

Regenerate the manifest when you:
- Add new files
- Rename functions/classes
- Do major refactoring

```bash
python tools/context_mapper.py /path/to/project
```

### 2. Use Line Ranges

When Claude asks for lines, paste only what's requested:

✅ **Good:**
```
L15: def authenticate(username, password):
L16:     try:
L17:         user = get_user(username)
```

❌ **Don't:**
```
[Entire 100-line file]
```

### 3. Regenerate on Major Changes

If your codebase changes significantly, regenerate the manifest:

```bash
python tools/context_mapper.py /path/to/project --output CONTEXT_MANIFEST.md
```

## Troubleshooting

### "Manifest not found"

Make sure you:
1. Generated the manifest successfully
2. Uploaded it to the Claude Project
3. Are in the correct Project chat

### "Claude still asks for full files"

Check that:
1. Custom Instructions are properly set
2. You're using the correct Project/chat
3. The prompt was pasted at the start

### "Manifest is too large"

For very large codebases:

```bash
# Index only specific extensions
python tools/context_mapper.py /path/to/project --extensions .py,.js

# Or manually edit the manifest to remove less important files
```

## Next Steps

- Read the [Customization Guide](customization.md) to tailor for your stack
- Check [Benchmarks](benchmarks.md) for real token savings
- See [Architecture](architecture.md) for how it works
