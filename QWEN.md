# Personal AI Employee FTEs

## Project Overview

This project is a **hackathon blueprint** for building a "Digital FTE" (Full-Time Equivalent) — an autonomous AI agent that manages personal and business affairs 24/7. The architecture is **local-first**, **agent-driven**, and uses **human-in-the-loop** patterns for sensitive actions.

**Core Concept:** Transform Claude Code from a reactive chatbot into a proactive business partner that:
- Monitors Gmail, WhatsApp, and filesystems via "Watcher" scripts
- Reasons about tasks using Obsidian Markdown as long-term memory
- Executes actions via MCP (Model Context Protocol) servers
- Provides a "Monday Morning CEO Briefing" with revenue, bottlenecks, and suggestions

**Tagline:** *Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.*

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PERCEPTION (Watchers)                    │
│  Gmail Watcher │ WhatsApp Watcher │ Filesystem Watcher      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              REASONING (Claude Code + Obsidian)             │
│  Dashboard.md │ Company_Handbook.md │ Plan.md │ Briefings   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  ACTION (MCP Servers)                       │
│  Email MCP │ Browser MCP │ Calendar MCP │ Payment MCP       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│            HUMAN-IN-THE-LOOP (Approval Workflow)            │
│  /Pending_Approval → /Approved → Execute → /Done            │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Brain** | Claude Code | Reasoning engine with Ralph Wiggum persistence loop |
| **Memory/GUI** | Obsidian | Local Markdown vault for dashboard and knowledge |
| **Senses** | Python Watchers | Monitor Gmail, WhatsApp, filesystems to trigger AI |
| **Hands** | MCP Servers | Execute external actions (email, browser, payments) |

## Project Structure

```
Personal-AI-Employee-FTEs/
├── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md  # Main blueprint
├── skills-lock.json          # Skill dependencies tracking
├── .qwen/skills/             # Installed AI skills
│   └── browsing-with-playwright/
│       ├── SKILL.md          # Browser automation skill documentation
│       ├── references/
│       │   └── playwright-tools.md  # MCP tool reference
│       └── scripts/
│           ├── mcp-client.py         # MCP client for Playwright
│           ├── start-server.sh       # Start Playwright MCP server
│           ├── stop-server.sh        # Stop Playwright MCP server
│           └── verify.py             # Server health check
└── .git/
```

## Building and Running

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Claude Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base & dashboard |
| Python | 3.13+ | Watcher scripts & orchestration |
| Node.js | v24+ LTS | MCP servers |
| GitHub Desktop | Latest | Version control |

### Hardware Requirements

- **Minimum:** 8GB RAM, 4-core CPU, 20GB free disk
- **Recommended:** 16GB RAM, 8-core CPU, SSD storage
- **For always-on:** Dedicated mini-PC or cloud VM

### Quick Start

1. **Set up Obsidian Vault:**
   ```bash
   mkdir AI_Employee_Vault
   cd AI_Employee_Vault
   # Create folders: /Inbox, /Needs_Action, /Done, /Pending_Approval, /Approved
   ```

2. **Verify Claude Code:**
   ```bash
   claude --version
   ```

3. **Start Playwright MCP Server (for browser automation):**
   ```bash
   # From project root
   bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh
   ```

4. **Verify Server:**
   ```bash
   python .qwen/skills/browsing-with-playwright/scripts/verify.py
   ```

5. **Stop Server (when done):**
   ```bash
   bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh
   ```

### Ralph Wiggum Persistence Loop

To keep Claude working autonomously until a task is complete:

```bash
# Start a Ralph loop
/ralph-loop "Process all files in /Needs_Action, move to /Done when complete" \
  --completion-promise "TASK_COMPLETE" \
  --max-iterations 10
```

**How it works:**
1. Orchestrator creates state file with prompt
2. Claude works on task
3. Claude tries to exit
4. Stop hook checks: Is task file in /Done?
5. YES → Allow exit; NO → Block exit, re-inject prompt (loop continues)

## Development Conventions

### Folder Structure (Obsidian Vault)

```
AI_Employee_Vault/
├── Dashboard.md              # Real-time summary
├── Company_Handbook.md       # Rules of engagement
├── Business_Goals.md         # Q1/Q2 objectives
├── Inbox/                    # Raw incoming items
├── Needs_Action/             # Items awaiting processing
├── In_Progress/<agent>/      # Claimed items (claim-by-move rule)
├── Pending_Approval/         # Awaiting human approval
├── Approved/                 # Approved actions (triggers execution)
├── Done/                     # Completed tasks
└── Briefings/                # CEO briefings (generated)
```

### Human-in-the-Loop Pattern

For sensitive actions (payments, sending emails), Claude writes an approval request:

```markdown
---
type: approval_request
action: payment
amount: 500.00
recipient: Client A
created: 2026-01-07T10:30:00Z
status: pending
---

## Payment Details
- Amount: $500.00
- To: Client A

## To Approve
Move this file to /Approved folder.
```

### Watcher Script Pattern

All Watchers follow the `BaseWatcher` abstract class:

```python
from pathlib import Path
from abc import ABC, abstractmethod

class BaseWatcher(ABC):
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval

    @abstractmethod
    def check_for_updates(self) -> list:
        '''Return list of new items to process'''
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        '''Create .md file in Needs_Action folder'''
        pass

    def run(self):
        while True:
            items = self.check_for_updates()
            for item in items:
                self.create_action_file(item)
            time.sleep(self.check_interval)
```

### Coding Style

