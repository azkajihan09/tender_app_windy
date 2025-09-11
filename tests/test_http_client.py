"""Tests for http_client module."""

import pytest
import httpx
from unittest.mock import Mock, patch, AsyncMock

from src.securekit.http_client import HttpxTransport, MockTransport, ApiClient


class TestMockTransport:
    """Tests for MockTransport - ensuring no real network calls."""
    
    def test_mock_transport_sync_request(self):
        """Test MockTransport sync request."""
        transport = MockTransport()
        
        response = transport.request("GET", "/test")
        
        assert response.status_code == 200
        assert response.json() == {"mock": True, "method": "GET", "url": "/test"}
        assert len(transport.call_log) == 1
        assert transport.call_log[0] == ("GET", "/test", {})
    
    @pytest.mark.asyncio
    async def test_mock_transport_async_request(self):
        """Test MockTransport async request."""
        transport = MockTransport()
        
        response = await transport.arequest("POST", "/api/data", json={"test": True})
        
        assert response.status_code == 200
        assert response.json() == {"mock": True, "method": "POST", "url": "/api/data"}
        assert len(transport.call_log) == 1
        assert transport.call_log[0] == ("POST", "/api/data", {"json": {"test": True}})
    
    def test_mock_transport_with_custom_responses(self):
        """Test MockTransport with predefined responses."""
        custom_response = httpx.Response(
            status_code=201,
            json={"created": True},
            request=httpx.Request("POST", "/users"),
        )
        
        transport = MockTransport(responses={"POST /users": custom_response})
        
        response = transport.request("POST", "/users")
        
        assert response.status_code == 201
        assert response.json() == {"created": True}
    
    def test_mock_transport_no_network_access(self):
        """Verify MockTransport doesn't make real network calls."""
        transport = MockTransport()
        
        # This should not make a real network call
        response = transport.request("GET", "https://httpbin.org/get")
        
        assert response.status_code == 200
        assert response.json() == {"mock": True, "method": "GET", "url": "https://httpbin.org/get"}


class TestHttpxTransport:
    """Tests for HttpxTransport with mocked httpx clients."""
    
    @patch('httpx.Client')
    def test_httpx_transport_sync_request(self, mock_client_class):
        """Test HttpxTransport sync request."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        mock_response = Mock()
        mock_client.request.return_value = mock_response
        
        transport = HttpxTransport(base_url="https://api.example.com", timeout=5.0)
        
        result = transport.request("GET", "/test")
        
        assert result == mock_response
        mock_client.request.assert_called_once_with("GET", "/test")
        mock_client_class.assert_called_once_with(
            base_url="https://api.example.com",
            timeout=5.0,
            verify=True,
        )
    
    @patch('httpx.AsyncClient')
    @pytest.mark.asyncio
    async def test_httpx_transport_async_request(self, mock_async_client_class):
        """Test HttpxTransport async request."""
        mock_async_client = AsyncMock()
        mock_async_client_class.return_value = mock_async_client
        
        mock_response = Mock()
        mock_async_client.request.return_value = mock_response
        
        transport = HttpxTransport(base_url="https://api.example.com", timeout=5.0)
        
        result = await transport.arequest("POST", "/data", json={"test": True})
        
        assert result == mock_response
        mock_async_client.request.assert_called_once_with("POST", "/data", json={"test": True})
    
    @patch('httpx.Client')
    def test_httpx_transport_close(self, mock_client_class):
        """Test HttpxTransport close method."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        transport = HttpxTransport()
        transport.close()
        
        mock_client.close.assert_called_once()
    
    @patch('httpx.AsyncClient')
    @pytest.mark.asyncio
    async def test_httpx_transport_aclose(self, mock_async_client_class):
        """Test HttpxTransport aclose method."""
        mock_async_client = AsyncMock()
        mock_async_client_class.return_value = mock_async_client
        
        transport = HttpxTransport()
        await transport.aclose()
        
        mock_async_client.aclose.assert_called_once()


