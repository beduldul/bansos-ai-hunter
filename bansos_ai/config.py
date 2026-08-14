"""
Konfigurasi kata kunci, reguler ekspresi, dan parameter jaringan
untuk pemindaian endpoint AI Relay ("AI中转站") dan kuota gratis.
"""

from typing import List, Dict

# Platform Sosmed & Forum Target
TARGET_SOCIAL_PLATFORMS: Dict[str, str] = {
    "Reddit": "site:reddit.com",
    "Threads": "site:threads.net",
    "Facebook": "site:facebook.com",
    "Twitter/X": "site:x.com",
    "Linux.do": "site:linux.do",
    "NodeSeek": "site:nodeseek.com",
    "V2EX": "site:v2ex.com",
    "Baidu Tieba": "site:tieba.baidu.com",
    "Xiaohongshu": "site:xiaohongshu.com",
    "QQ / Weixin Post": "site:mp.weixin.qq.com",
}

# Kata kunci pencarian spesifik (Mandarin, Indonesia, Inggris)
CHINESE_KEYWORDS: List[str] = [
    "AI中转站",
    "免费额度",
    "免费API",
    "注册送额度",
    "注册送API",
    "模型中转",
    "大模型API",
    "AI接口",
    "One-API 免费中转",
    "New-API 注册送",
    "Claude 3.5 Sonnet 免费API",
    "Claude 3.7 Sonnet 中转",
    "Claude Opus 免费中转",
    "DeepSeek R1 免费API",
    "O1 中转站 免费",
]

GLOBAL_KEYWORDS: List[str] = [
    "bansos ai api",
    "free openai api relay",
    "free api key one-api",
    "free claude 3.5 sonnet api relay",
    "free deepseek r1 api relay",
    "free gpt-4o api relay",
    "shared openai api base url",
]

# Pola Regex untuk Menemukan URL Base OpenAI-Compatible dan Key (sk-...)
URL_REGEX: str = r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?::\d+)?(?:/[a-zA-Z0-9_.-]*)*/?'
API_KEY_REGEX: str = r'sk-[a-zA-Z0-9]{32,64}'

# Blacklist domain korporat/bantuan/dokumentasi/sosmed/search engine (bukan relay API)
DOMAIN_BLACKLIST: List[str] = [
    "google.com", "bing.com", "duckduckgo.com", "baidu.com", "tieba.baidu.com",
    "yahoo.com", "yandex.com", "startpage.com", "mojeek.com", "brave.com",
    "youtube.com", "wikipedia.org", "grokipedia.com", "amazon.com", "taobao.com",
    "github.com", "gitlab.com", "microsoft.com", "openai.com", "anthropic.com",
    "help.aliyun.com", "cloud.tencent.com", "huaweicloud.com",
    "docs.openai.com", "learn.microsoft.com", "support.google.com",
    "w3schools.com", "developer.mozilla.org",
    # Platform Sosmed & Forum (Tempat mencari, bukan endpoint API itu sendiri)
    "reddit.com", "www.reddit.com", "x.com", "twitter.com", "facebook.com", "www.facebook.com",
    "threads.net", "www.threads.net", "linux.do", "www.linux.do",
    "nodeseek.com", "www.nodeseek.com", "v2ex.com", "www.v2ex.com",
    "xiaohongshu.com", "open.xiaohongshu.com", "ad-market.xiaohongshu.com", "e.xiaohongshu.com",
    "job.xiaohongshu.com", "beian.xiaohongshu.com", "security.xiaohongshu.com", "miniapp.xiaohongshu.com",
    "qq.com", "weixin.qq.com", "mp.weixin.qq.com"
]





# Daftar Model AI Tertinggi (Flagship & Top Tier) yang Diutamakan dalam Uji Ketersediaan
TEST_MODELS: List[str] = [
    "claude-3-7-sonnet",
    "claude-3-5-sonnet",
    "claude-3-opus",
    "claude-sonnet-5",
    "gpt-4.5-preview",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-sol",
    "o1",
    "o3-mini",
    "fable-5",
    "fable",
    "deepseek-r1",
    "deepseek-v3",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
    "qwen-max",
]


# Parameter Koneksi Network untuk M4 Pro High-Performance Concurrency
DEFAULT_TIMEOUT: float = 3.0
MAX_CONCURRENT_TASKS: int = 50
DEFAULT_USER_AGENT: str = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
)

