"""HTTP client with secure patterns and dependency injection for testing."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Protocol, runtime_checkable

import httpx


@runtime_checkable
class HttpTransport(Protocol):
    """Protocol for HTTP transport (sync or async)."""

    def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Sync HTTP request."""
        ...

    async def arequest(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Async HTTP request."""
        ...


class HttpxTransport:
    """Real HTTP transport using httpx."""

    def __init__(self, base_url: str = "", timeout: float = 10.0, verify: bool = True):
        self.base_url = base_url
        self.sync_client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            verify=verify,
        )
        self.async_client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            verify=verify,
        )

    def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Sync HTTP request."""
        return self.sync_client.request(method, url, **kwargs)

    async def arequest(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Async HTTP request."""
        return await self.async_client.request(method, url, **kwargs)

    def close(self) -> None:
        """Close sync client."""
        self.sync_client.close()

    async def aclose(self) -> None:
        """Close async client."""
        await self.async_client.aclose()


class MockTransport:
    """Mock HTTP transport for testing - does not make real network calls."""

    def __init__(self, responses: Dict[str, httpx.Response] | None = None):
        self.responses = responses or {}
        self.call_log: list[tuple[str, str, Dict[str, Any]]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Mock sync HTTP request."""
        self.call_log.append((method, url, kwargs))
        key = f"{method.upper()} {url}"
        if key in self.responses:
            return self.responses[key]
        # Default mock response
        return httpx.Response(
            status_code=200,
            json={"mock": True, "method": method, "url": url},
            request=httpx.Request(method, url),
        )

    async def arequest(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Mock async HTTP request."""
        return self.request(method, url, **kwargs)


class ApiClient:
    """HTTP API client with retry logic and secure defaults."""

    def __init__(self, transport: HttpTransport, max_retries: int = 3):
        self.transport = transport
        self.max_retries = max_retries

    def get(self, path: str, **kwargs: Any) -> httpx.Response:
        """GET request with retry logic."""
        return self._request_with_retry("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> httpx.Response:
        """POST request with retry logic."""
        return self._request_with_retry("POST", path, **kwargs)

    async def aget(self, path: str, **kwargs: Any) -> httpx.Response:
        """Async GET request with retry logic."""
        return await self._arequest_with_retry("GET", path, **kwargs)

    async def apost(self, path: str, **kwargs: Any) -> httpx.Response:
        """Async POST request with retry logic."""
        return await self._arequest_with_retry("POST", path, **kwargs)

    def _request_with_retry(
        self, method: str, path: str, **kwargs: Any
    ) -> httpx.Response:
        """Execute sync request with retry logic."""
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.transport.request(method, path, **kwargs)
                if response.status_code < 500:  # Don't retry client errors
                    return response
                if attempt == self.max_retries:
                    return response
            except (httpx.RequestError, httpx.TimeoutException) as e:
                last_exception = e
                if attempt == self.max_retries:
                    raise

        if last_exception:
            raise last_exception

        # This should never be reached
        raise RuntimeError("Unexpected retry logic error")

    async def _arequest_with_retry(
        self, method: str, path: str, **kwargs: Any
    ) -> httpx.Response:
        """Execute async request with retry logic."""
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.transport.arequest(method, path, **kwargs)
                if response.status_code < 500:  # Don't retry client errors
                    return response
                if attempt == self.max_retries:
                    return response
                await asyncio.sleep(0.1 * (2**attempt))  # Exponential backoff
            except (httpx.RequestError, httpx.TimeoutException) as e:
                last_exception = e
                if attempt == self.max_retries:
                    raise
                await asyncio.sleep(0.1 * (2**attempt))

        if last_exception:
            raise last_exception

        # This should never be reached
        raise RuntimeError("Unexpected retry logic error")
