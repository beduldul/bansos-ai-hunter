"""
Modul Net Utility untuk Pengelolaan HTTP Client Asinkron.
"""

import httpx
from typing import Dict, Optional
from bansos_ai.config import DEFAULT_TIMEOUT, DEFAULT_USER_AGENT

def get_async_client(timeout: float = DEFAULT_TIMEOUT, headers: Optional[Dict[str, str]] = None) -> httpx.AsyncClient:
    """Mengembalikan instance httpx.AsyncClient terkonfigurasi."""
    default_headers = {
        "User-Agent": DEFAULT_USER_AGENT,
        "Accept": "application/json, text/html, */*",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,id;q=0.6",
    }
    if headers:
        default_headers.update(headers)
        
    return httpx.AsyncClient(
        headers=default_headers,
        timeout=httpx.Timeout(timeout),
        follow_redirects=True,
        verify=False  # Mengizinkan pengetesan self-signed cert jika ada relay khusus
    )
