import os
import sys
import httpx
from fastmcp import FastMCP

# 헌법 6번 원칙: API 스펙 동기화 로직
def sync_api_spec():
    url = "http://localhost:8000/api/schema/"
    save_path = os.path.join("docs", "api", "openapi.json")
    
    # 디렉토리 생성
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    print(f"Syncing API spec from {url}...")
    try:
        with httpx.Client() as client:
            response = client.get(url)
            response.raise_for_status()
            with open(save_path, "wb") as f:
                f.write(response.content)
        print(f"Successfully synced to {save_path}")
    except Exception as e:
        print(f"Warning: Failed to sync API spec: {e}")
        if os.path.exists(save_path):
            print("Using existing local API spec as fallback.")
        else:
            # 엄격한 중단 조건
            print("CRITICAL: No API spec available (online or local). Aborting.")
            raise SystemExit(1)

# 서버 초기화 전 동기화 수행
# sync_api_spec()

# MCP 서버 생성
mcp = FastMCP("redmine-django-mcp")

# 도구 임포트 (등록을 위해 호출)
# 스크립트로 직접 실행 시 패키지 경로(src)를 sys.path에 추가하여 모듈을 찾을 수 있게 함
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from redmine_django_mcp.tools import project as _project_tools
from redmine_django_mcp.tools import approval as _approval_tools


# 기본 도구 예시 (구현 중임을 알림)
@mcp.tool()
def health_check() -> str:
    """MCP 서버의 상태를 확인합니다."""
    return "Redmine-Django MCP Server is running."

if __name__ == "__main__":
    mcp.run()
