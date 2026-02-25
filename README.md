# AI Employee - Bronze Tier Implementation

A local-first, autonomous AI Employee built with Qwen Code and Obsidian. This is the **Bronze Tier** (Foundation) implementation that provides the minimum viable deliverable for the Personal AI Employee Hackathon.

## 🏆 Bronze Tier Deliverables

- [x] Obsidian vault with `Dashboard.md` and `Company_Handbook.md`
- [x] One working Watcher script (File System monitoring)
- [x] Qwen Code integration for reading/writing to the vault
- [x] Basic folder structure: `/Inbox`, `/Needs_Action`, `/Done`
- [x] All AI functionality implemented as Agent Skills

## 📁 Project Structure

```
Personal-AI-Employee-FTEs/
├── scripts/                  # Configuration and template files
│   ├── Dashboard.md          # Real-time status dashboard
│   ├── Company_Handbook.md   # Rules of engagement
│   └── Business_Goals.md     # Objectives and metrics
├── AI_Employee_Vault/        # Obsidian vault
│   ├── Inbox/                # Raw incoming items
│   │   └── Drop/             # File drop folder (watched)
│   ├── Needs_Action/         # Items awaiting processing
│   ├── Pending_Approval/     # Awaiting human approval
│   ├── Approved/             # Approved actions (ready to execute)
│   ├── Done/                 # Completed tasks
│   ├── Plans/                # Action plans created by Qwen Code
│   ├── Briefings/            # CEO briefings (generated)
│   ├── Logs/                 # System logs
│   ├── Invoices/             # Generated invoices
│   └── Accounting/           # Financial records
├── watchers/                 # Python watcher scripts
│   ├── base_watcher.py       # Abstract base class
│   ├── filesystem_watcher.py # File system monitor
│   ├── orchestrator.py       # Master coordination script
│   └── verify_bronze.py      # Bronze tier verification
└── README.md                 # This file
```

## ⚡ Quick Start

### Prerequisites

Ensure you have the following installed:

| Software | Version | Purpose |
|----------|---------|---------|
| Python | 3.13+ | Watcher scripts |
| Qwen Code | Active | Reasoning engine |
| Obsidian | v1.10.6+ | Knowledge base |

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd C:\Users\Administrator\Desktop\GitHub\Personal-AI-Employee-FTEs
   ```

2. **Install Python dependencies:**
   ```bash
   pip install watchdog
   ```

3. **Set up environment variables:**
   ```bash
   # Copy the example env file
   cp watchers/.env.example watchers/.env
   
   # Edit watchers/.env with your actual values
   ```

4. **Verify Qwen Code:**
   ```bash
   qwen --version
   ```

### Running the Bronze Tier

#### Option 1: Start the File Watcher

The File Watcher monitors the `Inbox/Drop` folder for new files:

```bash
# Start the watcher (runs continuously)
python watchers/filesystem_watcher.py "C:\Users\Administrator\Desktop\GitHub\Personal-AI-Employee-FTEs\AI_Employee_Vault"
```

**Keep this running in a terminal window** - it will watch for new files 24/7.

#### Option 2: Process Files with Qwen Code

When files appear in `Needs_Action`, process them:

```bash
# Navigate to vault
cd AI_Employee_Vault

# Run Qwen Code to process files
qwen --prompt "Check /Needs_Action folder and create action plans for each file. Follow the Company_Handbook.md rules."
```

#### Option 3: Use the Orchestrator

The orchestrator automates processing:

```bash
# Process once
python watchers/orchestrator.py "C:\Users\Administrator\Desktop\GitHub\Personal-AI-Employee-FTEs\AI_Employee_Vault" --process

# Run continuous mode (checks every 60 seconds)
python watchers/orchestrator.py "C:\Users\Administrator\Desktop\GitHub\Personal-AI-Employee-FTEs\AI_Employee_Vault" --continuous --interval 60

# Update dashboard only
python watchers/orchestrator.py "C:\Users\Administrator\Desktop\GitHub\Personal-AI-Employee-FTEs\AI_Employee_Vault" --dashboard
```

## 🔄 How It Works

### File Drop Workflow

1. **Drop a file** into `AI_Employee_Vault/Inbox/Drop/`
2. **File Watcher detects** the new file
3. **Watcher creates:**
   - Copy of file in `/Needs_Action/`
   - Metadata `.md` file with context
4. **Orchestrator processes** the action file
5. **Qwen Code creates** a plan in `/Plans/`
6. **Human reviews** and approves if needed
7. **Action executes** and moves to `/Done/`

### Example: Processing a Document

```bash
# 1. Drop a file
echo "Please review this contract" > "AI_Employee_Vault/Inbox/Drop/contract.txt"

# 2. Watcher creates:
#    - /Needs_Action/FILE_contract.txt
#    - /Needs_Action/FILE_contract.txt.md

# 3. Process with Qwen Code
qwen --prompt "Process FILE_contract.txt.md in /Needs_Action. Create a plan and identify if approval is needed."

