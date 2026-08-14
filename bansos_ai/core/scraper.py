"""
Modul Pemindai & Harvester (Scraper) Multi-Source untuk Menemukan Target AI Relay & API Key.
"""

import re
import urllib.parse
from typing import List, Set, Dict, Any
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


from bansos_ai.config import (
    CHINESE_KEYWORDS,
    GLOBAL_KEYWORDS,
    DOMAIN_BLACKLIST,
    URL_REGEX,
    API_KEY_REGEX
)
from bansos_ai.core.models import RelayTarget
from bansos_ai.utils.logger import logger
from bansos_ai.utils.net import get_async_client

class BansosAIScraper:
    """Pemindai dan pemroses sumber web untuk pencarian API Relay AI gratisan."""

    def __init__(self, max_results_per_query: int = 15):
        self.max_results_per_query = max_results_per_query
        self.seen_urls: Set[str] = set()

    def clean_base_url(self, raw_url: str) -> str:
        """Membersihkan dan menormalisasi URL menjadi Base URL standar."""
        try:
            parsed = urllib.parse.urlparse(raw_url)
            scheme = parsed.scheme if parsed.scheme in ['http', 'https'] else 'https'
            netloc = parsed.netloc
            if not netloc:
                return ""
            
            # Hapus path spesifik jika ada (/v1/chat/completions -> base URL)
            path = parsed.path
            if "/v1" in path:
                base_path = path.split("/v1")[0]
                return f"{scheme}://{netloc}{base_path}".rstrip('/')
            
            return f"{scheme}://{netloc}".rstrip('/')
        except Exception:
            return ""

    def is_blacklisted(self, url: str) -> bool:
        """Memeriksa apakah domain URL ada di daftar hitam (blacklist)."""
        url_lower = url.lower()
        for domain in DOMAIN_BLACKLIST:
            if domain in url_lower:
                return True
        return False

    def extract_keys_from_text(self, text: str) -> List[str]:
        """Mengekstrak API Key OpenAI-compatible (format sk-...) dari teks."""
        if not text:
            return []
        matches = re.findall(API_KEY_REGEX, text)
        return list(set(matches))

    async def search_social_media(self, platform_name: str, site_query: str, keywords: List[str]) -> List[RelayTarget]:
        """Memindai spesifik platform sosial media / forum (Threads, Facebook, Reddit, Linux.do, dll)."""
        targets: List[RelayTarget] = []
        for kw in keywords[:4]:  # Ambil kata kunci utama untuk tiap platform
            combined_query = f"{site_query} {kw}"
            logger.info(f"📱 Memindai Platform [bold yellow]{platform_name}[/bold yellow] dengan query: [cyan]'{combined_query}'[/cyan]")
            
            try:
                ddgs = DDGS()
                results = list(ddgs.text(combined_query, max_results=self.max_results_per_query))
                
                for res in results:
                    href = res.get("href", "")
                    title = res.get("title", "")
                    snippet = res.get("body", "")
                    
                    if not href:
                        continue
                        
                    # 1. Ekstrak Base URL Relay dari dalam postingan / snippet sosmed
                    urls_in_post = re.findall(URL_REGEX, f"{title} {snippet}")
                    extracted_keys = self.extract_keys_from_text(f"{title} {snippet}")
                    api_key = extracted_keys[0] if extracted_keys else None
                    
                    # Jika postingan menyebutkan URL relay tertentu (misal: https://api.xxx.com)
                    relay_url_found = None
                    for u in urls_in_post:
                        if not self.is_blacklisted(u) and "site:" not in u:
                            cleaned = self.clean_base_url(u)
                            if cleaned and cleaned not in self.seen_urls:
                                relay_url_found = cleaned
                                break
                    
                    target_base = relay_url_found if relay_url_found else self.clean_base_url(href)
                    if not target_base or target_base in self.seen_urls:
                        continue
                        
                    self.seen_urls.add(target_base)
                    
                    targets.append(RelayTarget(
                        url=href,
                        base_url=target_base,
                        api_key=api_key,
                        source=f"Social Media ({platform_name})",
                        title=title,
                        snippet=snippet,
                        matched_keyword=combined_query
                    ))
            except Exception as e:
                logger.warning(f"⚠️ Gagal memindai {platform_name} query '{combined_query}': {e}")
                
        return targets

    async def search_ddg(self, query: str) -> List[RelayTarget]:
        """Melakukan pencarian umum melalui DuckDuckGo Search."""
        targets: List[RelayTarget] = []
        logger.info(f"🔎 Memindai Web Umum dengan query: [cyan]'{query}'[/cyan]")
        
        try:
            ddgs = DDGS()
            results = list(ddgs.text(query, max_results=self.max_results_per_query))
            
            for res in results:
                href = res.get("href", "")
                title = res.get("title", "")
                snippet = res.get("body", "")
                
                if not href or self.is_blacklisted(href):
                    continue
                    
                base_url = self.clean_base_url(href)
                if not base_url or base_url in self.seen_urls:
                    continue
                    
                self.seen_urls.add(base_url)
                
                extracted_keys = self.extract_keys_from_text(f"{title} {snippet}")
                api_key = extracted_keys[0] if extracted_keys else None
                
                targets.append(RelayTarget(
                    url=href,
                    base_url=base_url,
                    api_key=api_key,
                    source="General Web Search",
                    title=title,
                    snippet=snippet,
                    matched_keyword=query
                ))
        except Exception as e:
            logger.warning(f"⚠️ Gagal memindai web query '{query}': {e}")
            
        return targets

    async def scrape_all(self, include_chinese: bool = True, custom_keywords: List[str] = None, social_only: bool = False) -> List[RelayTarget]:
        """Menjalankan proses scraping komprehensif dari Sosial Media, Forum, dan Mesin Pencari."""
        from bansos_ai.config import TARGET_SOCIAL_PLATFORMS
        
        keywords = []
        if custom_keywords:
            keywords.extend(custom_keywords)
        else:
            if include_chinese:
                keywords.extend(CHINESE_KEYWORDS)
            keywords.extend(GLOBAL_KEYWORDS)

        all_targets: List[RelayTarget] = []
        
        # 1. Scrape Khusus Sosmed & Forum (Threads, Facebook, Reddit, Linux.do, NodeSeek, Xiaohongshu)
        for platform, site_q in TARGET_SOCIAL_PLATFORMS.items():
            social_targets = await self.search_social_media(platform, site_q, keywords)
            all_targets.extend(social_targets)

        # 2. General Web Scrape jika tidak social_only
        if not social_only:
            for kw in keywords[:3]:
                found = await self.search_ddg(kw)
                all_targets.extend(found)

        logger.info(f"✨ Total target postingan & relay unik berhasil dikumpulkan: [green]{len(all_targets)}[/green]")
        return all_targets


