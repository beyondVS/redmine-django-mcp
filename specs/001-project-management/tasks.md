# 작업 목록: Redmine 프로젝트 관리 (Project Management)

**입력**: `/specs/001-project-management/`의 설계 문서
**선행 조건**: plan.md, spec.md, research.md, data-model.md, contracts/mcp-tools.yaml

**조직**: 작업은 독립적인 구현 및 테스트가 가능하도록 사용자 스토리별로 그룹화됩니다.

## 형식: `[ID] [P?] [스토리] 설명`

- **[P]**: 병렬 실행 가능 (서로 다른 파일, 의존성 없음)
- **[스토리]**: 이 작업이 속한 사용자 스토리 (예: US1, US2, US3, US4)

---

## 1단계: 설정 (공통 인프라)

**목적**: 프로젝트 초기화 및 기본 구조

- [ ] T000 최신 API 스펙 동기화 (`http://localhost:8000/api/schema/` -> `docs/api/openapi.json`)
- [ ] T001 [P] `src/redmine_django_mcp/` 하위에 `tools/`, `services/`, `models/` 디렉토리 생성
- [ ] T002 [P] `pyproject.toml`에 `fastmcp`, `httpx`, `pydantic` 의존성 추가 및 설치
- [ ] T003 [P] `src/redmine_django_mcp/server.py`에 서버 시작 시 API 스펙 자동 동기화 로직이 포함된 진입점 구현

---

## 2단계: 기반 구축 (차단 선행 조건)

**목적**: 사용자 스토리를 구현하기 전에 반드시 완료되어야 하는 핵심 인프라

- [ ] T004 `src/redmine_django_mcp/models/schemas.py`에 Project, Member, Role 기본 Pydantic 모델 정의
- [ ] T005 `src/redmine_django_mcp/services/auth.py`에 OAuth 토큰 브릿지 및 매핑 로직 구현
- [ ] T006 `src/redmine_django_mcp/services/redmine_api.py`에 `httpx` 기반 공통 Redmine API 클라이언트 구현
- [ ] T007 [P] `src/redmine_django_mcp/services/approval.py`에 만료 시간(TTL) 기반 승인 토큰 관리 로직 구현

---

## 3단계: 사용자 스토리 1 - 프로젝트 현황 파악 (우선순위: P1) 🎯 MVP

**목표**: 상태 필터링 및 페이지네이션을 지원하는 프로젝트 목록 조회 기능

- [ ] T008 [P] [US1] `src/redmine_django_mcp/services/redmine_api.py`에 `list_projects` API 연동 메서드 추가
- [ ] T009 [US1] `src/redmine_django_mcp/tools/project.py`에 `list_projects` MCP 도구 구현
- [ ] T010 [US1] `tests/integration/test_project_list.py`에서 상태(Active/Closed) 필터링 및 증분 조회 테스트

---

## 4단계: 사용자 스토리 2 - 프로젝트 상세 및 계층 (우선순위: P1) 🎯 MVP

**목표**: 프로젝트 상세 정보 및 상/하위 계층 구조 조회 기능

- [ ] T011 [P] [US2] `src/redmine_django_mcp/services/redmine_api.py`에 `get_project` 상세 조회 API 연동 메서드 추가
- [ ] T012 [US2] `src/redmine_django_mcp/tools/project.py`에 `get_project_details` MCP 도구 구현
- [ ] T013 [US2] `tests/integration/test_project_detail.py`에서 식별자를 통한 상세 정보 및 계층 구조 데이터 검증

---

## 5단계: 사용자 스토리 3 - 멤버 및 역할 조회 (우선순위: P2)

**목표**: 프로젝트 멤버와 그들의 역할(ID, Name) 목록 조회

- [ ] T014 [P] [US3] `src/redmine_django_mcp/services/redmine_api.py`에 `get_memberships` API 연동 메서드 추가
- [ ] T015 [US3] `src/redmine_django_mcp/tools/project.py`에 `list_project_members` MCP 도구 구현
- [ ] T016 [US3] `tests/integration/test_project_members.py`에서 특정 프로젝트의 사용자별 역할 매핑 검증

---

## 6단계: 사용자 스토리 4 - 프로젝트 생성 및 수정 (우선순위: P2)

**목표**: 2단계 승인 프로세스를 통한 프로젝트 데이터 변경

- [ ] T017 [US4] `src/redmine_django_mcp/tools/approval.py`에 `request_project_create` 도구 구현 (승인 토큰 발급)
- [ ] T018 [US4] `src/redmine_django_mcp/tools/approval.py`에 `request_project_update` 도구 구현 (승인 토큰 발급)
- [ ] T019 [US4] `src/redmine_django_mcp/tools/approval.py`에 `approve_action` 도구 구현 (실제 API 호출)
- [ ] T020 [US4] `tests/integration/test_project_lifecycle.py`에서 생성 요청 -> 승인 -> 결과 확인 통합 시나리오 테스트

---

## N단계: 다듬기 및 교차 사안

**목적**: 문서화 및 최종 품질 검토

- [ ] T021 [P] `docs/api/openapi.json`과 구현된 도구 스키마의 일관성 재확인
- [ ] T022 [P] `README.md`에 프로젝트 관리 기능 도구 목록 및 사용법 추가
- [ ] T023 `src/redmine_django_mcp/server.py`에서 모든 도구의 `description` 필드 최적화 (LLM 가독성 향상)
- [ ] T024 [P] `src/redmine_django_mcp/services/auth.py`에 OAuth 액세스 토큰 만료 감지 및 세션 갱신(Refresh) 로직 구현
- [ ] T025 `tests/integration/test_performance.py`에서 모든 주요 도구의 응답 시간 측정 및 SC-001 준수 여부 검증

---

## 의존성 및 실행 순서

1. **설정(1단계)** 및 **기반 구축(2단계)**은 모든 사용자 스토리의 선행 조건입니다.
2. **US1**과 **US2**는 P1 우선순위로 가장 먼저 구현하며, 서로 병렬 작업이 가능합니다.
3. **US3**과 **US4**는 기반 인프라 완료 후 순차적으로 진행합니다.
4. **US4**는 `services/approval.py` 및 `services/redmine_api.py`의 쓰기 로직에 의존합니다.

## 구현 전략

### MVP 우선 (US1 & US2)
- 프로젝트 목록 조회와 상세 조회를 먼저 완성하여 사용자가 프로젝트 현황을 파악할 수 있는 최소한의 가치를 제공합니다.

### 점진적 인도
- US1, US2 (현황 파악) -> US3 (협업 대상 파악) -> US4 (관리 자동화) 순으로 기능을 확장합니다.
