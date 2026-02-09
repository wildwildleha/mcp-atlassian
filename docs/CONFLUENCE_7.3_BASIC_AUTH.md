# Quick Reference: Confluence 7.3.1 Basic Authentication

This guide is for users with **Confluence 7.3.1** or other older Server/Data Center versions that **do not support Personal Access Tokens (PAT)**.

## What You Need

For Confluence 7.3.1 without PAT support, use **Basic Authentication** with:
- Your Confluence **username**
- Your Confluence **password**

## Configuration

### Environment Variables

Set these three environment variables:

```bash
CONFLUENCE_URL=https://confluence.yourcompany.com
CONFLUENCE_USERNAME=your_username
CONFLUENCE_API_TOKEN=your_password
```

⚠️ **Important**: Despite the name `API_TOKEN`, use your actual **password** for basic authentication.

### Optional: Self-Signed Certificates

If your Confluence uses self-signed SSL certificates:

```bash
CONFLUENCE_SSL_VERIFY=false
```

## Using with Docker

### Method 1: Command Line

```bash
docker run --rm -i \
  -e CONFLUENCE_URL=https://confluence.yourcompany.com \
  -e CONFLUENCE_USERNAME=your_username \
  -e CONFLUENCE_API_TOKEN=your_password \
  -e CONFLUENCE_SSL_VERIFY=false \
  ghcr.io/sooperset/mcp-atlassian:latest
```

### Method 2: Environment File

1. Create a `.env` file:
   ```bash
   CONFLUENCE_URL=https://confluence.yourcompany.com
   CONFLUENCE_USERNAME=your_username
   CONFLUENCE_API_TOKEN=your_password
   CONFLUENCE_SSL_VERIFY=false
   ```

2. Run with env file:
   ```bash
   docker run --rm -i --env-file .env ghcr.io/sooperset/mcp-atlassian:latest
   ```

### Method 3: Docker Compose

1. Copy `docker-compose.example.yml` to `docker-compose.yml`
2. Uncomment the `mcp-atlassian-basic-auth` section
3. Update the environment variables with your credentials
4. Run:
   ```bash
   docker compose run --rm mcp-atlassian-basic-auth
   ```

## Using with Claude Desktop / Cursor

### With uvx (No Docker)

Edit your MCP configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

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

### With Docker

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "CONFLUENCE_URL",
        "-e", "CONFLUENCE_USERNAME",
        "-e", "CONFLUENCE_API_TOKEN",
        "-e", "CONFLUENCE_SSL_VERIFY",
        "ghcr.io/sooperset/mcp-atlassian:latest"
      ],
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

## Common Issues

### "Atlassian require secrets to work"

**Cause**: Missing `USERNAME` or `API_TOKEN`

**Solution**: Make sure **both** are set:
```bash
CONFLUENCE_USERNAME=your_username  # ← Must be set
CONFLUENCE_API_TOKEN=your_password # ← Must be set
```

### SSL Certificate Errors

**Cause**: Self-signed or untrusted certificate

**Solution**:
```bash
CONFLUENCE_SSL_VERIFY=false
```

⚠️ **Security Note**: Only use `SSL_VERIFY=false` in development or when you trust your network. In production, properly configure SSL certificates.

### Connection Timeouts

**Possible causes**:
1. Wrong URL - verify it's accessible from your machine/Docker
2. Firewall blocking Docker containers
3. Need to configure HTTP proxy

**Solution for proxy**:
```bash
CONFLUENCE_HTTP_PROXY=http://proxy.yourcompany.com:8080
CONFLUENCE_HTTPS_PROXY=http://proxy.yourcompany.com:8080
```

## Testing Your Configuration

### Test Authentication

Enable verbose logging to debug issues:

```bash
# With uvx
MCP_VERBOSE=true uvx mcp-atlassian

# With Docker
docker run --rm -i \
  -e MCP_VERBOSE=true \
  -e CONFLUENCE_URL=https://confluence.yourcompany.com \
  -e CONFLUENCE_USERNAME=your_username \
  -e CONFLUENCE_API_TOKEN=your_password \
  ghcr.io/sooperset/mcp-atlassian:latest
```

Look for:
- ✅ "Confluence configuration loaded and authentication is configured"
- ✅ "Confluence authentication successful"
- ❌ Authentication errors or warnings

### Enable Debug Logging

For even more details:

```bash
MCP_VERY_VERBOSE=true
```

## Security Best Practices

1. **Never commit credentials** to version control
2. Use `.env` files and add them to `.gitignore`
3. Consider using environment variables from your shell/system
4. For production, use proper SSL certificates (don't disable SSL verification)
5. If your version supports it, upgrade to use Personal Access Tokens instead of passwords

## Need More Help?

- Full documentation: https://personal-1d37018d.mintlify.app/docs/authentication
- Troubleshooting: https://personal-1d37018d.mintlify.app/docs/troubleshooting
- Docker examples: See `docker-compose.example.yml` in the repository
- GitHub Issues: https://github.com/sooperset/mcp-atlassian/issues
