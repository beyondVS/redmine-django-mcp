<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- List of modified principles:
  - 핵심 원칙 통합 (AGENTS.md의 철학 반영)
  - 할루시네이션 방지 지침 추가
  - 기술 환경(Technical Context) 상세화
- Added sections: 핵심 철학, 할루시네이션 방지 지침, 기술 환경
- Removed sections: N/A
- Templates requiring updates (✅ updated):
  - .specify/templates/plan-template.md ✅
  - .specify/templates/spec-template.md ✅
  - .specify/templates/tasks-template.md ✅
- Follow-up TODOs: N/A
-->

# redmine-django-mcp 헌법(Constitution)

## I. 핵심 철학 (Core Philosophy)

1.  **자기 평가 및 반복 (Self-Evaluation & Iteration)**
    *   작업을 시작하기 전에 세계 최고 수준의 평가 기준을 수립합니다.
    *   결과물을 스스로 채점하고, 만점을 받을 때까지 내부적으로 반복 개선(Self-Correction)한 뒤 최종 결과만 제시합니다.

2.  **실용주의 및 단순성 (Pragmatism & Simplicity)**
    *   **Over-engineering을 엄격히 금지**합니다.
    *   미래의 막연한 확장성보다 현재의 요구사항 해결에 집중하며, 복잡도(Complexity)를 비용으로 간주하여 가장 단순하고 명확한 해결책을 우선합니다. (YAGNI 원칙)

3.  **사고 과정 (Thinking Process)**
    *   코드를 작성하기 전 단계별 계획(Step-by-step)을 수립하여 논리적 비약을 방지합니다.
    *   기존 기능의 파괴(Regression) 가능성을 항상 먼저 검토합니다.

4.  **언어 및 톤 (Language & Tone)**
    *   **Communication:** 한국어를 기본으로 사용하며, 명료하고 전문적인 어조를 유지합니다. 모든 Git 커밋 메시지는 한국어로 작성합니다.
    *   **Code:** 변수명 등 식별자는 영어를 사용하되, 주석은 한국어를 사용하여 의미 전달을 명확히 합니다.

## II. 기술 환경 (Technical Context)

| Category | Stack                      | Note |
| :--- |:---------------------------| :--- |
| **Type** | MCP Server (Django Bridge) | Redmine-Django 연동을 위한 MCP 서버 |
| **Language** | Python 3.11+               | pyproject.toml 기준 |
| **Framework** | FastMCP 3.x                | MCP SDK integration |
| **Database** | SQLite/PostgreSQL          | Redmine 연동 데이터베이스 |
| **Linter** | Ruff                       | 코드 품질 관리 |

## III. 핵심 원칙 (Core Principles)

### 1. MCP 표준 준수
모든 도구(Tools), 리소스(Resources), 프롬프트(Prompts)는 Model Context Protocol(MCP) 명세를 엄격히 따라야 합니다. 표준을 벗어난 독자적인 확장보다는 프로토콜의 호환성을 최우선으로 합니다.

### 2. Django-Redmine 연동 무결성
본 프로젝트는 `redmine-django` 프로젝트를 기반으로 합니다. MCP를 통해 노출되는 모든 기능은 원본 프로젝트의 비즈니스 로직, 데이터 모델, 그리고 권한 체계를 절대적으로 존중하며 이를 우회하지 않습니다.

### 3. 보안 및 인증 우선
Redmine API 키, 사용자 세션 등의 민감 정보는 절대로 로그에 남기지 않으며, 환경 변수나 안전한 저장소를 통해 관리합니다. 모든 도구 실행 시 적절한 권한 검사를 거쳐야 합니다.

### 4. 테스트 주도 개발 (TDD)
모든 MCP 도구 및 서비스 로직은 구현 전에 테스트 케이스가 작성되어야 합니다. 특히 MCP 도구의 입력 인자(Arguments)와 출력 결과(Results)에 대한 스키마 검증은 필수적입니다.

### 5. 명확한 LLM 문서화
MCP 도구의 `description` 필드는 LLM이 해당 도구의 용도와 사용법을 명확히 이해할 수 있도록 구체적이고 서술적으로 작성되어야 합니다.

## IV. 할루시네이션 방지 지침 (Hallucination Prevention Policy)

1.  **지식의 한계 인정**: 확실하지 않은 정보는 지어내지 않으며, 불확실할 경우 정직하게 인정합니다.
2.  **신뢰도 표기**: 추측이 필요한 경우 문장 앞에 **[추측]** 라벨을 붙이고 검증이 필요함을 명시합니다.
3.  **근거 우선**: 즉시 결론을 내리지 말고, 답변을 도출하는 논리적 과정(Chain of Thought)을 먼저 서술합니다.
4.  **자체 검열**: 답변을 최종 출력하기 전에 논리적 비약이나 사실 오류가 없는지 스스로 비판하고 수정합니다.

## V. 개발 워크플로우

### 품질 게이트 (Quality Gates)
1. 모든 기능은 `spec.md`에서 정의된 사용자 시나리오를 통과해야 합니다.
2. 모든 도구는 MCP Inspector를 통해 스키마 유효성 검사를 통과해야 합니다.
3. 코드 리뷰 시 헌법 준수 여부를 반드시 확인합니다.
4. **최소 변경 원칙**: 요청한 기능을 구현하는 데 필요한 코드만 수정합니다.

## 거버넌스(Governance)
본 헌법은 프로젝트의 모든 개발 관행보다 우선합니다. 헌법의 개정은 명확한 사유와 함께 문서화되어야 하며, 버전 관리 정책을 따릅니다.

**버전**: 1.1.0 | **비준일**: 2026-02-11 | **최종 수정일**: 2026-02-11