class TestApiClient:
    """Tests for ApiClient with retry logic."""
    
    def test_api_client_get_success(self):
        """Test ApiClient GET request success."""
        transport = MockTransport()
        client = ApiClient(transport, max_retries=2)
        
        response = client.get("/users")
        
        assert response.status_code == 200
        assert len(transport.call_log) == 1
        assert transport.call_log[0][0] == "GET"
        assert transport.call_log[0][1] == "/users"
    
    def test_api_client_post_success(self):
        """Test ApiClient POST request success."""
        transport = MockTransport()
        client = ApiClient(transport, max_retries=2)
        
        response = client.post("/users", json={"name": "John"})
        
        assert response.status_code == 200
        assert len(transport.call_log) == 1
        assert transport.call_log[0] == ("POST", "/users", {"json": {"name": "John"}})
    
    @pytest.mark.asyncio
    async def test_api_client_aget_success(self):
        """Test ApiClient async GET request success."""
        transport = MockTransport()
        client = ApiClient(transport, max_retries=2)
        
        response = await client.aget("/users")
        
        assert response.status_code == 200
        assert len(transport.call_log) == 1
        assert transport.call_log[0][0] == "GET"
        assert transport.call_log[0][1] == "/users"
    
    @pytest.mark.asyncio
    async def test_api_client_apost_success(self):
        """Test ApiClient async POST request success."""
        transport = MockTransport()
        client = ApiClient(transport, max_retries=2)
        
        response = await client.apost("/users", json={"name": "Jane"})
        
        assert response.status_code == 200
        assert len(transport.call_log) == 1
        assert transport.call_log[0] == ("POST", "/users", {"json": {"name": "Jane"}})
    
    def test_api_client_retry_on_server_error(self):
        """Test ApiClient retries on server errors."""
        # Create responses that simulate server errors then success
        server_error = httpx.Response(
            status_code=500,
            request=httpx.Request("GET", "/api"),
        )
        success_response = httpx.Response(
            status_code=200,
            json={"success": True},
            request=httpx.Request("GET", "/api"),
        )
        
        transport = MockTransport()
        client = ApiClient(transport, max_retries=2)
        
        # Mock transport to return server error first, then success
        original_request = transport.request
        call_count = 0
        
        def mock_request(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return server_error
            return success_response
        
        transport.request = mock_request
        
        response = client.get("/api")
        
        assert response.status_code == 200
        assert call_count == 2  # One retry
    
    def test_api_client_no_retry_on_client_error(self):
        """Test ApiClient doesn't retry on client errors."""
        client_error = httpx.Response(
            status_code=404,
            request=httpx.Request("GET", "/api"),
        )
        
        transport = MockTransport(responses={"GET /api": client_error})
        client = ApiClient(transport, max_retries=2)
        
        response = client.get("/api")
        
        assert response.status_code == 404
        assert len(transport.call_log) == 1  # No retries
    
    def test_api_client_retry_exhaustion(self):
        """Test ApiClient exhausts retries and returns last response."""
        server_error = httpx.Response(
            status_code=503,
            request=httpx.Request("GET", "/api"),
        )
        
        transport = MockTransport(responses={"GET /api": server_error})
        client = ApiClient(transport, max_retries=2)
        
        response = client.get("/api")
        
        assert response.status_code == 503
        assert len(transport.call_log) == 3  # Original + 2 retries
    
    @patch('asyncio.sleep')
    @pytest.mark.asyncio
    async def test_api_client_async_retry_with_backoff(self, mock_sleep):
        """Test ApiClient async retry with exponential backoff."""
        server_error = httpx.Response(
            status_code=500,
            request=httpx.Request("GET", "/api"),
        )
        success_response = httpx.Response(
            status_code=200,
            json={"success": True},
            request=httpx.Request("GET", "/api"),
        )
        
        transport = MockTransport()
        client = ApiClient(transport, max_retries=2)
        
        # Mock transport to return server error first, then success
        call_count = 0
        
        async def mock_arequest(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return server_error
            return success_response
        
        transport.arequest = mock_arequest
        
        response = await client.aget("/api")
        
        assert response.status_code == 200
        assert call_count == 2
        mock_sleep.assert_called_once_with(0.1)  # First backoff


class TestNoNetworkAccess:
    """Integration tests to ensure no real network access during testing."""
    
    def test_mock_transport_prevents_network_calls(self):
        """Verify that using MockTransport prevents any real network calls."""
        transport = MockTransport()
        client = ApiClient(transport)
        
        # This would fail if real network calls were made
        response = client.get("https://this-domain-definitely-does-not-exist.invalid/test")
        
        assert response.status_code == 200
        assert "mock" in response.json()
    
    @pytest.mark.asyncio
    async def test_async_mock_transport_prevents_network_calls(self):
        """Verify that async MockTransport prevents any real network calls."""
        transport = MockTransport()
        client = ApiClient(transport)
        
        # This would fail if real network calls were made
        response = await client.aget("https://this-domain-definitely-does-not-exist.invalid/test")
        
        assert response.status_code == 200
        assert "mock" in response.json()