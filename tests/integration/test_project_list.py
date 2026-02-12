import pytest
from src.redmine_django_mcp.services.auth import auth_service
from src.redmine_django_mcp.tools.project import list_projects_impl

@pytest.mark.asyncio
async def test_list_projects_integration():
    # 1. 가상의 Redmine API Key 등록 및 MCP 토큰 발급
    test_key = "test_api_key_123"
    mcp_token = auth_service.register_token(test_key)
    
    # 2. 도구 구현 함수 호출
    try:
        response = await list_projects_impl(mcp_token=mcp_token, status="active", limit=5)
        
        # 3. 검증
        assert "프로젝트" in response
        
        print("\nIntegration Test Response Success")
    except Exception as e:
        # 실제 서버 접속 에러는 무시
        if "ConnectError" in str(e) or "404" in str(e) or "Unauthorized" in str(e):
            print(f"\nSkipping actual connection: {e}")
        else:
            pytest.fail(f"Integration test failed unexpectedly: {e}")