# 4. Qwen Code creates:
#    - /Plans/PLAN_FILE_contract.txt.md

# 5. Review the plan, then approve if needed
#    Move approval file from /Pending_Approval to /Approved

# 6. Execute approved action
python watchers/orchestrator.py "path/to/vault" --approved
```

## 📊 Dashboard

The `Dashboard.md` provides real-time visibility:

- Pending tasks count
- Folder statistics
- Recent activity
- System status

It auto-updates when the orchestrator runs.

## 📘 Company Handbook

The `Company_Handbook.md` defines rules for autonomous operation:

- **Communication rules** (email, WhatsApp)
- **Financial thresholds** (auto-approve vs. require approval)
- **File operation permissions**
- **Escalation rules** (when to wake a human)
- **Security policies**

**Key Rule:** Any payment, sensitive action, or irreversible operation requires human approval.

## 🧪 Testing the Bronze Tier

### Test 1: File Drop

1. Start the File Watcher:
   ```bash
   python watchers/filesystem_watcher.py "path/to/vault"
   ```

2. Drop a test file:
   ```bash
   echo "Test content" > "AI_Employee_Vault/Inbox/Drop/test.txt"
   ```

3. Verify files created in `/Needs_Action/`

### Test 2: Qwen Code Processing

1. Navigate to vault:
   ```bash
   cd AI_Employee_Vault
   ```

2. Run Qwen Code:
   ```bash
   qwen
   ```

3. Prompt:
   ```
   Read the file in /Needs_Action folder. Create a step-by-step plan 
   in /Plans folder following the Company_Handbook.md rules.
   ```

### Test 3: Approval Workflow

1. Create an approval request manually:
   ```markdown
   ---
   type: approval_request
   action: test_action
   created: 2026-02-25T00:00:00Z
   ---
   
   # Test Approval Request
   
   Move this file to /Approved to approve.
   ```

2. Save to `/Pending_Approval/TEST.md`

3. Move to `/Approved/`

4. Run orchestrator:
   ```bash
   python watchers/orchestrator.py "path/to/vault" --approved
   ```

5. Verify file moved to `/Done/`

## 🔧 Configuration

### Watcher Intervals

Edit the watcher scripts to change check intervals:

```python
# In filesystem_watcher.py
watcher = FilesystemWatcher(
    vault_path, 
    check_interval=5  # Seconds between checks
)
```

### Logging

All logs are stored in `/Logs/` folder:

- `watcher_FilesystemWatcher.log` - File watcher logs
- `orchestrator_YYYYMMDD.log` - Daily orchestrator logs
- `YYYY-MM-DD.jsonl` - Action audit logs

## 🚀 Next Steps (Silver Tier)

After mastering Bronze, add:

1. **Gmail Watcher** - Monitor email for urgent messages
2. **WhatsApp Watcher** - Detect keywords in messages
3. **MCP Server** - Send emails autonomously
4. **Scheduled Tasks** - Cron/Task Scheduler integration
5. **Enhanced HITL** - Full approval workflow

## 📝 Agent Skills

All AI functionality should be implemented as [Qwen Agent Skills](https://platform.qwen.ai/docs/en/agents-and-tools/agent-skills/overview):

### Bronze Tier Skills

| Skill | Description |
|-------|-------------|
| `process_inbox` | Process files in /Needs_Action |
| `create_plan` | Create action plans in /Plans |
| `update_dashboard` | Refresh dashboard stats |
| `log_action` | Write to audit logs |
| `request_approval` | Create approval request files |

## 🐛 Troubleshooting

### Watcher doesn't detect files

- Ensure the `Inbox/Drop` folder exists
- Check watcher is running: `ps aux | grep filesystem_watcher`
- Verify folder permissions allow read/write

### Qwen Code errors

- Verify installation: `qwen --version`
- Check you're in the vault directory
- Ensure files have `.md` extension

### Orchestrator fails

- Check Python version: `python --version` (need 3.13+)
- Install dependencies: `pip install watchdog`
- Check logs in `/Logs/` folder

## 📚 Resources

- **Main Blueprint:** `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Claude Code Docs:** https://claude.com/product/claude-code
- **Obsidian Help:** https://help.obsidian.md
- **Watchdog Docs:** https://pypi.org/project/watchdog/

## ✅ Bronze Tier Checklist

Before considering Bronze Tier complete:

- [ ] Vault folder structure created
- [ ] Dashboard.md displays correct counts
- [ ] Company_Handbook.md reviewed and customized
- [ ] File Watcher runs without errors
- [ ] Dropping a file creates action file in Needs_Action
- [ ] Qwen Code can read and write to vault
- [ ] Approval workflow tested (Pending → Approved → Done)
- [ ] Logs are being written to /Logs folder

---

*AI Employee v0.1 - Bronze Tier*
*Built for Personal AI Employee Hackathon 2026*
