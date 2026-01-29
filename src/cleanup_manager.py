"""
Cleanup Manager Module
Manages temporary file cleanup
"""

import os
from pathlib import Path
from typing import List, Tuple
from contextlib import contextmanager


class CleanupManager:
    """Manages cleanup of temporary files"""
    
    def __init__(self):
        self.temp_files = []
    
    def register_file(self, filepath: str):
        """
        Register a file for cleanup
        
        Args:
            filepath: Path to file that should be cleaned up
        """
        if filepath and filepath not in self.temp_files:
            self.temp_files.append(filepath)
    
    def register_files(self, filepaths: List[str]):
        """
        Register multiple files for cleanup
        
        Args:
            filepaths: List of file paths to clean up
        """
        for filepath in filepaths:
            self.register_file(filepath)
    
    def cleanup(self) -> Tuple[int, int]:
        """
        Delete all registered temporary files
        
        Returns:
            Tuple of (successful_deletions, failed_deletions)
        """
        successful = 0
        failed = 0
        
        for filepath in self.temp_files:
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                    print(f"✓ Cleaned up: {filepath}")
                    successful += 1
            except Exception as e:
                print(f"✗ Failed to delete {filepath}: {e}")
                failed += 1
        
        # Clear the list after cleanup
        self.temp_files.clear()
        
        return successful, failed
    
    def cleanup_directory(self, directory: Path, pattern: str = "*"):
        """
        Clean up files in a directory matching a pattern
        
        Args:
            directory: Directory to clean
            pattern: Glob pattern for files to delete (default: all files)
        """
        if not directory.exists():
            return
        
        for file in directory.glob(pattern):
            if file.is_file():
                self.register_file(str(file))


@contextmanager
def auto_cleanup():
    """
    Context manager for automatic cleanup
    
    Usage:
        with auto_cleanup() as manager:
            manager.register_file("temp.wav")
            # ... do work ...
        # Files are automatically cleaned up when exiting context
    """
    manager = CleanupManager()
    try:
        yield manager
    finally:
        success, failed = manager.cleanup()
        if success > 0:
            print(f"\n🗑️  Cleanup complete: {success} file(s) deleted")
        if failed > 0:
            print(f"⚠️  Warning: {failed} file(s) could not be deleted")
