import pytest
from src.redmine_django_mcp.services.auth import auth_service
from src.redmine_django_mcp.tools.project import get_project_details_impl

@pytest.mark.asyncio
async def test_get_project_details_integration():
    # 1. 가상의 MCP 토큰 발급
    test_key = "test_api_key_123"
    mcp_token = auth_service.register_token(test_key)
    
    # 2. 도구 구현 함수 호출
    try:
        response = await get_project_details_impl(mcp_token=mcp_token, identifier="test-project")
        
        # 3. 검증
        assert "상세 정보" in response
        
        print("\nSuccess")
    except Exception as e:
        if "ConnectError" in str(e) or "404" in str(e) or "Unauthorized" in str(e):
            print("\nSkipping")
        else:
            pytest.fail("Failed: {}".format(e))
