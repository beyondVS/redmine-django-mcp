# 조사 및 기술 결정: Redmine 프로젝트 관리

이 문서는 프로젝트 관리 기능 구현을 위한 주요 기술 결정 사항과 근거를 기록합니다.

## 기술 결정 사항

### 1. MCP 프레임워크 선정
- **결정**: [FastMCP (Python)](https://github.com/jlowin/fastmcp)
- **근거**: 
    - 헌법의 Python 3.11+ 환경과 완벽히 호환됨.
    - 장식자(Decorator) 기반의 직관적인 도구(Tool) 및 리소스(Resource) 정의가 가능하여 개발 속도가 빠름.
    - MCP 표준 명세를 충실히 구현하고 있으며, 향후 확장이 용이함.
- **고려된 대안**: MCP 공식 Python SDK (mcp-python-sdk) - 더 저수준의 제어가 가능하지만 설정 코드가 복잡함.

### 2. OAuth 토큰 브릿지 전략
- **결정**: MCP Server 내부에 **OAuth 토큰 매핑 레이어** 구축
- **근거**: 
    - 사양서 `FR-001` 준수: 사용자의 Redmine API 키를 직접 노출하지 않고 Server에서 안전하게 관리함.
    - Client에게는 MCP 전용 세션 토큰을 발급하여 보안 계층을 분리함.
- **고려된 대안**: 클라이언트가 직접 Redmine 키를 전달하는 방식 - 보안 및 헌법의 '인증 우선' 원칙에 위배됨.

### 3. 2단계 승인 프로세스 (Two-Phase Approval)
- **결정**: **메모리 기반 승인 토큰(Approval Token) 시스템**
- **근거**: 
    - `FR-005` 준수: 파괴적인 작업(생성/수정) 전 명시적인 사용자 승인 단계 제공.
    - 상태(State)를 서버 메모리에 일시 저장하고 고유 토큰을 발급하여, 사용자가 `approve <token>` 명령을 내릴 때만 실제 API를 호출함.
- **고려된 대안**: MCP 도구 내 인터럽트(Interrupt) - 현재 대부분의 LLM 인터페이스에서 도구 실행 중 사용자 입력을 받는 기능이 불안정함.

### 4. API 스펙 동기화 전략
- **결정**: **동적 스키마 로드 및 로컬 캐싱**
- **근거**: 
    - 헌법 `III. 6` 준수: `http://localhost:8000/api/schema/`를 최우선으로 참조.
    - 서버 시작 시 또는 명시적 갱신 요청 시 스펙을 `docs/api/openapi.json`에 동기화하여 안정적인 도구 스키마 생성을 보장함.

## 조사 작업 결과
- **Redmine API 엔드포인트 확인**: `/projects.json`, `/projects/{id}.json`, `/projects/{id}/memberships.json` 사용 확인됨.
- **인증 헤더**: `X-Redmine-API-Key` 헤더 사용 방식 확인.
