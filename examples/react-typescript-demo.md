# ⚛️ Example: React TypeScript Project

## Project Structure

```
my-react-app/
├── src/
│   ├── components/
│   │   ├── UserProfile.tsx
│   │   └── Dashboard.tsx
│   ├── hooks/
│   │   └── useAuth.ts
│   ├── utils/
│   │   └── api.ts
│   └── types/
│       └── user.ts
```

## Manifest Snippet

```markdown
📄 src/components/UserProfile.tsx
L5: interface UserProfileProps {
L8: const UserProfile: React.FC<UserProfileProps> = ({ userId }) => {
L12:   const { user, loading } = useUser(userId);
L18:   if (loading) return <Spinner />;

📄 src/hooks/useAuth.ts
L3: export const useAuth = () => {
L6:   const [token, setToken] = useState<string | null>(null);
L10:   const login = async (email: string, password: string) => {
L15:   const logout = () => {
```

## Query

**User:** "Why does UserProfile show stale data after logout?"

**Claude:**
```
📍 Scope: Looking at manifest — UserProfile.tsx uses useUser() hook, useAuth.ts handles logout.

Can you show me:
- src/hooks/useAuth.ts lines 10-25 (login/logout logic)
- src/components/UserProfile.tsx lines 8-25 (component body)
```

**User:** [Pastes both sections — ~30 lines total]

**Claude:**
```
📍 Scope: useAuth.ts L10-25, UserProfile.tsx L8-25
🧠 Analysis:
- useAuth.ts L15: logout() clears token but doesn't trigger re-render
- UserProfile.tsx L12: useUser() depends on userId prop, not auth state
- Root cause: No dependency on token from useAuth()

⚠️ Impact:
- After logout, UserProfile still shows cached user data
- Security risk (UI shows logged-in state)
- Affects all components using useUser() without auth check

✅ Next:
Add const { token } = useAuth() to UserProfile
Add useEffect to clear user when token becomes null
Show me src/hooks/useUser.ts if you want exact implementation
```

**Token savings: ~15x**
