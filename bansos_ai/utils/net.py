"""
Modul Net Utility untuk Pengelolaan HTTP Client Asinkron.
"""

import httpx
from typing import Dict, Optional
from bansos_ai.config import DEFAULT_TIMEOUT, DEFAULT_USER_AGENT

def get_async_client(timeout: float = 3.0, headers: Optional[Dict[str, str]] = None) -> httpx.AsyncClient:
    """Mengembalikan instance httpx.AsyncClient berperforma tinggi untuk M4 Pro Multi-Threading."""
    default_headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "application/json, text/html, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,id;q=0.6",
    }
    if headers:
        default_headers.update(headers)
        
    return httpx.AsyncClient(
        headers=default_headers,
        timeout=httpx.Timeout(timeout, connect=2.0),
        limits=httpx.Limits(max_connections=200, max_keepalive_connections=50),
        follow_redirects=True,
        verify=False
    )

