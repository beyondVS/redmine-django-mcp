# 퀵스타트: Redmine 프로젝트 관리 (Project Management)

이 가이드는 Redmine 프로젝트 관리 기능을 MCP 도구로 사용하는 방법을 설명합니다.

## 개발 환경 설정

1. **의존성 설치**:
   ```bash
   pip install fastmcp
   ```

2. **서버 실행**:
   ```bash
   python src/redmine_django_mcp/server.py
   ```

## 도구 사용 예시

### 1. 프로젝트 목록 조회
`list_projects` 도구를 호출하여 활성 프로젝트 목록을 가져옵니다.
```json
{
  "status": "active",
  "limit": 10
}
```

### 2. 프로젝트 생성 (2단계 승인)
- **1단계: 요청**
  `request_project_create` 도구를 호출합니다.
  ```json
  {
    "name": "New MCP Project",
    "identifier": "mcp-new-project",
    "is_public": true
  }
  ```
  결과로 `approval_token: "xyz123"`를 받습니다.

- **2단계: 승인**
  `approve_action` 도구에 토큰을 전달하여 최종 승인합니다.
  ```json
  {
    "approval_token": "xyz123"
  }
  ```

## 주의 사항
- 프로젝트 삭제는 지원하지 않으므로 웹 UI를 사용해야 합니다.
- 승인 토큰은 보안을 위해 일정 시간(예: 30분) 후 만료됩니다.
