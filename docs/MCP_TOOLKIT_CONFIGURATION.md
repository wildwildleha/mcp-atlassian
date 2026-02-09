# MCP Toolkit Configuration Guide

This guide explains how to configure MCP Atlassian in various MCP toolkit configuration interfaces like Claude Desktop, Cursor, Smithery.ai, and other MCP-compatible applications.

## Configuration Validation

MCP Atlassian validates configuration at startup to ensure all required credentials are provided. The server will **not start** if authentication is incomplete, which may result in errors like:

- "Atlassian require secrets to work"
- "Authentication is not fully configured"
- "Service will be unavailable"

## Required Configuration

### Option 1: Basic Authentication (Username + Password/Token)

For basic authentication, **BOTH** username and API token/password must be provided:

**For Confluence:**
```json
{
  "confluenceUrl": "https://confluence.yourcompany.com",
  "confluenceUsername": "your_username",
  "confluenceApiToken": "your_password"
}
```

**For Jira:**
```json
{
  "jiraUrl": "https://jira.yourcompany.com",
  "jiraUsername": "your_username",
  "jiraApiToken": "your_password"
}
```

### Option 2: Personal Access Token (Server/DC Only)

For Server/DC with PAT support:

**For Confluence (7.9+):**
```json
{
  "confluenceUrl": "https://confluence.yourcompany.com",
  "confluencePersonalToken": "your_pat_token"
}
```

**For Jira (8.14+):**
```json
{
  "jiraUrl": "https://jira.yourcompany.com",
  "jiraPersonalToken": "your_pat_token"
}
```

## Common Configuration Errors

### ❌ Incomplete Basic Auth - Missing Username

```json
{
  "confluenceUrl": "https://confluence.yourcompany.com",
  "confluenceApiToken": "your_password"
  // Missing: confluenceUsername
}
```

**Error:** "Authentication is not fully configured"
**Fix:** Add `confluenceUsername`

### ❌ Incomplete Basic Auth - Missing API Token

```json
{
  "confluenceUrl": "https://confluence.yourcompany.com",
  "confluenceUsername": "your_username"
  // Missing: confluenceApiToken
}
```

**Error:** "Authentication is not fully configured"
**Fix:** Add `confluenceApiToken`

### ❌ URL Only (No Credentials)

```json
{
  "confluenceUrl": "https://confluence.yourcompany.com"
  // Missing: ANY authentication method
}
```

**Error:** "Atlassian require secrets to work"
**Fix:** Add either (username + apiToken) OR personalToken

## Platform-Specific Configuration

### Claude Desktop

Edit your configuration file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

**Example - Server/DC Basic Auth:**
```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "CONFLUENCE_URL": "https://confluence.yourcompany.com",
        "CONFLUENCE_USERNAME": "your_username",
        "CONFLUENCE_API_TOKEN": "your_password",
        "CONFLUENCE_SSL_VERIFY": "false"
      }
    }
  }
}
```

### Cursor

Open **Settings** → **MCP** → **+ Add new global MCP server**

Use the same JSON configuration as Claude Desktop.

### Smithery.ai

When configuring through Smithery.ai's web interface:

1. **Choose Authentication Method:**
   - Basic Auth: Fill in URL + Username + API Token
   - PAT: Fill in URL + Personal Token

2. **For Basic Auth** (e.g., Confluence 7.3.1):
   - ✅ Confluence URL: `https://confluence.yourcompany.com`
   - ✅ Confluence Username: `john.doe`
   - ✅ Confluence API Token: `YourActualPassword123`
   - ✅ Confluence SSL Verify: `false` (if self-signed cert)

3. **For PAT** (newer versions):
   - ✅ Confluence URL: `https://confluence.yourcompany.com`
   - ✅ Confluence Personal Token: `your_pat_token`
   - ✅ Confluence SSL Verify: `true`

### Docker Configuration

When using Docker, you can pass configuration via:

#### Environment Variables (Command Line)

```bash
docker run --rm -i \
  -e CONFLUENCE_URL=https://confluence.yourcompany.com \
  -e CONFLUENCE_USERNAME=your_username \
  -e CONFLUENCE_API_TOKEN=your_password \
  -e CONFLUENCE_SSL_VERIFY=false \
  ghcr.io/sooperset/mcp-atlassian:latest
```

#### Environment File

Create `.env` file:
```env
CONFLUENCE_URL=https://confluence.yourcompany.com
CONFLUENCE_USERNAME=your_username
CONFLUENCE_API_TOKEN=your_password
CONFLUENCE_SSL_VERIFY=false
```

