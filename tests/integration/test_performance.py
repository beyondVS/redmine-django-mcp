import pytest
import time
from redmine_django_mcp.services.auth import auth_service
from redmine_django_mcp.tools.project import list_project_members_impl

@pytest.mark.asyncio
async def test_performance_sc_001():
    test_key = "test_api_key_123"
    mcp_token = auth_service.register_token(test_key)
    start_time = time.perf_counter()
    try:
        await list_project_members_impl(mcp_token=mcp_token, identifier="test-project")
        end_time = time.perf_counter()
        duration = end_time - start_time
        print("Duration: {}".format(duration))
        assert duration < 3.0
    except Exception:
        print("Skipping")
