"""
Modul Async Validator untuk Menguji Konektivitas, Respon Latency, Model, dan Agen AI.
"""

import time
import asyncio
from typing import List, Optional
import httpx

from bansos_ai.config import DEFAULT_TIMEOUT, TEST_MODELS
from bansos_ai.core.models import RelayTarget, ValidationResult
from bansos_ai.utils.logger import logger
from bansos_ai.utils.net import get_async_client

class BansosAIValidator:
    """Validator asinkron untuk pengujian endpoint AI Relay."""

    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        self.timeout = timeout

    async def validate_target(self, target: RelayTarget) -> ValidationResult:
        """Menguji secara mendalam satu target Relay."""
        result = ValidationResult(target=target)
        base_url = target.base_url.rstrip('/')
        
        headers = {}
        if target.api_key:
            headers["Authorization"] = f"Bearer {target.api_key}"
            
        async with get_async_client(timeout=self.timeout, headers=headers) as client:
            start_time = time.time()
            
            # Step 1: Tes Endpoint /v1/models
            models_url = f"{base_url}/v1/models"
            try:
                resp = await client.get(models_url)
                result.status_code = resp.status_code
                latency = (time.time() - start_time) * 1000
                result.latency_ms = round(latency, 2)
                
                if resp.status_code == 200:
                    result.is_valid = True
                    result.is_one_api_format = True
                    try:
                        data = resp.json()
                        if isinstance(data, dict) and "data" in data:
                            model_list = [m.get("id") for m in data["data"] if isinstance(m, dict) and "id" in m]
                            result.supported_models = model_list[:10]  # Ambil 10 model pertama
                        result.status_message = "Endpoint Active (200 OK)"
                    except Exception:
                        result.status_message = "Endpoint 200 OK (Non-JSON response)"
                elif resp.status_code in [401, 403]:
                    result.is_valid = True
                    result.status_message = f"Endpoint Online ({resp.status_code} Auth Required)"
                else:
                    result.status_message = f"HTTP Status {resp.status_code}"
            except httpx.TimeoutException:
                result.status_message = "Connection Timeout"
                return result
            except Exception as e:
                result.status_message = f"Error: {type(e).__name__}"
                return result

            # Step 2: Tes Agent Completion & Per-Model Workability
            if result.is_valid:
                chat_url = f"{base_url}/v1/chat/completions"
                
                # Daftar model yang akan diuji secara spesifik
                models_to_test = []
                if result.supported_models:
                    models_to_test.extend([m for m in result.supported_models if any(tm in m.lower() for tm in ["gpt-4", "claude", "deepseek", "gemini", "o1", "qwen"])][:4])
                if not models_to_test:
                    models_to_test = ["gpt-4o-mini", "gpt-3.5-turbo"]

                for test_m in models_to_test:
                    payload = {
                        "model": test_m,
                        "messages": [{"role": "user", "content": "ping"}],
                        "max_tokens": 5
                    }
                    try:
                        chat_resp = await client.post(chat_url, json=payload)
                        if chat_resp.status_code == 200:
                            chat_data = chat_resp.json()
                            if "choices" in chat_data and len(chat_data["choices"]) > 0:
                                result.is_agent_working = True
                                result.tested_models_status[test_m] = True
                            else:
                                result.tested_models_status[test_m] = False
                        else:
                            result.tested_models_status[test_m] = False
                    except Exception:
                        result.tested_models_status[test_m] = False

                if result.is_agent_working:
                    working_models = [m for m, ok in result.tested_models_status.items() if ok]
                    result.status_message = f"Agent WORK! ({', '.join(working_models[:2])})"


            # Step 3: Cek Quota/Saldo (jika ada API key)
            if target.api_key and result.is_valid:
                usage_url = f"{base_url}/v1/dashboard/billing/credit_grants"
                try:
                    quota_resp = await client.get(usage_url)
                    if quota_resp.status_code == 200:
                        qdata = quota_resp.json()
                        if "total_available" in qdata:
                            result.available_quota = f"${qdata.get('total_available', 0)}"
                except Exception:
                    pass

        return result


    async def validate_batch(self, targets: List[RelayTarget], max_concurrency: int = 10) -> List[ValidationResult]:
        """Menguji sekelompok target secara asinkron dengan batasan konkuensi."""
        semaphore = asyncio.Semaphore(max_concurrency)
        
        async def sem_validate(target: RelayTarget):
            async with semaphore:
                return await self.validate_target(target)
                
        logger.info(f"Memulai pengujian otomatis pada [cyan]{len(targets)}[/cyan] target endpoint...")
        tasks = [sem_validate(t) for t in targets]
        results = await asyncio.gather(*tasks)
        
        valid_count = sum(1 for r in results if r.is_valid)
        agent_count = sum(1 for r in results if r.is_agent_working)
        
        logger.info(f"Pengujian selesai: [green]{valid_count} Endpoint Valid[/green] | [bold green]{agent_count} Agent Siap Pakai[/bold green]")
        return results