- **Python:** Use type hints, follow PEP 8
- **Markdown:** Use YAML frontmatter for metadata
- **Error Handling:** Log errors gracefully; watchers should never crash
- **Security:** Never commit secrets, tokens, or credentials to Git

## Testing Practices

1. **Unit Tests:** Test individual watcher functions in isolation
2. **Integration Tests:** Verify watcher → Claude → MCP flow
3. **Approval Workflow Tests:** Ensure sensitive actions require approval

## Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12 hrs | Obsidian vault, 1 watcher, basic Claude integration |
| **Silver** | 20-30 hrs | 2+ watchers, Plan.md generation, 1 MCP server, HITL workflow |
| **Gold** | 40+ hrs | Full integration, Odoo accounting, Ralph Wiggum loop, audit logging |
| **Platinum** | 60+ hrs | Cloud deployment, domain specialization, A2A upgrade |

## MCP Servers

MCP (Model Context Protocol) servers are Claude Code's "hands" for interacting with external systems. Each server exposes specific capabilities that Claude can invoke.

### Recommended MCP Servers

| Server | Package/Command | Purpose | Sensitivity |
|--------|-----------------|---------|-------------|
| **Filesystem** | Built-in | Read/write vault files | Low |
| **Playwright Browser** | `@playwright/mcp` | Web automation, form filling | Medium |
| **Email (Gmail)** | Custom Node.js | Send/draft/search emails | High |
| **Calendar** | Custom Node.js | Create/update events | Medium |
| **Odoo Accounting** | `mcp-odoo-adv` | Invoices, payments, reports | High |
| **Slack** | Custom Node.js | Team communication | Medium |

### MCP Configuration for Claude Code

Create `~/.config/claude-code/mcp.json`:

```json
{
  "servers": [
    {
      "name": "filesystem",
      "command": "builtin",
      "args": ["--allowedPaths", "/path/to/AI_Employee_Vault"]
    },
    {
      "name": "browser",
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {
        "HEADLESS": "true"
      }
    },
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/email-mcp/index.js"],
      "env": {
        "GMAIL_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    {
      "name": "odoo",
      "command": "npx",
      "args": ["mcp-odoo-adv"],
      "env": {
        "ODOO_URL": "https://your-odoo-instance.com",
        "ODOO_API_KEY": "your-api-key"
      }
    }
  ]
}
```

### Human-in-the-Loop Pattern for MCP Actions

For sensitive actions (payments, sending emails), Claude writes an approval request file instead of acting directly:

```
/Pending_Approval/PAYMENT_Client_A_2026-01-07.md
    ↓ (user moves to /Approved)
/Approved/PAYMENT_Client_A_2026-01-07.md
    ↓ (Orchestrator triggers MCP)
Execute MCP action → Log → Move to /Done
```

### Available Playwright MCP Tools

The Playwright MCP server provides 22 tools:

| Category | Tools |
|----------|-------|
| **Navigation** | `browser_navigate`, `browser_navigate_back` |
| **Snapshot** | `browser_snapshot`, `browser_take_screenshot` |
| **Interaction** | `browser_click`, `browser_type`, `browser_fill_form`, `browser_hover`, `browser_drag` |
| **Dropdown** | `browser_select_option` |
| **JavaScript** | `browser_evaluate`, `browser_run_code` |
| **Wait** | `browser_wait_for` |
| **Browser Control** | `browser_close`, `browser_resize`, `browser_tabs`, `browser_install` |
| **Other** | `browser_console_messages`, `browser_network_requests`, `browser_handle_dialog`, `browser_file_upload`, `browser_press_key` |

**Read-only tools:** `browser_snapshot`, `browser_take_screenshot`, `browser_console_messages`, `browser_network_requests`, `browser_wait_for`

**Destructive tools:** All others (modify page state)

### Example: Email MCP Server Implementation

```javascript
// email-mcp/index.js
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { GmailAPI } from './gmail-client.js';

const server = new Server({
  name: 'email-mcp',
  version: '1.0.0',
}, {
  capabilities: {
    tools: {
      send_email: {
        description: 'Send an email',
        inputSchema: {
          to: { type: 'string' },
          subject: { type: 'string' },
          body: { type: 'string' },
          draft: { type: 'boolean', default: false }
        }
      },
      search_emails: {
        description: 'Search Gmail',
        inputSchema: {
          query: { type: 'string' },
          maxResults: { type: 'number', default: 10 }
        }
      }
    }
  }
});

server.setRequestHandler('tools/send_email', async (request) => {
  const { to, subject, body, draft } = request.params;
  if (draft) {
    await GmailAPI.createDraft(to, subject, body);
    return { content: [{ type: 'text', text: 'Draft created' }] };
  }
  await GmailAPI.send(to, subject, body);
  return { content: [{ type: 'text', text: 'Email sent' }] };
});

server.connect();
```

## Key Resources

- **Main Blueprint:** `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Playwright Skill:** `.qwen/skills/browsing-with-playwright/SKILL.md`
- **MCP Tools Reference:** `.qwen/skills/browsing-with-playwright/references/playwright-tools.md`
- **Ralph Wiggum Plugin:** https://github.com/anthropics/claude-code/tree/main/.claude/plugins/ralph-wiggum
- **MCP SDK:** https://github.com/modelcontextprotocol
- **Odoo MCP:** https://github.com/AlanOgic/mcp-odoo-adv

## Weekly Research Meeting

- **When:** Wednesdays at 10:00 PM (first meeting: Jan 7th, 2026)
- **Zoom:** https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1
- **YouTube:** https://www.youtube.com/@panaversity
