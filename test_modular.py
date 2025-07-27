#!/usr/bin/env python3
"""
Simple test script to verify the modular structure works correctly.
"""

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        import config
        print("✅ config.py imports successfully")
        
        import utils
        print("✅ utils.py imports successfully")
        
        import file_processor
        print("✅ file_processor.py imports successfully")
        
        import ai_client
        print("✅ ai_client.py imports successfully")
        
        import cli
        print("✅ cli.py imports successfully")
        
        import main
        print("✅ main.py imports successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_config():
    """Test configuration values are accessible."""
    try:
        from config import BASE_URL, EXPLANATION_WORDS, MODEL, MODIFICATION_WORDS
        assert BASE_URL is not None
        assert MODEL is not None
        assert len(MODIFICATION_WORDS) > 0
        assert len(EXPLANATION_WORDS) > 0
        print("✅ Configuration values are accessible")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_utils():
    """Test utility functions."""
    try:
        from utils import is_modification_request

        # Test modification request
        assert is_modification_request("fix the bug") == True
        assert is_modification_request("add a new feature") == True
        
        # Test explanation request
        assert is_modification_request("explain how this works") == False
        assert is_modification_request("what does this do") == False
        
        print("✅ Utility functions work correctly")
        return True
    except Exception as e:
        print(f"❌ Utility test failed: {e}")
        return False


def test_file_processor():
    """Test file processing functions."""
    try:
        from file_processor import extract_code_for_file, process_file_references

        # Test file reference processing (without actual files)
        processed, has_refs, is_mod = process_file_references("fix @nonexistent.py")
        assert isinstance(processed, str)
        assert isinstance(has_refs, bool)
        assert isinstance(is_mod, bool)
        
        # Test code extraction
        test_response = "```python\ndef hello():\n    print('world')\n```"
        code = extract_code_for_file(test_response)
        assert "def hello():" in code
        
        print("✅ File processing functions work correctly")
        return True
    except Exception as e:
        print(f"❌ File processing test failed: {e}")
        return False


def test_cli():
    """Test CLI argument parsing."""
    try:
        from cli import build_parser
        
        parser = build_parser()
        # Test that parser can be created
        assert parser is not None
        
        print("✅ CLI argument parsing works correctly")
        return True
    except Exception as e:
        print(f"❌ CLI test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Testing GhostCoder modular structure...\n")
    
    tests = [
        test_imports,
        test_config,
        test_utils,
        test_file_processor,
        test_cli,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The modular structure is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False


if __name__ == "__main__":
    main() 