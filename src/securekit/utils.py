"""Utility helpers with secure coding patterns."""

from __future__ import annotations

import os
import subprocess
from contextlib import contextmanager
from typing import Callable, Any, Dict, Optional
from functools import wraps


@contextmanager
def temp_env(**kwargs: object):
    """
    Temporarily set environment variables inside context block.
    Restores previous values on exit.
    """
    saved: Dict[str, Optional[str]] = {k: os.environ.get(k) for k in kwargs}
    try:
        os.environ.update({k: str(v) for k, v in kwargs.items()})
        yield
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def validate_args(validator: Callable[..., bool]) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator factory to validate arguments before running function.
    Validator should return True for valid args or False otherwise.
    """

    def deco(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> Any:
            if not validator(*args, **kwargs):
                raise ValueError("Invalid arguments")
            return func(*args, **kwargs)

        return wrapper

    return deco


def run_command(args: list[str], timeout: int = 10) -> tuple[int, str, str]:
    """
    Run a subprocess safely by requiring args (list) and avoiding shell=True.
    Returns (returncode, stdout, stderr).
    """
    # Note: do not pass user input directly into args without validation.
    proc = subprocess.run(
        args,
        capture_output=True,
        text=True,
        timeout=timeout,
        shell=False,  # Explicitly avoid shell=True for security
    )
    return proc.returncode, proc.stdout, proc.stderr


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing dangerous characters.
    Useful for preventing path traversal attacks.
    """
    import re
    # Remove path separators and other dangerous chars
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing dots and spaces
    sanitized = sanitized.strip('. ')
    # Prevent empty filename
    if not sanitized:
        sanitized = "unnamed"
    return sanitized


def secure_compare(a: str, b: str) -> bool:
    """
    Time-constant string comparison to prevent timing attacks.
    """
    import hmac
    return hmac.compare_digest(a, b)