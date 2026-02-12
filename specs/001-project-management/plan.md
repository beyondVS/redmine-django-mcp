# 구현 계획: Redmine 프로젝트 관리

**브랜치**: `001-project-management` | **날짜**: 2026-02-12 | **사양**: `specs/001-project-management/spec.md`
**입력**: `/specs/001-project-management/spec.md`의 기능 사양서

## 요약
Redmine REST API를 기반으로 프로젝트 목록 조회, 상세 정보 조회, 멤버 및 역할 관리, 그리고 2단계 승인을 통한 프로젝트 생성 및 수정 기능을 구현합니다. 기술적으로는 FastMCP(Python)를 사용하여 MCP 서버를 구축하고, OAuth 토큰 브릿지 레이어를 통해 보안을 강화합니다.

## 기술적 컨텍스트

**언어/버전**: Python 3.11+  
**주요 의존성**: FastMCP, httpx (API 통신), Pydantic (데이터 검증)  
**저장소**: In-memory (토큰 매핑 및 승인 상태 관리)  
**테스트**: pytest (단위 및 통합 테스트)  
**대상 플랫폼**: MCP 호환 클라이언트 (Claude Desktop 등)
**프로젝트 유형**: 단일 프로젝트 (MCP Server)  
**성능 목표**: 멤버 조회 3초 이내 (SC-001)  
**제약 사항**: <100MB 메모리 사용, 실시간 API 동기화 필요

## 헌법 준수 확인

*게이트: 0단계 조사 전에 통과해야 함. 1단계 설계 후 재확인.*

- [x] **API 스펙 동기화**: `http://localhost:8000/api/schema/`에서 최신 스펙을 가져와 `docs/api/openapi.json`에 저장했는가?
- [x] **최신 스펙 참조**: 작업을 위한 모든 근거가 최신 API 스펙에 기반하고 있는가?
- [x] **할루시네이션 방지**: 확실하지 않은 API 동작에 대해 추측 대신 스펙을 확인했는가?
- [x] **한국어 커밋 메시지**: 모든 커밋은 한국어로 작성되었는가?
- [x] **2단계 승인**: 프로젝트 생성/수정에 대해 2단계 승인 프로세스를 설계했는가?

## 프로젝트 구조

### 문서 (이 기능 관련)

```text
specs/001-project-management/
├── plan.md              # 이 파일
├── research.md          # 0단계 출력 (기술 결정 및 조사)
├── data-model.md        # 1단계 출력 (엔티티 정의)
├── quickstart.md        # 1단계 출력 (사용 가이드)
├── contracts/           # 1단계 출력 (MCP 도구 명세)
└── tasks.md             # 2단계 출력 (예정)
```

### 소스 코드 (저장소 루트)

```text
src/
└── redmine_django_mcp/
    ├── server.py        # FastMCP 서버 진입점
    ├── tools/
    │   ├── project.py   # 프로젝트 관련 도구 구현
    │   └── approval.py  # 승인 토큰 관리 및 도구
    ├── services/
    │   ├── redmine_api.py # Redmine API 클라이언트
    │   └── auth.py      # OAuth 토큰 브릿지 서비스
    └── models/
        └── schemas.py   # Pydantic 모델 정의

tests/
├── integration/         # Redmine API 연동 테스트
└── unit/                # 로직 단위 테스트
```

**구조 결정**: 단일 MCP 서버 프로젝트 구조를 따르며, 관심사 분리를 위해 도구, 서비스, 모델 레이어를 나눕니다.

## 복잡성 추적

| 위반 사항 | 필요한 이유 | 더 간단한 대안을 거부한 이유 |
|-----------|------------|---------------------------|
| OAuth 브릿지 레이어 | 헌법의 보안 및 인증 우선 원칙 준수 | 클라이언트 직접 인증은 보안상 위험함 |
| 2단계 승인 토큰 시스템 | AI 작업의 안정성 및 사용자 통제권 보장 | 인터럽트 방식은 현재 인프라에서 불안정함 |
