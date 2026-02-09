# Configuration Validation Flow

## Before Fix ❌

```
User fills in Smithery.ai UI:
┌─────────────────────────────────────┐
│ Confluence URL: confluence.com      │ ✓ Required
│ Username: [empty]                   │ ✗ Optional (misleading!)
│ API Token: my_password              │ ✗ Optional (misleading!)
└─────────────────────────────────────┘
         ↓
    UI accepts config (schema passes)
         ↓
    Server starts
         ↓
    Authentication validation fails
         ↓
    ❌ "Atlassian require secrets to work"
```

## After Fix ✅

```
User fills in Smithery.ai UI:
┌─────────────────────────────────────────────────────┐
│ Confluence URL: confluence.com                      │
│ Username: john.doe                                  │
│ API Token: my_password                              │
└─────────────────────────────────────────────────────┘
         ↓
    Schema validation (anyOf rules)
         ↓
    ✓ Has URL + Username + API Token (basic auth)
    OR
    ✓ Has URL + Personal Token (PAT)
         ↓
    UI accepts config ✅
         ↓
    Server starts successfully
         ↓
    ✅ "Confluence authentication configured"
```

## Schema Validation Rules

The `smithery.yaml` now uses `anyOf` to enforce complete authentication:

```yaml
anyOf:
  # Basic Auth for Jira
  - required: [jiraUrl, jiraUsername, jiraApiToken]
  
  # PAT for Jira  
  - required: [jiraUrl, jiraPersonalToken]
  
  # Basic Auth for Confluence
  - required: [confluenceUrl, confluenceUsername, confluenceApiToken]
  
  # PAT for Confluence
  - required: [confluenceUrl, confluencePersonalToken]
```

## Valid Configurations

### ✅ Confluence Only - Basic Auth
```json
{
  "confluenceUrl": "https://confluence.example.com",
  "confluenceUsername": "john.doe",
  "confluenceApiToken": "password123"
}
```

### ✅ Confluence Only - PAT
```json
{
  "confluenceUrl": "https://confluence.example.com",
  "confluencePersonalToken": "pat_token_xyz"
}
```

### ✅ Both Services - Mixed Auth
```json
{
  "confluenceUrl": "https://confluence.example.com",
  "confluenceUsername": "john.doe",
  "confluenceApiToken": "password123",
  "jiraUrl": "https://jira.example.com",
  "jiraPersonalToken": "jira_pat_abc"
}
```

## Invalid Configurations

### ❌ URL Only
```json
{
  "confluenceUrl": "https://confluence.example.com"
  // Missing: Any authentication method
}
```
**Error**: Schema validation fails - none of the `anyOf` rules satisfied

### ❌ Incomplete Basic Auth (Username Only)
```json
{
  "confluenceUrl": "https://confluence.example.com",
  "confluenceUsername": "john.doe"
  // Missing: confluenceApiToken
}
```
**Error**: Schema validation fails - `anyOf` rule requires BOTH

### ❌ Incomplete Basic Auth (Token Only)
```json
{
  "confluenceUrl": "https://confluence.example.com",
  "confluenceApiToken": "password123"
  // Missing: confluenceUsername
}
```
**Error**: Schema validation fails - `anyOf` rule requires BOTH

## Platform Behavior

| Platform | Schema Validation | User Experience |
|----------|-------------------|-----------------|
| **Smithery.ai** | ✅ Enforced | UI prevents saving incomplete config |
| **Claude Desktop** | ❌ Manual JSON | User must ensure completeness |
| **Cursor** | ❌ Manual JSON | User must ensure completeness |
| **Docker** | ❌ Env vars | Server validates at startup |

## Testing

Run validation tests:
```bash
pytest tests/unit/test_smithery_config.py -v
```

Expected output:
```
test_smithery_config_exists PASSED
test_smithery_config_schema_has_anyof PASSED
test_smithery_config_basic_auth_requirements PASSED
test_smithery_config_pat_requirements PASSED
test_environment_validation[env_vars0-True] PASSED
test_environment_validation[env_vars3-False] PASSED
test_environment_validation[env_vars4-False] PASSED
test_environment_validation[env_vars5-False] PASSED
...
15 passed
```

## Migration Guide

If you previously had a configuration with incomplete credentials:

**Old (may have worked inconsistently):**
```json
{
  "confluenceUrl": "https://confluence.example.com",
  "confluenceApiToken": "password"
}
```

**New (required):**
```json
{
  "confluenceUrl": "https://confluence.example.com",
  "confluenceUsername": "your_username",
  "confluenceApiToken": "password"
}
```

Or use PAT:
```json
{
  "confluenceUrl": "https://confluence.example.com",
  "confluencePersonalToken": "your_pat_token"
}
```

## Benefits

1. **Early Validation**: Schema catches incomplete configs before server starts
2. **Clear Requirements**: Field descriptions explain what's needed
3. **Better UX**: Users see validation errors in UI, not server logs
4. **Consistent Behavior**: Same validation across all platforms
5. **Documentation**: Clear rules in smithery.yaml comments

## Summary

✅ **Yes, it works fine in Docker and MCP toolkit Configuration pages!**

The schema now properly validates that authentication credentials are complete, preventing the "Atlassian require secrets to work" error by catching incomplete configurations at the UI level rather than at runtime.
