# SOP: MCP Server Configuration

**Purpose:** Document how we add and manage Model Context Protocol (MCP) servers for Claude Code and Claude Desktop
**Applies To:** All MCP integrations in this project
**Last Updated:** 2025-12-08

## Overview

MCP servers extend Claude's capabilities by providing access to external tools, APIs, and data sources. We configure MCPs using the Claude Code CLI for terminal usage and JSON configuration files for Claude Desktop.

## The Standard

### Transport Types

We use three transport types depending on the MCP server:

| Transport | Use Case | Example |
|-----------|----------|---------|
| `stdio` | Local processes, Docker containers | n8n-mcp via Docker |
| `http` | Local HTTP servers | Archon at localhost:8051 |
| `sse` | Remote streaming servers | Deprecated, avoid |

### Adding MCPs to Claude Code

We use the `claude mcp add` CLI command rather than editing JSON directly:

```bash
# HTTP transport (for local servers)
claude mcp add --transport http <name> <url>

# STDIO transport (for Docker/local processes)
claude mcp add --transport stdio <name> -- <command>
```

### Configuration Scopes

| Scope | Location | Use Case |
|-------|----------|----------|
| User | `~/.claude.json` | Personal MCPs, available in all projects |
| Project | `.mcp.json` | Team MCPs, committed to git |
| Local | `.claude/settings.local.json` | Project-specific, not committed |

### Claude Desktop Configuration

We edit the JSON config file directly:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

## On-Demand vs Always-On

MCPs can be configured two ways:

| Approach | When to Use | Trade-off |
|----------|-------------|-----------|
| **Always-on** | Frequently used MCPs (e.g., Archon) | Convenience vs resource usage |
| **On-demand** | Occasional use, heavy resource MCPs | Manual add/remove vs lower overhead |

**On-demand workflow:**
```bash
# When starting work that needs the MCP
claude mcp add --scope user --transport stdio <name> -- <command>

# When done
claude mcp remove <name>
```

**Note:** There is no `claude mcp enable/disable` command. MCPs are either configured (and loaded on startup) or removed.

## Rationale

- **CLI over JSON editing:** The `claude mcp add` command handles escaping and validation automatically
- **Docker for isolation:** Docker-based MCPs provide consistent environments and easy updates
- **STDIO for Claude integrations:** Required mode for Claude Code/Desktop to communicate with MCPs
- **On-demand for heavy MCPs:** Docker-based MCPs that aren't used daily should be added/removed as needed to avoid unnecessary resource consumption

## Examples

### Good: Docker-based MCP with STDIO

```bash
claude mcp add --transport stdio n8n-mcp -- docker run -i --rm --init \
  -e MCP_MODE=stdio \
  -e LOG_LEVEL=error \
  ghcr.io/czlonkowski/n8n-mcp:latest
```

### Good: Local HTTP server

```bash
claude mcp add --transport http archon http://localhost:8051/mcp
```

### Good: Claude Desktop JSON config

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init",
        "-e", "MCP_MODE=stdio",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
```

### Anti-Patterns

```bash
# Don't manually edit ~/.claude.json for MCPs
# Use 'claude mcp add' instead

# Don't use HTTP mode for Claude integrations
# Claude Code/Desktop require STDIO mode

# Don't forget MCP_MODE=stdio for Docker MCPs
# JSON parse errors will occur without it
```

## Exceptions

- **Archon MCP:** Uses HTTP transport because it runs as a local server, not a Docker container
- **Testing:** May temporarily edit JSON directly for debugging

## Managing MCPs

```bash
# List all configured MCPs
claude mcp list

# Get details about a specific MCP
claude mcp get <name>

# Remove an MCP
claude mcp remove <name>
```

## Updating Docker-based MCPs

```bash
docker pull <image>:latest
# Then restart Claude Code / Claude Desktop
```

## Related Documentation

- [FEAT-005: n8n MCP Integration](../features/FEAT-005_n8n_mcp_integration/notes.md)
- [Claude Code MCP Docs](https://docs.claude.com/en/docs/claude-code/mcp)

## Agent Enforcement

Agents should:
- Verify MCPs are configured before attempting to use MCP tools
- Check `claude mcp list` output when debugging MCP issues
- Recommend STDIO transport for new Docker-based MCPs
- Flag any manual JSON editing of `~/.claude.json` for MCPs
