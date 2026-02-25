"""
AI Employee Watchers Package

This package contains all watcher implementations and the orchestrator.
"""

from .base_watcher import BaseWatcher
from .filesystem_watcher import FilesystemWatcher
from .orchestrator import Orchestrator

__all__ = ['BaseWatcher', 'FilesystemWatcher', 'Orchestrator']
__version__ = '0.1.0'
