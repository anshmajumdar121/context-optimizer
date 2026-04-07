# 🐍 Example: Python FastAPI Project

## Project Structure

```
my-fastapi-app/
├── app/
│   ├── main.py
│   ├── auth.py
│   ├── database.py
│   └── models.py
├── tests/
│   └── test_auth.py
└── requirements.txt
```

## Step 1: Generate Manifest

```bash
python tools/context_mapper.py ~/my-fastapi-app
```

**Output snippet (CONTEXT_MANIFEST.md):**

```markdown
📄 app/main.py
L1: from fastapi import FastAPI, Depends
L5: app = FastAPI()
L12: @app.get("/users/{user_id}")
L15: def get_user(user_id: int, db = Depends(get_db)):

📄 app/auth.py
L3: from jose import JWTError
L8: def create_access_token(data: dict):
L15: def verify_token(token: str):
L22: class AuthHandler:
L25:     def authenticate(self, username: str, password: str):
```

## Step 2: Start Claude Chat with One-Click Prompt

```
🔒 SESSION MODE: CONTEXT-OPTIMIZED CODING
[rest of prompt]
```

## Step 3: Ask Your Question

**User:** "Why is my JWT token verification failing?"

**Claude:**
```
📍 Scope: Looking at manifest, I see app/auth.py has token functions.

Can you show me:
- Lines 15-30 of app/auth.py (the verify_token function)
- Lines 40-50 if you have token validation middleware
```

**User:** [Pastes lines 15-30]

```python
L15: def verify_token(token: str):
L16:     try:
L17:         payload = jwt.decode(
L18:             token, 
L19:             SECRET_KEY, 
L20:             algorithms=[ALGORITHM]
L21:         )
L22:         return payload
L23:     except JWTError:
L24:         return None
L25:     except ExpiredSignatureError:
L26:         print("Token expired")
L27:         return None
```

**Claude:**
```
📍 Scope: app/auth.py L15-30
🧠 Analysis:
- Line 24 returns None on JWTError (generic)
- Line 27 also returns None on expiration
- Issue: Both errors return None — caller can't distinguish between invalid vs expired

⚠️ Impact:
- Any code calling verify_token() can't differentiate error types
- If you have expiration-based logic (refresh token flows), it's broken
- Check lines 45-60 where this function is called

✅ Next:
Change to raise specific exceptions or return error codes
Update caller (likely app/auth.py L50-55) to handle both cases
Show me the caller if you want specific fix
```

**User:** [Shows caller lines]

## Token saved: ~14,000 tokens vs pasting entire file.

## Full Conversation Token Count

| Action | Tokens |
|--------|--------|
| Initial prompt | ~400 |
| Manifest reference (already uploaded) | 0 |
| Paste 15 lines | ~200 |
| Claude response | ~350 |
| **TOTAL** | **~950** |

Without optimization: Would have pasted entire auth.py (~250 lines) + main.py → ~8,000 tokens.

**Savings: 8.4x**
