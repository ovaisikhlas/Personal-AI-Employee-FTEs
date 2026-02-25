"""
Bronze Tier Verification Script

Run this script to verify all Bronze Tier requirements are met.
"""

import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def check_file(path: Path, description: str) -> bool:
    """Check if a file exists."""
    exists = path.exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {path}")
    return exists


def check_folder(path: Path, description: str) -> bool:
    """Check if a folder exists and list contents."""
    exists = path.exists() and path.is_dir()
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {path}")
    if exists:
        items = list(path.iterdir())
        print(f"      Contents: {len(items)} items")
    return exists


def check_import(module: str, name: str) -> bool:
    """Check if a module can be imported."""
    try:
        __import__(module)
        print(f"  ✓ Python import: {name}")
        return True
    except ImportError as e:
        print(f"  ✗ Python import: {name} - {e}")
        return False


def main():
    print("=" * 60)
    print("BRONZE TIER VERIFICATION")
    print("=" * 60)
    
    # Get vault path from command line or use default
    if len(sys.argv) > 1:
        vault_path = Path(sys.argv[1])
    else:
        vault_path = Path(__file__).parent.parent / "AI_Employee_Vault"
    
    watchers_path = Path(__file__).parent.parent / "watchers"
    
    all_passed = True
    
    print("\n📁 VAULT STRUCTURE")
    print("-" * 40)
    
    # Check required folders
    required_folders = [
        ("Inbox", "Inbox folder"),
        ("Needs_Action", "Needs_Action folder"),
        ("Done", "Done folder"),
        ("Pending_Approval", "Pending Approval folder"),
        ("Approved", "Approved folder"),
        ("Plans", "Plans folder"),
        ("Logs", "Logs folder"),
    ]
    
    for folder, description in required_folders:
        if not check_folder(vault_path / folder, description):
            all_passed = False
    
    print("\n📄 KEY FILES (in scripts folder)")
    print("-" * 40)
    
    # Check required files in scripts folder
    scripts_path = vault_path.parent / "scripts"
    required_files = [
        ("Dashboard.md", "Dashboard"),
        ("Company_Handbook.md", "Company Handbook"),
        ("Business_Goals.md", "Business Goals"),
    ]
    
    for filename, description in required_files:
        if not check_file(scripts_path / filename, description):
            all_passed = False
    
    print("\n🐍 WATCHER SCRIPTS")
    print("-" * 40)
    
    # Check watcher scripts
    watcher_scripts = [
        ("base_watcher", "BaseWatcher class"),
        ("filesystem_watcher", "FilesystemWatcher"),
        ("orchestrator", "Orchestrator"),
    ]
    
    sys.path.insert(0, str(watchers_path))
    
    for module, description in watcher_scripts:
        if not check_import(module, description):
            all_passed = False
    
    print("\n📊 FUNCTIONAL TESTS")
    print("-" * 40)
    
    # Check if watcher can run
    try:
        from filesystem_watcher import FilesystemWatcher
        print(f"  ✓ FilesystemWatcher can be instantiated")
    except Exception as e:
        print(f"  ✗ FilesystemWatcher error: {e}")
        all_passed = False
    
    # Check if orchestrator can run
    try:
        from orchestrator import Orchestrator
        orch = Orchestrator(str(vault_path))
        print(f"  ✓ Orchestrator can be instantiated")
    except Exception as e:
        print(f"  ✗ Orchestrator error: {e}")
        all_passed = False
    
    # Check file counts
    needs_action_count = len(list((vault_path / "Needs_Action").glob("*.md")))
    plans_count = len(list((vault_path / "Plans").glob("*.md")))
    
    print(f"\n📈 CURRENT STATE")
    print("-" * 40)
    print(f"  Files in Needs_Action: {needs_action_count}")
    print(f"  Plans created: {plans_count}")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ BRONZE TIER VERIFICATION PASSED")
        print("\nYour AI Employee Bronze Tier is ready!")
        print("\nNext steps:")
        print("1. Start the File Watcher:")
        print(f"   python watchers/filesystem_watcher.py \"{vault_path}\"")
        print("\n2. Drop a file in Inbox/Drop to test")
        print("\n3. Process files with:")
        print(f"   python watchers/orchestrator.py \"{vault_path}\" --process")
    else:
        print("❌ BRONZE TIER VERIFICATION FAILED")
        print("\nPlease fix the issues above and try again.")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
