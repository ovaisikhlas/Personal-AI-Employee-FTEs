"""
Orchestrator - Master process for AI Employee

This script orchestrates all watchers and processes files in the Needs_Action folder.
It serves as the central coordination point for the AI Employee system.

Features:
- Start/stop all watchers
- Process files in Needs_Action folder using Qwen Code
- Update Dashboard.md with current stats
- Handle approval workflow

Usage:
    python orchestrator.py <vault_path> [--process] [--watchers] [--dashboard]
"""

import sys
import subprocess
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import re

# Handle both package import and direct script execution
try:
    from .base_watcher import BaseWatcher
except ImportError:
    from base_watcher import BaseWatcher


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.
    
    Coordinates watchers, processes action files, and maintains the dashboard.
    """
    
    def __init__(self, vault_path: str, scripts_path: str = None):
        """
        Initialize the orchestrator.

        Args:
            vault_path: Path to the Obsidian vault root
            scripts_path: Optional path to scripts folder (default: parent/vault/scripts)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        
        # Scripts folder (outside vault) contains Dashboard, Handbook, Business_Goals
        if scripts_path:
            self.scripts_path = Path(scripts_path)
        else:
            # Default: scripts folder is sibling to vault
            self.scripts_path = self.vault_path.parent / 'scripts'
        
        self.dashboard = self.scripts_path / 'Dashboard.md'
        self.company_handbook = self.scripts_path / 'Company_Handbook.md'
        self.business_goals = self.scripts_path / 'Business_Goals.md'

        # Ensure directories exist
        for folder in [self.needs_action, self.approved, self.done, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)

        # Set up logging
        self._setup_logging()

        # Watcher processes
        self.watcher_processes: List[subprocess.Popen] = []

        self.logger.info(f'Orchestrator initialized for vault: {self.vault_path}')
        self.logger.info(f'Scripts path: {self.scripts_path}')
    
    def _setup_logging(self):
        """Set up logging configuration."""
        log_file = self.logs / f'orchestrator_{datetime.now().strftime("%Y%m%d")}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('Orchestrator')
    
    def process_needs_action(self) -> int:
        """
        Process all files in the Needs_Action folder.

        Uses Qwen Code to analyze and create action plans for each file.

        Returns:
            Number of files processed
        """
        files = list(self.needs_action.glob('*.md'))
        
        if not files:
            self.logger.info('No files to process in Needs_Action')
            return 0
        
        self.logger.info(f'Found {len(files)} file(s) to process')
        
        processed = 0
        for file_path in files:
            try:
                self._process_single_file(file_path)
                processed += 1
            except Exception as e:
                self.logger.error(f'Error processing {file_path.name}: {e}')
        
        self.logger.info(f'Processed {processed} file(s)')
        return processed
    
    def _process_single_file(self, file_path: Path):
        """
        Process a single action file using Qwen Code.

        Args:
            file_path: Path to the file to process
        """
        self.logger.info(f'Processing: {file_path.name}')

        # Read the file content
        content = file_path.read_text()

        # Create a prompt for Qwen Code
        prompt = self._create_process_prompt(file_path, content)

        # Log the action
        self._log_action('process_file', str(file_path.name))

        # For Bronze tier: Create a Plan.md file for Qwen Code to work with
        plan_path = self.vault_path / 'Plans' / f'PLAN_{file_path.stem}.md'
        plan_content = self._create_plan_template(file_path, content)
        plan_path.write_text(plan_content, encoding='utf-8')

        self.logger.info(f'Created plan: {plan_path.name}')

        # Update dashboard
        self.update_dashboard()
    
    def _create_process_prompt(self, file_path: Path, content: str) -> str:
        """
        Create a prompt for Qwen Code to process the file.

        Args:
            file_path: Path to the action file
            content: File content

        Returns:
            Prompt string for Qwen Code
        """
        return f'''
You are processing an action file from the AI Employee system.

File: {file_path.name}
Content:
{content}

---

Please:
1. Analyze the content and determine what action is needed
2. Check Company_Handbook.md for rules and guidelines
3. Create a step-by-step plan in Plans/ folder
4. If action requires approval, create file in /Pending_Approval
5. If action can be auto-completed, execute and move to /Done

Remember to follow the Human-in-the-Loop pattern for sensitive actions.
'''
    
    def _create_plan_template(self, file_path: Path, content: str) -> str:
        """
        Create a plan template for Qwen Code to fill in.

        Args:
            file_path: Path to the action file
            content: File content

        Returns:
            Plan markdown content
        """
        timestamp = datetime.now().isoformat()
        
        return f'''---
created: {timestamp}
status: pending
source_file: {file_path.name}
type: action_plan
---

# Action Plan: {file_path.stem}

## Objective
*Describe the main objective here*

## Context
*Summary of the situation based on the action file*

## Steps
- [ ] Analyze the request
- [ ] Check Company_Handbook.md for applicable rules
- [ ] Determine if approval is required
- [ ] Execute action or create approval request
- [ ] Log the action
- [ ] Move to /Done when complete

## Notes
*Add any relevant notes here*

## Approval Required?
- [ ] Yes → Created file in /Pending_Approval
- [ ] No → Can proceed autonomously

---
*Generated by Orchestrator v0.1*
'''
    
    def process_approved(self) -> int:
        """
        Process all approved files (execute the approved actions).
        
        Returns:
            Number of approved files processed
        """
        files = list(self.approved.glob('*.md'))
        
        if not files:
            self.logger.info('No approved files to process')
            return 0
        
        self.logger.info(f'Found {len(files)} approved file(s) to execute')
        
        processed = 0
        for file_path in files:
            try:
                self._execute_approved_action(file_path)
                processed += 1
            except Exception as e:
                self.logger.error(f'Error executing {file_path.name}: {e}')
        
        return processed
    
    def _execute_approved_action(self, file_path: Path):
        """
        Execute an approved action.
        
        Args:
            file_path: Path to the approved file
        """
        self.logger.info(f'Executing approved action: {file_path.name}')
        
        # Read the approval file
        content = file_path.read_text()
        
        # Log the action
        self._log_action('execute_approved', str(file_path.name))
        
        # For Bronze tier: Just move to Done and log
        # In higher tiers, this would call MCP servers
        
        # Move to Done
        dest = self.done / file_path.name
        file_path.rename(dest)
        
        self.logger.info(f'Moved to Done: {dest.name}')
        
        # Update dashboard
        self.update_dashboard()
    
    def update_dashboard(self):
        """Update the Dashboard.md with current stats."""
        self.logger.debug('Updating dashboard')

        # Count files in each folder
        inbox_count = len(list((self.vault_path / 'Inbox').glob('*'))) if (self.vault_path / 'Inbox').exists() else 0
        needs_action_count = len(list(self.needs_action.glob('*.md')))
        pending_count = len(list(self.approved.glob('*.md')))
        done_today = len([f for f in self.done.glob('*.md') if self._is_today(f)])

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        iso_timestamp = datetime.now().isoformat()

        # Create fresh dashboard content
        content = f'''---
last_updated: {iso_timestamp}
status: active
---

# AI Employee Dashboard

> **Last Refresh:** {timestamp}

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| Pending Tasks | {needs_action_count} |
| Awaiting Approval | {pending_count} |
| Completed Today | {done_today} |
| Revenue MTD | $0 |

---

## 📥 Inbox Status

| Folder | Count |
|--------|-------|
| /Inbox | {inbox_count} |
| /Needs_Action | {needs_action_count} |
| /Pending_Approval | {pending_count} |

---

## ✅ Recent Activity

*Check /Done folder for completed tasks.*

---

## 📈 Business Health

### Revenue Tracking
- **Monthly Goal:** $10,000
- **Current MTD:** $0 (0%)
- **Projected:** On track

### Active Projects
1. *No active projects*

---

## 🤖 System Status

| Component | Status |
|-----------|--------|
| Gmail Watcher | ⚪ Not Running |
| File Watcher | 🟢 Running |
| Orchestrator | 🟢 Active |

---

## 📝 Quick Commands

```bash
# Start File Watcher
python watchers/filesystem_watcher.py

# Process Needs_Action folder
python watchers/orchestrator.py --process

# Process approved actions
python watchers/orchestrator.py --approved
```

---

*Generated by AI Employee v0.1 (Bronze Tier)*
'''

        self.dashboard.write_text(content, encoding='utf-8')
        self.logger.info('Dashboard updated')
    
    def _is_today(self, file_path: Path) -> bool:
        """Check if file was modified today."""
        today = datetime.now().date()
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime).date()
        return mtime == today
    
    def _log_action(self, action_type: str, target: str):
        """
        Log an action to the logs folder.
        
        Args:
            action_type: Type of action
            target: Target of the action
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'actor': 'orchestrator',
            'target': target,
            'result': 'success'
        }
        
        log_file = self.logs / f'{datetime.now().strftime("%Y-%m-%d")}.jsonl'
        
        with open(log_file, 'a') as f:
            import json
            f.write(json.dumps(log_entry) + '\n')
    
    def start_file_watcher(self, drop_folder: Optional[str] = None):
        """
        Start the filesystem watcher as a subprocess.
        
        Args:
            drop_folder: Optional path to drop folder
        """
        watchers_dir = Path(__file__).parent
        script = watchers_dir / 'filesystem_watcher.py'
        
        cmd = [sys.executable, str(script), str(self.vault_path)]
        if drop_folder:
            cmd.append(drop_folder)
        
        self.logger.info(f'Starting File Watcher: {" ".join(cmd)}')
        
        process = subprocess.Popen(cmd)
        self.watcher_processes.append(process)
        
        self.logger.info(f'File Watcher started (PID: {process.pid})')
    
    def stop_all_watchers(self):
        """Stop all watcher processes."""
        for process in self.watcher_processes:
            if process.poll() is None:  # Still running
                process.terminate()
                self.logger.info(f'Terminated watcher (PID: {process.pid})')
        
        self.watcher_processes.clear()
    
    def run_once(self):
        """Run a single processing cycle."""
        self.logger.info('Running single processing cycle')
        
        # Process approved files first
        self.process_approved()
        
        # Then process needs_action files
        self.process_needs_action()
        
        # Update dashboard
        self.update_dashboard()
        
        self.logger.info('Processing cycle complete')
    
    def run_continuous(self, interval: int = 60):
        """
        Run continuous processing cycles.
        
        Args:
            interval: Seconds between cycles
        """
        self.logger.info(f'Starting continuous mode (interval: {interval}s)')
        
        try:
            while True:
                self.run_once()
                time.sleep(interval)
        except KeyboardInterrupt:
            self.logger.info('Stopping continuous mode...')
            self.stop_all_watchers()


def main():
    """Main entry point for the orchestrator."""
    import argparse

    parser = argparse.ArgumentParser(description='AI Employee Orchestrator')
    parser.add_argument('vault_path', help='Path to the Obsidian vault')
    parser.add_argument('--scripts', help='Path to scripts folder (default: vault_parent/scripts)')
    parser.add_argument('--process', action='store_true',
                       help='Process Needs_Action folder once')
    parser.add_argument('--approved', action='store_true',
                       help='Process approved files once')
    parser.add_argument('--watchers', action='store_true',
                       help='Start all watchers')
    parser.add_argument('--dashboard', action='store_true',
                       help='Update dashboard only')
    parser.add_argument('--continuous', action='store_true',
                       help='Run in continuous mode')
    parser.add_argument('--interval', type=int, default=60,
                       help='Interval for continuous mode (seconds)')

    args = parser.parse_args()

    # Validate vault path
    vault_path = Path(args.vault_path)
    if not vault_path.exists():
        print(f'Error: Vault path does not exist: {args.vault_path}')
        sys.exit(1)

    # Initialize orchestrator with scripts path
    orchestrator = Orchestrator(str(vault_path), args.scripts)
    
    # Execute requested operations
    if args.process:
        orchestrator.process_needs_action()
    
    if args.approved:
        orchestrator.process_approved()
    
    if args.dashboard:
        orchestrator.update_dashboard()
    
    if args.watchers:
        orchestrator.start_file_watcher()
    
    if args.continuous:
        orchestrator.run_continuous(args.interval)
    
    # If no specific action requested, show help
    if not any([args.process, args.approved, args.watchers, args.dashboard, args.continuous]):
        parser.print_help()


if __name__ == '__main__':
    main()
