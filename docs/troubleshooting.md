# Troubleshooting Guide

Common issues and how to fix them.

## Installation Issues

### "Python not found"

**Problem:** Python isn't installed or not in PATH.

**Solution:**
```bash
# Check if Python is installed
python --version
# or
python3 --version

# If not installed, download from https://python.org
```

### "Permission denied" when running script

**Problem:** Script doesn't have execute permissions.

**Solution:**
```bash
# Make executable
chmod +x tools/context_mapper.py

# Or run with Python explicitly
python tools/context_mapper.py /path/to/project
```

## Manifest Generation Issues

### "No files indexed"

**Problem:** The indexer didn't find any files.

**Causes & Solutions:**

1. **Wrong path:**
   ```bash
   # Make sure path exists
   ls /path/to/project
   
   # Use absolute path
   python tools/context_mapper.py $(pwd)/my-project
   ```

2. **No supported file extensions:**
   ```bash
   # Check what files exist
   find /path/to/project -type f | head -20
   
   # Add custom extensions
   python tools/context_mapper.py /path/to/project --extensions .custom,.other
   ```

3. **All files in skipped directories:**
   ```bash
   # Check SKIP_DIRS in context_mapper.py
   # Remove directories you want to index
   ```

### "Manifest is empty"

**Problem:** Files found but no symbols extracted.

**Causes:**
- Files don't contain recognized keywords
- Files are minified/compiled
- Files use unusual formatting

**Solution:**
```python
# Add custom keywords for your codebase
KEYWORDS = {
    ".py": ["def ", "class ", "async def ", "your_custom_keyword "],
}
```

### "Unicode decode error"

**Problem:** Files with non-UTF-8 encoding.

**Solution:**
The script already handles this with `errors='ignore'`, but if you see issues:

```python
# In context_mapper.py, change the encoding detection
import chardet  # Note: requires external dependency

with open(filepath, 'rb') as f:
    raw = f.read()
    encoding = chardet.detect(raw)['encoding']
```

## Claude Integration Issues

### "Claude doesn't recognize the manifest"

**Problem:** Manifest not properly uploaded or referenced.

**Solutions:**

1. **For Projects:**
   - Go to Project Knowledge
   - Verify `CONTEXT_MANIFEST.md` is listed
   - Try re-uploading

2. **For Direct Chat:**
   - Make sure you paste the manifest at the start
   - Don't paste it after the conversation has started

3. **File too large:**
   - Split into multiple manifests
   - Filter out less important files

### "Claude still asks for full files"

**Problem:** Custom Instructions not active.

**Solutions:**

1. **Check Custom Instructions:**
   - Go to Project Settings
   - Verify instructions are saved
   - Make sure you're in the correct Project

2. **Restart chat:**
   - Custom Instructions apply to new chats
   - Existing chats won't have them

3. **Instructions not pasted correctly:**
   - Copy the entire file content
   - Don't include markdown code blocks

### "Token usage still high"

**Problem:** Optimization not working as expected.

**Check:**

1. **Are you using the one-click prompt?**
   ```
   Paste the prompt at the START of every chat
   ```

2. **Are you pasting full files?**
   ```
   ❌ Don't: [paste 500 lines]
   ✅ Do: Paste only lines Claude asks for
   ```

3. **Is the manifest current?**
   ```bash
   # Regenerate if codebase changed
   python tools/context_mapper.py /path/to/project
   ```

## Performance Issues

### "Indexing takes too long"

**Problem:** Large codebase with many files.

**Solutions:**

1. **Index specific directories:**
   ```bash
   python tools/context_mapper.py /project/src
   ```

2. **Exclude heavy directories:**
   ```python
   SKIP_DIRS = {
       # ... defaults ...
       "generated",
       "vendor",
       "third_party",
   }
   ```

3. **Index only specific extensions:**
   ```bash
   python tools/context_mapper.py /project --extensions .py,.js
   ```

### "Manifest is too large for Claude"

**Problem:** Very large codebase generates huge manifest.

**Solutions:**

1. **Filter by importance:**
   ```bash
   # Only core business logic
   python tools/context_mapper.py /project/src/core
   ```

2. **Split by module:**
   ```bash
   python tools/context_mapper.py /project/src/auth --output AUTH_MANIFEST.md
   python tools/context_mapper.py /project/src/api --output API_MANIFEST.md
   ```

3. **Post-process to remove noise:**
   ```bash
   # Remove test files
   grep -v "test_" CONTEXT_MANIFEST.md > CONTEXT_MANIFEST_CLEAN.md
   ```

## Claude-Specific Issues

### "Claude says it can't see the files"

**Problem:** Claude doesn't understand the manifest format.

**Solution:**
- Make sure you uploaded the manifest, not just mentioned it
- Paste a sample of the manifest format in your first message

### "Claude ignores the token budget"

**Problem:** Claude's default behavior overrides instructions.

**Solutions:**

1. **Be explicit:**
   ```
   Remember: Show me only lines 15-30, not the full file.
   ```

2. **Use emergency override:**
   ```
   TOKEN BUDGET OVERRIDE: Show me the full function
   ```

3. **Restart the chat:**
   - Sometimes Claude gets stuck in a pattern
   - Fresh chat often helps

### "Claude asks for lines that don't exist"

**Problem:** Manifest is outdated.

**Solution:**
```bash
# Regenerate the manifest
python tools/context_mapper.py /path/to/project

# Re-upload to Claude Project
```

## Getting Help

If your issue isn't covered here:

1. **Check the logs:**
   ```bash
   python tools/context_mapper.py /path/to/project --dry-run
   ```

2. **Open a GitHub Discussion:**
   - Include your Python version
   - Include the error message
   - Describe what you tried

3. **Test with a small project:**
   ```bash
   mkdir test_project
   echo "def hello(): pass" > test_project/test.py
   python tools/context_mapper.py test_project
   ```