Run with:
```bash
docker run --rm -i --env-file .env ghcr.io/sooperset/mcp-atlassian:latest
```

#### Docker Compose

See `docker-compose.example.yml` for complete examples.

## Validation Checklist

Before starting the server, ensure:

- [ ] **At least one service is configured** (Jira or Confluence or both)
- [ ] **For Basic Auth**: Both URL and (username + apiToken) are set
- [ ] **For PAT**: Both URL and personalToken are set
- [ ] **SSL Verification**: Set to `false` only for self-signed certificates
- [ ] **Credentials are correct**: Test login in web browser first

## Testing Your Configuration

Enable verbose logging to see authentication validation:

```json
{
  "env": {
    "CONFLUENCE_URL": "...",
    "CONFLUENCE_USERNAME": "...",
    "CONFLUENCE_API_TOKEN": "...",
    "MCP_VERBOSE": "true"
  }
}
```

**Look for these log messages:**

✅ Success:
- "Confluence configuration loaded and authentication is configured"
- "Using Confluence Server/Data Center authentication (PAT or Basic Auth)"

❌ Failure:
- "Confluence is not configured or required environment variables are missing"
- "Authentication is not fully configured. Confluence tools will be unavailable"

## Troubleshooting by Platform

### Smithery.ai Configuration Page

**Symptom**: "Atlassian require secrets to work" after saving configuration

**Causes:**
1. Only URL is filled, no credentials
2. Only username OR only apiToken is filled (not both)
3. Wrong authentication method for your version

**Solution:**
- For Basic Auth: Fill **all three**: URL + Username + API Token
- For PAT: Fill **both**: URL + Personal Token
- Check logs in Smithery console for detailed error messages

### Claude Desktop

**Symptom**: MCP server not appearing in tools list

**Causes:**
1. JSON syntax error in config file
2. Missing required fields
3. Server failed to start due to auth errors

**Solution:**
1. Validate JSON syntax (use a JSON validator)
2. Check Claude Desktop logs
3. Enable `MCP_VERBOSE: "true"` in env section
4. Restart Claude Desktop after config changes

### Docker

**Symptom**: Container exits immediately

**Causes:**
1. Missing environment variables
2. Authentication validation failed
3. Cannot connect to Confluence/Jira URL

**Solution:**
1. Run with `-e MCP_VERBOSE=true` to see logs
2. Verify all required env vars are set
3. Test URL accessibility: `curl -k https://confluence.yourcompany.com`
4. Check Docker network connectivity

## Schema Validation

The `smithery.yaml` configuration schema enforces:

```yaml
anyOf:
  - required: [jiraUrl, jiraUsername, jiraApiToken]
  - required: [jiraUrl, jiraPersonalToken]
  - required: [confluenceUrl, confluenceUsername, confluenceApiToken]
  - required: [confluenceUrl, confluencePersonalToken]
```

This means you must provide **one of** these complete combinations:
1. Jira with Basic Auth (URL + username + apiToken)
2. Jira with PAT (URL + personalToken)
3. Confluence with Basic Auth (URL + username + apiToken)
4. Confluence with PAT (URL + personalToken)

You can also configure **both** Jira and Confluence simultaneously.

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** or secret management tools
3. **Use PAT instead of passwords** when your version supports it
4. **Enable SSL verification** in production (only disable for dev/test)
5. **Rotate credentials regularly**
6. **Use read-only mode** if you only need to view data

## Getting Help

If configuration issues persist:

1. Enable verbose logging: `MCP_VERBOSE=true`
2. Check authentication works in web browser
3. Review server logs for specific error messages
4. See detailed guides:
   - [docs/authentication.mdx](./authentication.mdx) - Authentication methods
   - [docs/troubleshooting.mdx](./troubleshooting.mdx) - Common issues
   - [docs/CONFLUENCE_7.3_BASIC_AUTH.md](./CONFLUENCE_7.3_BASIC_AUTH.md) - Legacy version guide
5. Open an issue with logs (redact credentials!)

## Summary

The key takeaway: **Basic authentication requires BOTH username AND apiToken to be set together**. Providing only one will result in authentication failure and the "Atlassian require secrets to work" error.

The MCP toolkit configuration page (Smithery.ai, Claude Desktop, etc.) will now properly validate that complete authentication credentials are provided before allowing the server to start.
