# MCP Atlassian

![PyPI Version](https://img.shields.io/pypi/v/mcp-atlassian)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mcp-atlassian)
![PePy - Total Downloads](https://static.pepy.tech/personalized-badge/mcp-atlassian?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Total%20Downloads)
[![Run Tests](https://github.com/sooperset/mcp-atlassian/actions/workflows/tests.yml/badge.svg)](https://github.com/sooperset/mcp-atlassian/actions/workflows/tests.yml)
![License](https://img.shields.io/github/license/sooperset/mcp-atlassian)
[![Docs](https://img.shields.io/badge/docs-mintlify-blue)](https://personal-1d37018d.mintlify.app)

Model Context Protocol (MCP) server for Atlassian products (Confluence and Jira). Supports both Cloud and Server/Data Center deployments.

https://github.com/user-attachments/assets/35303504-14c6-4ae4-913b-7c25ea511c3e

<details>
<summary>Confluence Demo</summary>

https://github.com/user-attachments/assets/7fe9c488-ad0c-4876-9b54-120b666bb785

</details>

## Quick Start

### 1. Get Your API Token

Go to https://id.atlassian.com/manage-profile/security/api-tokens and create a token.

> **Server/Data Center users**: Use a Personal Access Token (PAT) if supported by your version. For older versions (e.g., Confluence 7.3.1, Jira < 8.14) that don't support PAT, use basic authentication with username and password. See [Authentication](https://personal-1d37018d.mintlify.app/docs/authentication) for details.

### 2. Configure Your IDE

Add to your Claude Desktop or Cursor MCP configuration:

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_USERNAME": "your.email@company.com",
        "JIRA_API_TOKEN": "your_api_token",
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "your.email@company.com",
        "CONFLUENCE_API_TOKEN": "your_api_token"
      }
    }
  }
}
```

> **Python 3.14 not yet supported.** Use `["--python=3.12", "mcp-atlassian"]` as args if needed.

> **Server/Data Center users**: 
> - **PAT (recommended)**: Use `JIRA_PERSONAL_TOKEN` / `CONFLUENCE_PERSONAL_TOKEN` for newer versions
> - **Basic Auth (legacy)**: Use `USERNAME` + `API_TOKEN` (as password) for older versions that don't support PAT
> - See [Authentication](https://personal-1d37018d.mintlify.app/docs/authentication) for complete details and examples.


### 3. Start Using

Ask your AI assistant to:
- **"Find issues assigned to me in PROJ project"**
- **"Search Confluence for onboarding docs"**
- **"Create a bug ticket for the login issue"**
- **"Update the status of PROJ-123 to Done"**

## Docker Deployment Guide

This step-by-step guide walks you through deploying MCP Atlassian using Docker and integrating it with MCP toolkit applications.

### Prerequisites

Before you begin, ensure you have:

- ✅ **Docker installed** ([Install Docker](https://docs.docker.com/get-docker/))
- ✅ **Atlassian credentials** (API token or Personal Access Token)
- ✅ **Your Atlassian instance URL(s)** (Jira/Confluence)
- ✅ **MCP-compatible application** (Claude Desktop, Cursor, or similar)

### Step 1: Pull the Docker Image

Pull the latest MCP Atlassian image from GitHub Container Registry:

```bash
docker pull ghcr.io/sooperset/mcp-atlassian:latest
```

> **Note**: You can also build from source using the included Dockerfile.

### Step 2: Create Configuration File

Create a `.env` file with your Atlassian credentials. Choose one of the following configurations based on your setup:

<details>
<summary><b>Option A: Atlassian Cloud (API Token)</b></summary>

Create a `.env` file:

```bash
# Atlassian Cloud Configuration
JIRA_URL=https://your-company.atlassian.net
JIRA_USERNAME=your.email@company.com
JIRA_API_TOKEN=your_jira_api_token

CONFLUENCE_URL=https://your-company.atlassian.net/wiki
CONFLUENCE_USERNAME=your.email@company.com
CONFLUENCE_API_TOKEN=your_confluence_api_token
```

Get your API token from: https://id.atlassian.com/manage-profile/security/api-tokens

</details>

<details>
<summary><b>Option B: Server/Data Center (Personal Access Token)</b></summary>

Create a `.env` file:

```bash
# Server/Data Center with PAT (Jira 8.14+, Confluence 7.9+)
JIRA_URL=https://jira.yourcompany.com
JIRA_PERSONAL_TOKEN=your_jira_pat_token
JIRA_SSL_VERIFY=true

CONFLUENCE_URL=https://confluence.yourcompany.com
CONFLUENCE_PERSONAL_TOKEN=your_confluence_pat_token
CONFLUENCE_SSL_VERIFY=true
```

</details>

<details>
<summary><b>Option C: Server/Data Center (Basic Auth - Legacy)</b></summary>

For older versions without PAT support (e.g., Confluence 7.3.1):

```bash
# Server/Data Center with Basic Auth
CONFLUENCE_URL=https://confluence.yourcompany.com
CONFLUENCE_USERNAME=your_username
CONFLUENCE_API_TOKEN=your_password
CONFLUENCE_SSL_VERIFY=false

JIRA_URL=https://jira.yourcompany.com
JIRA_USERNAME=your_username
JIRA_API_TOKEN=your_password
JIRA_SSL_VERIFY=false
```

⚠️ **Important**: For basic auth, use your actual password in `API_TOKEN` field.

</details>

### Step 3: Test the Docker Container

Verify your configuration by running the container:

```bash
docker run --rm -i --env-file .env ghcr.io/sooperset/mcp-atlassian:latest
```

**Expected output:**
- ✅ "Jira configuration loaded and authentication is configured."
- ✅ "Confluence configuration loaded and authentication is configured."

**If you see errors**, enable verbose logging:

```bash
docker run --rm -i --env-file .env \
  -e MCP_VERBOSE=true \
  ghcr.io/sooperset/mcp-atlassian:latest
```

### Step 4: Integrate with MCP Toolkit

Choose your preferred MCP toolkit application:

<details>
<summary><b>Claude Desktop Integration</b></summary>

1. **Locate your Claude Desktop config file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Add the MCP server configuration:**

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "JIRA_URL",
        "-e", "JIRA_USERNAME",
        "-e", "JIRA_API_TOKEN",
        "-e", "CONFLUENCE_URL",
        "-e", "CONFLUENCE_USERNAME",
        "-e", "CONFLUENCE_API_TOKEN",
        "ghcr.io/sooperset/mcp-atlassian:latest"
      ],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_USERNAME": "your.email@company.com",
        "JIRA_API_TOKEN": "your_jira_api_token",
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "your.email@company.com",
        "CONFLUENCE_API_TOKEN": "your_confluence_api_token"
      }
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Verify**: The MCP Atlassian tools should now appear in Claude's tool list.

</details>

<details>
<summary><b>Cursor Integration</b></summary>

1. **Open Cursor Settings** → **MCP** → **+ Add new global MCP server**

2. **Use the same JSON configuration as Claude Desktop** (see above)

3. **Save and restart Cursor**

</details>

<details>
<summary><b>Smithery.ai Integration</b></summary>

1. **Visit Smithery.ai** and connect your Atlassian instance

2. **Fill in the configuration form:**
   - Confluence URL: `https://confluence.yourcompany.com`
   - Confluence Username: `your_username`
   - Confluence API Token: `your_password`
   - (Same for Jira if needed)

3. **Save configuration** - Schema validation ensures complete credentials

</details>

### Step 5: Using Docker Compose (Optional)

For persistent deployments or multiple configurations:

1. **Copy the example compose file:**

```bash
cp docker-compose.example.yml docker-compose.yml
```

2. **Edit `docker-compose.yml`** and uncomment your preferred configuration

3. **Run with Docker Compose:**

```bash
# Start the service
docker compose up -d mcp-atlassian-basic-auth

# View logs
docker compose logs -f mcp-atlassian-basic-auth

# Stop the service
docker compose down
```

See [docker-compose.example.yml](docker-compose.example.yml) for complete examples.

### Step 6: Verify Everything Works

Test your setup by asking your AI assistant:

```
"Search Confluence for onboarding documentation"
"Find my open Jira tickets in PROJECT-NAME"
"Create a test issue in PROJECT-NAME"
```

### Troubleshooting

**Problem: "Atlassian require secrets to work"**
- **Cause**: Incomplete credentials (missing username or token)
- **Fix**: Ensure BOTH username AND API_TOKEN are set for basic auth

**Problem: SSL Certificate Errors**
- **Cause**: Self-signed or untrusted certificates
- **Fix**: Set `CONFLUENCE_SSL_VERIFY=false` and `JIRA_SSL_VERIFY=false`

**Problem: Container exits immediately**
- **Cause**: Authentication failure or configuration error
- **Fix**: Run with `-e MCP_VERBOSE=true` to see detailed logs

**Problem: Cannot connect to Atlassian**
- **Cause**: Network issues, firewall, or wrong URL
- **Fix**: Test URL accessibility: `curl -k https://your-confluence-url`

For more help, see:
- [Troubleshooting Guide](https://personal-1d37018d.mintlify.app/docs/troubleshooting)
- [MCP Toolkit Configuration](docs/MCP_TOOLKIT_CONFIGURATION.md)
- [Confluence 7.3.1 Guide](docs/CONFLUENCE_7.3_BASIC_AUTH.md)

### Quick Reference

**Pull image:**
```bash
docker pull ghcr.io/sooperset/mcp-atlassian:latest
```

**Run with env file:**
```bash
docker run --rm -i --env-file .env ghcr.io/sooperset/mcp-atlassian:latest
```

**Run with inline env vars:**
```bash
docker run --rm -i \
  -e CONFLUENCE_URL=https://confluence.example.com \
  -e CONFLUENCE_USERNAME=user \
  -e CONFLUENCE_API_TOKEN=pass \
  ghcr.io/sooperset/mcp-atlassian:latest
```

**Enable debug logging:**
```bash
docker run --rm -i --env-file .env \
  -e MCP_VERBOSE=true \
  -e MCP_VERY_VERBOSE=true \
  ghcr.io/sooperset/mcp-atlassian:latest
```

## Building and Deploying from a Specific Branch

If you want to deploy a specific branch (e.g., a feature branch or development version) instead of the pre-built latest release, follow these steps:

### Prerequisites

- ✅ **Git installed** ([Install Git](https://git-scm.com/downloads))
- ✅ **Docker installed** ([Install Docker](https://docs.docker.com/get-docker/))
- ✅ **Atlassian credentials** (for testing your deployment)

### Step 1: Clone the Repository and Checkout the Branch

Clone the repository and switch to your desired branch:

```bash
# Clone the repository
git clone https://github.com/wildwildleha/mcp-atlassian.git
cd mcp-atlassian

# List available branches
git branch -a

# Checkout the specific branch you want to deploy
git checkout branch-name

# Or checkout a remote branch
git checkout -b local-branch-name origin/remote-branch-name
```

**Common branch examples:**
- `main` - Stable main branch
- `develop` or `dev` - Development branch
- `feature/new-feature` - Feature branch
- `fix/bug-description` - Bug fix branch

### Step 2: Build the Docker Image from Source

Build a Docker image from the branch you checked out:

```bash
# Build with a descriptive tag
docker build -t mcp-atlassian:branch-name .

# Or build with a version tag
docker build -t mcp-atlassian:feature-xyz .

# View your built images
docker images mcp-atlassian
```

**Build options:**
```bash
# Build with no cache (clean build)
docker build --no-cache -t mcp-atlassian:branch-name .

# Build with build arguments
docker build --build-arg PYTHON_VERSION=3.10 -t mcp-atlassian:branch-name .

# Build and view output
docker build -t mcp-atlassian:branch-name . --progress=plain
```

### Step 3: Test the Built Image

Test your newly built image with your configuration:

```bash
# Test with environment file
docker run --rm -i --env-file .env mcp-atlassian:branch-name

# Test with inline environment variables
docker run --rm -i \
  -e CONFLUENCE_URL=https://confluence.example.com \
  -e CONFLUENCE_USERNAME=user \
  -e CONFLUENCE_API_TOKEN=token \
  mcp-atlassian:branch-name

# Test with verbose logging
docker run --rm -i --env-file .env \
  -e MCP_VERBOSE=true \
  mcp-atlassian:branch-name
```

### Step 4: Use the Custom Image in Your MCP Configuration

Update your MCP toolkit configuration to use your custom-built image:

**Claude Desktop / Cursor Configuration:**

```json
{
  "mcpServers": {
    "mcp-atlassian": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "JIRA_URL",
        "-e", "JIRA_USERNAME",
        "-e", "JIRA_API_TOKEN",
        "-e", "CONFLUENCE_URL",
        "-e", "CONFLUENCE_USERNAME",
        "-e", "CONFLUENCE_API_TOKEN",
        "mcp-atlassian:branch-name"
      ],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_USERNAME": "your.email@company.com",
        "JIRA_API_TOKEN": "your_jira_api_token",
        "CONFLUENCE_URL": "https://your-company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "your.email@company.com",
        "CONFLUENCE_API_TOKEN": "your_confluence_api_token"
      }
    }
  }
}
```

> **Note**: Replace `mcp-atlassian:branch-name` with the tag you used when building the image.

### Step 5: Using Docker Compose with Custom Build

You can also use Docker Compose to build from source. Create or modify `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mcp-atlassian-branch:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mcp-atlassian-branch
    stdin_open: true
    tty: false
    env_file:
      - .env
```

**Docker Compose commands:**

```bash
# Build the image
docker compose build

# Build without cache
docker compose build --no-cache

# Run the service
docker compose run --rm mcp-atlassian-branch

# Start as a background service (for HTTP transport)
docker compose up -d mcp-atlassian-branch

# View logs
docker compose logs -f mcp-atlassian-branch

# Stop the service
docker compose down
```

### Step 6: Managing Multiple Branch Images

Keep track of different branch builds:

```bash
# Tag images with descriptive names
docker build -t mcp-atlassian:main .
docker build -t mcp-atlassian:feature-xyz .
docker build -t mcp-atlassian:dev .

# List all your mcp-atlassian images
docker images mcp-atlassian

# Remove old/unused images
docker rmi mcp-atlassian:old-branch

# Clean up unused images
docker image prune
```

### Updating to a Newer Version of the Branch

When the branch is updated on GitHub:

```bash
# Pull latest changes
git pull origin branch-name

# Rebuild the image
docker build -t mcp-atlassian:branch-name .

# Restart your MCP toolkit to use the updated image
```

### Troubleshooting Branch Deployments

**Problem: Build fails with "uv lock" errors**
- **Cause**: Network issues or dependency conflicts
- **Fix**: Ensure you have internet connectivity and try `docker build --no-cache`

**Problem: Image builds but doesn't work**
- **Cause**: The branch may have breaking changes or missing dependencies
- **Fix**: Check the branch's README or recent commits for setup requirements

**Problem: Can't find branch**
- **Cause**: Branch doesn't exist locally or remotely
- **Fix**: Run `git fetch --all` to update remote branches, then `git branch -a` to list all

**Problem: Docker build is slow**
- **Cause**: Docker is downloading dependencies
- **Fix**: This is normal for first build; subsequent builds use cache

### Best Practices for Branch Deployments

1. **Tag images clearly**: Use descriptive tags like `feature-name` or `dev-yyyy-mm-dd`
2. **Test before deploying**: Always test the built image before integrating with your MCP toolkit
3. **Document the branch**: Note which branch/commit you deployed for troubleshooting
4. **Keep branches updated**: Regularly pull updates if testing an active development branch
5. **Clean up old images**: Remove unused branch images to save disk space

### Quick Reference for Branch Deployment

```bash
# Clone and build from a specific branch
git clone https://github.com/wildwildleha/mcp-atlassian.git
cd mcp-atlassian
git checkout branch-name
docker build -t mcp-atlassian:branch-name .

# Test the image
docker run --rm -i --env-file .env mcp-atlassian:branch-name

# Use in Docker Compose (add to docker-compose.yml)
docker compose build
docker compose run --rm mcp-atlassian-branch
```

## Documentation

Full documentation is available at **[personal-1d37018d.mintlify.app](https://personal-1d37018d.mintlify.app)**.

Documentation is also available in [llms.txt format](https://llmstxt.org/), which LLMs can consume easily:
- [`llms.txt`](https://personal-1d37018d.mintlify.app/llms.txt) — documentation sitemap
- [`llms-full.txt`](https://personal-1d37018d.mintlify.app/llms-full.txt) — complete documentation

| Topic | Description |
|-------|-------------|
| [Installation](https://personal-1d37018d.mintlify.app/docs/installation) | uvx, Docker, pip, from source |
| [Authentication](https://personal-1d37018d.mintlify.app/docs/authentication) | API tokens, PAT, OAuth 2.0 |
| [Configuration](https://personal-1d37018d.mintlify.app/docs/configuration) | IDE setup, environment variables |
| [HTTP Transport](https://personal-1d37018d.mintlify.app/docs/http-transport) | SSE, streamable-http, multi-user |
| [Tools Reference](https://personal-1d37018d.mintlify.app/docs/tools-reference) | All Jira & Confluence tools |
| [Troubleshooting](https://personal-1d37018d.mintlify.app/docs/troubleshooting) | Common issues & debugging |

## Compatibility

| Product | Deployment | Support |
|---------|------------|---------|
| Confluence | Cloud | Fully supported |
| Confluence | Server/Data Center | Supported (v6.0+) |
| Jira | Cloud | Fully supported |
| Jira | Server/Data Center | Supported (v8.14+) |

## Key Tools

| Jira | Confluence |
|------|------------|
| `jira_search` - Search with JQL | `confluence_search` - Search with CQL |
| `jira_get_issue` - Get issue details | `confluence_get_page` - Get page content |
| `jira_create_issue` - Create issues | `confluence_create_page` - Create pages |
| `jira_update_issue` - Update issues | `confluence_update_page` - Update pages |
| `jira_transition_issue` - Change status | `confluence_add_comment` - Add comments |
| `jira_get_issue_sla` - Calculate SLA metrics | `confluence_get_page_views` - Get page view stats (Cloud only) |

See [Tools Reference](https://personal-1d37018d.mintlify.app/docs/tools-reference) for the complete list.

## Security

Never share API tokens. Keep `.env` files secure. See [SECURITY.md](SECURITY.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup.

## License

MIT - See [LICENSE](LICENSE). Not an official Atlassian product.
