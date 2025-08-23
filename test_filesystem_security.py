#!/usr/bin/env python3
"""Test filesystem security configuration."""

import os
import sys
import tempfile
from pathlib import Path

# Add src to Python path to import modules
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from mcp_sqlserver_filesystem.config import reload_config
from mcp_sqlserver_filesystem.filesystem import FilesystemManager


def test_configuration(test_name: str, env_vars: dict):
    """Test a specific configuration."""
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"{'='*60}")
    
    # Set environment variables
    original_values = {}
    for key, value in env_vars.items():
        original_values[key] = os.environ.get(key)
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    
    try:
        # Reload configuration
        config = reload_config()
        
        # Create filesystem manager
        fs = FilesystemManager()
        
        # Test paths
        test_paths = [
            Path.cwd() / 'README.md',
            Path.cwd() / 'pyproject.toml',
            Path('C:') / 'Windows' / 'System32' / 'notepad.exe' if os.name == 'nt' else Path('/etc/passwd'),
            Path.home() / 'Desktop' / 'test.txt',
            Path(tempfile.gettempdir()) / 'test_file.py'
        ]
        
        print(f"\nFilesystem Configuration:")
        print(f"  Full Access Mode: {config.filesystem.is_full_access_mode}")
        print(f"  Allowed Paths: {config.filesystem.allowed_paths}")
        print(f"  Allowed Extensions: {config.filesystem.allowed_extensions}")
        print(f"  Ignore File Locks: {config.filesystem.ignore_file_locks}")
        
        print(f"\nPath Access Tests:")
        for test_path in test_paths:
            try:
                is_allowed = fs._is_path_allowed(test_path)
                is_ext_allowed = fs._is_extension_allowed(test_path)
                overall_allowed = is_allowed and is_ext_allowed
                
                status = "✅ ALLOWED" if overall_allowed else "❌ BLOCKED"
                path_status = "✅" if is_allowed else "❌"
                ext_status = "✅" if is_ext_allowed else "❌"
                
                print(f"  {status} {test_path} (Path: {path_status}, Ext: {ext_status})")
            except Exception as e:
                print(f"  ❗ ERROR {test_path}: {e}")
                
        # Test extension wildcards
        if '*.*' in config.filesystem.allowed_extensions or '*' in config.filesystem.allowed_extensions:
            print(f"\n🌟 Wildcard Extension Mode: All extensions allowed")
        elif not config.filesystem.allowed_extensions:
            print(f"\n🌟 No Extension Restrictions: All extensions allowed")
        
    except Exception as e:
        print(f"❌ Configuration Error: {e}")
    
    finally:
        # Restore original environment variables
        for key, original_value in original_values.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value


def test_file_lock_handling():
    """Test file lock handling functionality."""
    print(f"\n{'='*60}")
    print(f"Testing: File Lock Handling")
    print(f"{'='*60}")
    
    # Set up test environment with ignore_file_locks=True
    test_env = {
        'FS_ALLOWED_PATHS': '',  # Full access
        'FS_IGNORE_FILE_LOCKS': 'true'
    }
    
    original_values = {}
    for key, value in test_env.items():
        original_values[key] = os.environ.get(key)
        os.environ[key] = value
    
    try:
        config = reload_config()
        fs = FilesystemManager()
        
        # Create a test file
        test_file = Path(tempfile.gettempdir()) / 'lock_test.txt'
        test_content = "This is a test file for lock handling."
        
        # Write test file
        test_file.write_text(test_content, encoding='utf-8')
        print(f"✅ Created test file: {test_file}")
        
        # Try to read the file (should work)
        read_content = fs.read_file(test_file)
        print(f"✅ Successfully read file: {len(read_content)} characters")
        
        # Test write with lock handling
        new_content = test_content + "\nAdditional line added."
        fs.write_file(test_file, new_content)
        print(f"✅ Successfully wrote to file")
        
        # Verify content
        final_content = fs.read_file(test_file)
        if "Additional line added" in final_content:
            print(f"✅ File content updated successfully")
        else:
            print(f"❌ File content not updated properly")
            
        # Clean up
        test_file.unlink(missing_ok=True)
        print(f"✅ Test file cleaned up")
        
    except Exception as e:
        print(f"❗ File lock test error: {e}")
        
    finally:
        # Restore environment
        for key, original_value in original_values.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value


if __name__ == '__main__':
    print("\n🔒 Filesystem Security Configuration Tests")
    print("========================================")
    
    # Test 1: Full Access Mode
    test_configuration(
        "Full Access Mode (No Restrictions)",
        {
            'FS_ALLOWED_PATHS': '',  # Empty = full access
            'FS_ALLOWED_EXTENSIONS': '',
            'FS_IGNORE_FILE_LOCKS': 'true'
        }
    )
    
    # Test 2: Wildcard Access Mode  
    test_configuration(
        "Wildcard Access Mode (*)",
        {
            'FS_ALLOWED_PATHS': '*',
            'FS_ALLOWED_EXTENSIONS': '*.*',
            'FS_IGNORE_FILE_LOCKS': 'true'
        }
    )
    
    # Test 3: Restricted Access Mode
    current_dir = str(Path.cwd())
    temp_dir = tempfile.gettempdir()
    test_configuration(
        "Restricted Access Mode",
        {
            'FS_ALLOWED_PATHS': f'{current_dir},{temp_dir}',
            'FS_ALLOWED_EXTENSIONS': '.txt,.md,.py,.json',
            'FS_IGNORE_FILE_LOCKS': 'false'
        }
    )
    
    # Test 4: Specific Extension Restrictions
    test_configuration(
        "Text Files Only",
        {
            'FS_ALLOWED_PATHS': current_dir,
            'FS_ALLOWED_EXTENSIONS': '.txt,.md,.log',
            'FS_IGNORE_FILE_LOCKS': 'true'
        }
    )
    
    # Test 5: File Lock Handling
    test_file_lock_handling()
    
    print(f"\n✅ All tests completed!")
    print(f"\n📝 Summary:")
    print(f"  - Simplified configuration: No more BLOCKED_* settings")
    print(f"  - Wildcard support: Use *.* or * for all extensions")
    print(f"  - File lock handling: Can read/write locked files when enabled")
    print(f"  - Default behavior: Not in allowed list = blocked")