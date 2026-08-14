"""
Unit test untuk validator konektivitas dan kapabilitas AI Relay.
"""

import pytest
from bansos_ai.core.models import RelayTarget
from bansos_ai.core.validator import BansosAIValidator

@pytest.mark.asyncio
async def test_validate_target_invalid():
    # Menguji endpoint tak dikenal yang dipastikan unreachable/invalid
    target = RelayTarget(
        url="https://invalid-nonexistent-domain-12345.org",
        base_url="https://invalid-nonexistent-domain-12345.org",
        source="Test"
    )
    
    validator = BansosAIValidator(timeout=2.0)
    res = await validator.validate_target(target)
    
    assert res.is_valid is False
    assert res.is_agent_working is False
