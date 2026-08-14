"""
Unit test untuk modul scraper dan pemroses URL/Key.
"""

import pytest
from bansos_ai.core.scraper import BansosAIScraper

def test_clean_base_url():
    scraper = BansosAIScraper()
    
    assert scraper.clean_base_url("https://api.one-api.cn/v1/chat/completions") == "https://api.one-api.cn"
    assert scraper.clean_base_url("http://relay.example.com:8080/v1/models") == "http://relay.example.com:8080"
    assert scraper.clean_base_url("https://sub.domain.org/register?ref=123") == "https://sub.domain.org"

def test_is_blacklisted():
    scraper = BansosAIScraper()
    
    assert scraper.is_blacklisted("https://www.google.com/search?q=test") is True
    assert scraper.is_blacklisted("https://github.com/topics/one-api") is True
    assert scraper.is_blacklisted("https://api.free-relay-station.com/v1") is False

def test_extract_keys_from_text():
    scraper = BansosAIScraper()
    sample_text = "Share API Key gratis: sk-abc123def456ghi789jkl012mno345pqr678 dan selamat mencoba!"
    
    keys = scraper.extract_keys_from_text(sample_text)
    assert len(keys) == 1
    assert keys[0].startswith("sk-")
