# 데이터 모델: Redmine 프로젝트 관리

## 엔티티 정의

### 1. Project (프로젝트)
Redmine의 핵심 단위인 프로젝트 정보를 관리합니다.

| 필드 | 타입 | 필수 | 설명 |
| :--- | :--- | :--- | :--- |
| `id` | Integer | Y | 시스템 내부 ID |
| `name` | String | Y | 프로젝트 표시 이름 |
| `identifier` | String | Y | 프로젝트 식별자 (Slug) |
| `description` | String | N | 프로젝트 상세 설명 |
| `homepage` | String | N | 프로젝트 홈페이지 URL |
| `parent_id` | Integer | N | 상위 프로젝트 ID (계층 구조) |
| `status` | Integer | Y | 상태 (1: Active, 5: Closed, 9: Archived) |
| `is_public` | Boolean | Y | 공개 여부 |
| `created_on` | DateTime | Y | 생성일시 |
| `updated_on` | DateTime | Y | 수정일시 |

### 2. Member (프로젝트 멤버)
특정 프로젝트에 할당된 사용자 정보입니다.

| 필드 | 타입 | 설명 |
| :--- | :--- | :--- |
| `id` | Integer | 멤버십 고유 ID |
| `user_id` | Integer | 사용자 ID |
| `user_name` | String | 사용자 실명 또는 로그인 ID |
| `roles` | List[Role] | 사용자에게 부여된 역할 목록 |

### 3. Role (역할)
프로젝트 내에서의 권한 그룹입니다.

| 필드 | 타입 | 설명 |
| :--- | :--- | :--- |
| `id` | Integer | 역할 고유 ID |
| `name` | String | 역할 이름 (예: Manager, Developer) |

## 관계 및 제약 사항
- **계층 구조**: `Project.parent_id`를 통해 트리 구조를 형성합니다. 상위 프로젝트 삭제 시 하위 프로젝트에 대한 처리 로직은 Redmine API 정책을 따릅니다.
- **2단계 승인 상태**: 생성/수정 요청 시 발급되는 `approval_token`은 서버 메모리 내에서 `Project` 생성/수정 페이로드와 매핑되어 유지됩니다.
