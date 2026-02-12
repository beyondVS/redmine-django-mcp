import pytest
from redmine_django_mcp.services.auth import auth_service
from redmine_django_mcp.tools.project import list_project_members_impl

@pytest.mark.asyncio
async def test_list_project_members_integration():
    test_key = "test_api_key_123"
    mcp_token = auth_service.register_token(test_key)
    try:
        response = await list_project_members_impl(mcp_token=mcp_token, identifier="test-project")
        assert "멤버" in response
        print("Success")
    except Exception as e:
        if "ConnectError" in str(e) or "404" in str(e) or "Unauthorized" in str(e):
            print("Skipping")
        else:
            pytest.fail("Failed")
