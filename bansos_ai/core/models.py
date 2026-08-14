"""
Definisi Data Model Menggunakan Pydantic untuk Penanganan Target dan Hasil Validasi.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class RelayTarget(BaseModel):
    """Model data untuk endpoint atau sumber AI Relay yang ditemukan."""
    url: str
    base_url: str
    api_key: Optional[str] = None
    source: str = "Search Engine"
    title: Optional[str] = None
    snippet: Optional[str] = None
    matched_keyword: Optional[str] = None
    extracted_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class ValidationResult(BaseModel):
    """Model data hasil uji konektivitas dan kapabilitas AI Relay."""
    target: RelayTarget
    is_valid: bool = False
    is_agent_working: bool = False  # Uji tes agen / kelayakan penyelesaian pesan
    status_code: int = 0
    status_message: str = "Unchecked"
    latency_ms: float = 0.0
    supported_models: List[str] = Field(default_factory=list)
    available_quota: Optional[str] = None
    is_one_api_format: bool = False
    tested_at: str = Field(default_factory=lambda: datetime.now().isoformat())

class ScanSummary(BaseModel):
    """Ringkasan akhir proses pemindaian dan pengujian."""
    scan_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    total_found: int = 0
    total_valid: int = 0
    total_agent_ready: int = 0
    duration_seconds: float = 0.0
    valid_endpoints: List[ValidationResult] = Field(default_factory=list)
