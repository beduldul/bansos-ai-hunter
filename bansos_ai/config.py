"""
Konfigurasi kata kunci, reguler ekspresi, dan parameter jaringan
untuk pemindaian endpoint AI Relay ("AI中转站") dan kuota gratis.
"""

from typing import List, Dict

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
    "充值",
    "余额",
    "One-API 免费中转",
    "New-API 注册送",
    "Claude 3.5 Sonnet 免费API",
    "Claude 3.7 Sonnet 中转",
    "Claude Opus 免费中转",
    "GPT-4o 免费额度",
    "DeepSeek R1 免费API",
    "O1 中转站 免费",
    "Qwen Max 免费接口",
]

GLOBAL_KEYWORDS: List[str] = [
    "bansos ai api",
    "free openai api relay",
    "free api key one-api",
    "free claude 3.5 sonnet api relay",
    "free claude opus api key",
    "free deepseek r1 api relay",
    "free gpt-4o api relay",
    "free o1 o3-mini api relay",
    "new-api free trial quota",
    "shared openai api base url",
    "flagship ai model free api proxy",
]

# Ekstraksi URL & Domain Relay yang Dikenal
ONE_API_PATHS: List[str] = [
    "/v1/models",
    "/v1/chat/completions",
    "/v1/user/self",
    "/register",
    "/login",
    "/dashboard",
]

# Pola Regex untuk Menemukan URL Base OpenAI-Compatible dan Key (sk-...)
URL_REGEX: str = r'https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?::\d+)?(?:/[a-zA-Z0-9_.-]*)*/?'
API_KEY_REGEX: str = r'sk-[a-zA-Z0-9]{32,64}'

# Blacklist domain yang tidak relevan (Sosmed utama, e-commerce, dsb.)
DOMAIN_BLACKLIST: List[str] = [
    "google.com", "bing.com", "duckduckgo.com", "baidu.com",
    "youtube.com", "facebook.com", "instagram.com", "twitter.com",
    "x.com", "wikipedia.org", "amazon.com", "taobao.com",
    "github.com", "gist.github.com", "gitlab.com"
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


# Parameter Koneksi Network
DEFAULT_TIMEOUT: float = 8.0
MAX_CONCURRENT_TASKS: int = 15
DEFAULT_USER_AGENT: str = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
)
