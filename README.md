# Redmine-Django MCP Server

Redmine-Django API를 Model Context Protocol(MCP)을 통해 사용할 수 있게 해주는 브릿지 서버입니다.

## 주요 기능
- **프로젝트 관리**: 목록 조회, 상세 정보 및 계층 구조 확인
- **멤버 관리**: 프로젝트별 멤버 및 역할(Role) 조회
- **안전한 데이터 변경**: 2단계 승인 토큰 시스템을 통한 프로젝트 생성 및 수정
- **OAuth 브릿지**: MCP Client 토큰과 실제 Redmine API 키를 분리하여 보안 강화

## 설치 및 실행

1. **의존성 설치**:
   ```bash
   pip install -e .
   ```

2. **서버 실행**:
   ```bash
   python -m src.redmine_django_mcp.server
   ```

## 사용 가능한 도구 (Tools)
- `list_projects`: 프로젝트 목록 조회
- `get_project_details`: 프로젝트 상세 정보 및 계층 확인
- `list_project_members`: 프로젝트 멤버 및 역할 조회
- `request_project_create`: 프로젝트 생성 요청 (승인 토큰 발급)
- `request_project_update`: 프로젝트 수정 요청 (승인 토큰 발급)
- `approve_action`: 승인 토큰을 사용한 최종 작업 실행

## 라이선스
MIT License
