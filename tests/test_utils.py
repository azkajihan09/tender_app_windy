"""Tests for utils module."""

import os
import subprocess
import pytest
from unittest.mock import patch, MagicMock

from src.securekit.utils import temp_env, validate_args, run_command, sanitize_filename, secure_compare


class TestTempEnv:
    """Tests for temp_env context manager."""
    
    def test_temp_env_sets_and_restores_new_var(self):
        """Test that temp_env sets new environment variable and restores."""
        test_key = "TEST_TEMP_ENV_NEW"
        test_value = "test_value"
        
        # Ensure the key doesn't exist initially
        os.environ.pop(test_key, None)
        assert test_key not in os.environ
        
        with temp_env(**{test_key: test_value}):
            assert os.environ[test_key] == test_value
        
        assert test_key not in os.environ
    
    def test_temp_env_sets_and_restores_existing_var(self):
        """Test that temp_env sets existing environment variable and restores."""
        test_key = "TEST_TEMP_ENV_EXISTING"
        original_value = "original"
        temp_value = "temporary"
        
        os.environ[test_key] = original_value
        
        with temp_env(**{test_key: temp_value}):
            assert os.environ[test_key] == temp_value
        
        assert os.environ[test_key] == original_value
        
        # Clean up
        os.environ.pop(test_key, None)
    
    def test_temp_env_with_exception(self):
        """Test that temp_env restores environment even when exception occurs."""
        test_key = "TEST_TEMP_ENV_EXCEPTION"
        original_value = "original"
        temp_value = "temporary"
        
        os.environ[test_key] = original_value
        
        with pytest.raises(ValueError):
            with temp_env(**{test_key: temp_value}):
                assert os.environ[test_key] == temp_value
                raise ValueError("Test exception")
        
        assert os.environ[test_key] == original_value
        
        # Clean up
        os.environ.pop(test_key, None)


class TestValidateArgs:
    """Tests for validate_args decorator."""
    
    def test_validate_args_valid_input(self):
        """Test validate_args with valid input."""
        def is_positive(x):
            return x > 0
        
        @validate_args(is_positive)
        def add_one(x):
            return x + 1
        
        result = add_one(5)
        assert result == 6
    
    def test_validate_args_invalid_input(self):
        """Test validate_args with invalid input."""
        def is_positive(x):
            return x > 0
        
        @validate_args(is_positive)
        def add_one(x):
            return x + 1
        
        with pytest.raises(ValueError, match="Invalid arguments"):
            add_one(-5)
    
    def test_validate_args_with_kwargs(self):
        """Test validate_args with keyword arguments."""
        def validate_user(name=None, age=None):
            return name and len(name) > 0 and age and age >= 0
        
        @validate_args(validate_user)
        def create_user(name, age):
            return f"User: {name}, Age: {age}"
        
        result = create_user(name="John", age=25)
        assert result == "User: John, Age: 25"
        
        with pytest.raises(ValueError, match="Invalid arguments"):
            create_user(name="", age=25)


class TestRunCommand:
    """Tests for run_command function."""
    
    @patch('subprocess.run')
    def test_run_command_success(self, mock_run):
        """Test run_command with successful execution."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Hello, World!",
            stderr=""
        )
        
        returncode, stdout, stderr = run_command(["echo", "Hello, World!"])
        
        assert returncode == 0
        assert stdout == "Hello, World!"
        assert stderr == ""
        
        mock_run.assert_called_once_with(
            ["echo", "Hello, World!"],
            capture_output=True,
            text=True,
            timeout=10,
            shell=False,
        )
    
    @patch('subprocess.run')
    def test_run_command_with_timeout(self, mock_run):
        """Test run_command with custom timeout."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="output",
            stderr=""
        )
        
        run_command(["test"], timeout=30)
        
        mock_run.assert_called_once_with(
            ["test"],
            capture_output=True,
            text=True,
            timeout=30,
            shell=False,
        )
    
    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run):
        """Test run_command with command failure."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Command failed"
        )
        
        returncode, stdout, stderr = run_command(["false"])
        
        assert returncode == 1
        assert stdout == ""
        assert stderr == "Command failed"


class TestSanitizeFilename:
    """Tests for sanitize_filename function."""
    
    def test_sanitize_filename_normal(self):
        """Test sanitize_filename with normal filename."""
        result = sanitize_filename("normal_file.txt")
        assert result == "normal_file.txt"
    
    def test_sanitize_filename_dangerous_chars(self):
        """Test sanitize_filename with dangerous characters."""
        result = sanitize_filename("../../../etc/passwd")
        assert result == "______etc_passwd"
    
    def test_sanitize_filename_windows_dangerous(self):
        """Test sanitize_filename with Windows dangerous characters."""
        result = sanitize_filename('file<>:"/\\|?*.txt')
        assert result == "file_________.txt"
    
    def test_sanitize_filename_empty(self):
        """Test sanitize_filename with empty string."""
        result = sanitize_filename("")
        assert result == "unnamed"
    
    def test_sanitize_filename_only_dots(self):
        """Test sanitize_filename with only dots."""
        result = sanitize_filename("...")
        assert result == "unnamed"
    
    def test_sanitize_filename_leading_trailing_whitespace(self):
        """Test sanitize_filename removes leading/trailing whitespace and dots."""
        result = sanitize_filename("  .file.txt.  ")
        assert result == "file.txt"


class TestSecureCompare:
    """Tests for secure_compare function."""
    
    def test_secure_compare_equal_strings(self):
        """Test secure_compare with equal strings."""
        assert secure_compare("secret123", "secret123") is True
    
    def test_secure_compare_different_strings(self):
        """Test secure_compare with different strings."""
        assert secure_compare("secret123", "secret456") is False
    
    def test_secure_compare_empty_strings(self):
        """Test secure_compare with empty strings."""
        assert secure_compare("", "") is True
    
    def test_secure_compare_different_lengths(self):
        """Test secure_compare with strings of different lengths."""
        assert secure_compare("short", "longer_string") is False