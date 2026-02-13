import os
import sys

# 도구 임포트 (등록을 위해 호출)
# 스크립트로 직접 실행 시 패키지 경로(src)를 sys.path에 추가하여 모듈을 찾을 수 있게 함
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from redmine_django_mcp.app import mcp

from redmine_django_mcp.tools import project as _project_tools
from redmine_django_mcp.tools import approval as _approval_tools


# 기본 도구 예시 (구현 중임을 알림)
@mcp.tool()
def health_check() -> str:
    """MCP 서버의 상태를 확인합니다."""
    return "Redmine-Django MCP Server is running."

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8010)
