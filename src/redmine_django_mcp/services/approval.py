import secrets
import time
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class ApprovalService:
    def __init__(self, ttl_minutes: int = 30):
        self.ttl_minutes = ttl_minutes
        # token -> { "payload": Dict, "expires_at": float, "action_type": str }
        self._pending_actions: Dict[str, Dict[str, Any]] = {}

    def create_request(self, action_type: str, payload: Dict[str, Any]) -> str:
        """승인 요청을 생성하고 토큰을 반환합니다."""
        token = secrets.token_urlsafe(16)
        expires_at = time.time() + (self.ttl_minutes * 60)
        
        self._pending_actions[token] = {
            "action_type": action_type,
            "payload": payload,
            "expires_at": expires_at
        }
        return token

    def get_request(self, token: str) -> Optional[Dict[str, Any]]:
        """토큰에 해당하는 유효한 요청을 반환합니다. 만료된 경우 삭제합니다."""
        request = self._pending_actions.get(token)
        if not request:
            return None
        
        if time.time() > request["expires_at"]:
            del self._pending_actions[token]
            return None
            
        return request

    def consume_request(self, token: str) -> Optional[Dict[str, Any]]:
        """승인 처리 후 요청을 삭제하고 페이로드를 반환합니다."""
        request = self.get_request(token)
        if request:
            del self._pending_actions[token]
        return request

# 글로벌 싱글톤 인스턴스
approval_service = ApprovalService()
