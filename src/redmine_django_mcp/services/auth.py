import secrets
from typing import Dict, Optional

class AuthService:
    def __init__(self):
        # MCP Client Token -> Redmine API Key 매핑 (실제 운영 시에는 OAuth 토큰 관리)
        self._token_map: Dict[str, str] = {}

    def register_token(self, redmine_api_key: str) -> str:
        """Redmine API Key를 기반으로 MCP 전용 토큰을 발급하고 저장합니다."""
        mcp_token = f"mcp_{secrets.token_urlsafe(32)}"
        self._token_map[mcp_token] = redmine_api_key
        return mcp_token

    def get_redmine_key(self, mcp_token: str) -> Optional[str]:
        """MCP 토큰에 매핑된 Redmine API Key를 반환합니다."""
        return self._token_map.get(mcp_token)

    def refresh_session(self, mcp_token: str) -> bool:
        """
        토큰 만료를 감지하고 세션을 갱신합니다.
        (현재는 인메모리 구조이므로 유효성 확인만 수행)
        """
        if mcp_token in self._token_map:
            # 실운영 환경에서는 여기서 Refresh Token을 사용하여 Access Token을 갱신함
            return True
        return False


# 글로벌 싱글톤 인스턴스
auth_service = AuthService()
