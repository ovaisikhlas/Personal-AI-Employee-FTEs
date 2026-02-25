# Scripts Folder Update - Change Summary

## Overview

The AI Employee project structure has been reorganized. Core configuration files (`Dashboard.md`, `Company_Handbook.md`, `Business_Goals.md`) have been moved from the vault root to a new `/scripts` folder outside the vault.

---

## New Project Structure

```
Personal-AI-Employee-FTEs/
├── scripts/                    # ← NEW: Configuration files
│   ├── Dashboard.md
│   ├── Company_Handbook.md
│   └── Business_Goals.md
│
├── AI_Employee_Vault/          # Obsidian vault (data only)
│   ├── Inbox/
│   ├── Needs_Action/
│   ├── Pending_Approval/
│   ├── Approved/
│   ├── Done/
│   ├── Plans/
│   ├── Logs/
│   └── ... (other folders)
│
└── watchers/                   # Python scripts
    ├── orchestrator.py         # Updated to use scripts folder
    └── verify_bronze.py        # Updated to check scripts folder
```

---

## Why This Change?

### Benefits

1. **Separation of Concerns**
   - `/scripts` = Configuration & templates
   - `/vault` = Dynamic data & logs

2. **Git Sync Friendly**
   - Vault can be synced via Obsidian Sync
   - Configuration files versioned separately in Git

3. **Cleaner Vault**
   - Obsidian vault contains only working files
   - No template files cluttering the root

4. **Multiple Vaults**
   - One `/scripts` folder can serve multiple vaults
   - Easy to switch between test/production vaults

---

## Files Updated

### 1. `watchers/orchestrator.py`

**Changes:**
- Added `scripts_path` parameter to `__init__()`
- Default: `scripts` folder is sibling to vault
- Updated `self.dashboard` to point to `/scripts/Dashboard.md`
- Added `self.company_handbook` and `self.business_goals` paths
- Added `--scripts` argument to CLI

**Usage:**
```bash
# Default (scripts folder is sibling to vault)
python watchers/orchestrator.py "path/to/vault" --dashboard

# Custom scripts path
python watchers/orchestrator.py "path/to/vault" --scripts "custom/path/scripts" --dashboard
```

---

### 2. `watchers/verify_bronze.py`

**Changes:**
- Updated to check for files in `vault_parent/scripts/` instead of `vault/`
- Updated verification message: "KEY FILES (in scripts folder)"

---

### 3. `README.md`

**Changes:**
- Updated project structure diagram
- Added `/scripts` folder description
- Updated file locations in documentation

---

## Migration Steps (Already Completed)

1. ✅ Created `/scripts` folder
2. ✅ Moved `Dashboard.md` to `/scripts`
3. ✅ Moved `Company_Handbook.md` to `/scripts`
4. ✅ Moved `Business_Goals.md` to `/scripts`
5. ✅ Updated orchestrator to use new paths
6. ✅ Updated verification script
7. ✅ Tested all functionality

---

## Verification

```bash
# Run verification
python watchers/verify_bronze.py "path/to/vault"

# Expected output:
# ✓ Dashboard: .../scripts/Dashboard.md
# ✓ Company Handbook: .../scripts/Company_Handbook.md
# ✓ Business Goals: .../scripts/Business_Goals.md
```

---

## Usage Examples

### Update Dashboard

```bash
python watchers/orchestrator.py "C:\...\AI_Employee_Vault" --dashboard
```

**Output:**
```
2026-02-26 00:44:41 - Orchestrator - INFO - Scripts path: C:\...\scripts
2026-02-26 00:44:41 - Orchestrator - INFO - Dashboard updated
```

### Process Files

```bash
python watchers/orchestrator.py "C:\...\AI_Employee_Vault" --process
```

### Custom Scripts Path

```bash
python watchers/orchestrator.py "C:\...\AI_Employee_Vault" \
  --scripts "D:\Config\AI_Employee" \
  --process
```

---

## File Locations Reference

| File | Old Location | New Location |
|------|--------------|--------------|
| Dashboard | `AI_Employee_Vault/Dashboard.md` | `scripts/Dashboard.md` |
| Company Handbook | `AI_Employee_Vault/Company_Handbook.md` | `scripts/Company_Handbook.md` |
| Business Goals | `AI_Employee_Vault/Business_Goals.md` | `scripts/Business_Goals.md` |

---

## Backward Compatibility

The orchestrator automatically detects the scripts folder location:

1. **If `--scripts` argument provided:** Uses specified path
2. **Otherwise:** Assumes `scripts` folder is sibling to vault
3. **Legacy vaults:** Can still work by placing config files in vault root and updating paths

---

## Next Steps

### Recommended
- [ ] Update any custom scripts to use new paths
- [ ] Update documentation references
- [ ] Test with your workflow

### Optional
- [ ] Set up Git sync for `/scripts` folder
- [ ] Configure Obsidian Sync for `/AI_Employee_Vault` folder
- [ ] Create backup strategy for both folders

---

*Updated: 2026-02-26*
*AI Employee v0.1 - Scripts Folder Update*
