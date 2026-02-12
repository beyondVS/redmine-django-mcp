from typing import Optional
from redmine_django_mcp.server import mcp
from redmine_django_mcp.services.approval import approval_service
from redmine_django_mcp.services.redmine_api import RedmineApiClient

async def request_project_create_impl(
    mcp_token: str,
    name: str,
    identifier: str,
    description: Optional[str] = None,
    homepage: Optional[str] = None,
    parent_id: Optional[int] = None,
    is_public: bool = True
) -> str:
    """프로젝트 생성 요청의 실제 구현 로직"""
    payload = {
        "mcp_token": mcp_token,
        "name": name,
        "identifier": identifier,
        "description": description,
        "homepage": homepage,
        "parent_id": parent_id,
        "is_public": is_public
    }
    token = approval_service.create_request("create_project", payload)
    return (
        "프로젝트 생성 요청이 접수되었습니다.\n"
        "- 이름: {}\n"
        "- 식별자: {}\n\n"
        "위 변경 사항을 적용하려면 다음 도구를 호출하십시오:\n"
        "approve_action(approval_token='{}')"
    ).format(name, identifier, token)

@mcp.tool()
async def request_project_create(
    mcp_token: str,
    name: str,
    identifier: str,
    description: Optional[str] = None,
    homepage: Optional[str] = None,
    parent_id: Optional[int] = None,
    is_public: bool = True
) -> str:
    """새로운 프로젝트 생성을 요청합니다. 승인 토큰을 발급합니다."""
    return await request_project_create_impl(mcp_token, name, identifier, description, homepage, parent_id, is_public)

async def request_project_update_impl(
    mcp_token: str,
    identifier: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    homepage: Optional[str] = None,
    parent_id: Optional[int] = None,
    is_public: Optional[bool] = None
) -> str:
    """프로젝트 수정 요청의 실제 구현 로직"""
    update_data = {}
    if name is not None: update_data["name"] = name
    if description is not None: update_data["description"] = description
    if homepage is not None: update_data["homepage"] = homepage
    if parent_id is not None: update_data["parent_id"] = parent_id
    if is_public is not None: update_data["is_public"] = is_public
    
    payload = {
        "mcp_token": mcp_token,
        "identifier": identifier,
        "update_data": update_data
    }
    token = approval_service.create_request("update_project", payload)
    return (
        "프로젝트 수정 요청이 접수되었습니다. (식별자: {})\n"
        "- 수정 예정 항목: {}\n\n"
        "위 변경 사항을 적용하려면 다음 도구를 호출하십시오:\n"
        "approve_action(approval_token='{}')"
    ).format(identifier, ", ".join(update_data.keys()), token)

@mcp.tool()
async def request_project_update(
    mcp_token: str,
    identifier: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    homepage: Optional[str] = None,
    parent_id: Optional[int] = None,
    is_public: Optional[bool] = None
) -> str:
    """기존 프로젝트 정보 수정을 요청합니다. 승인 토큰을 발급합니다."""
    return await request_project_update_impl(mcp_token, identifier, name, description, homepage, parent_id, is_public)

async def approve_action_impl(approval_token: str) -> str:
    """승인 실행의 실제 구현 로직"""
    request = approval_service.consume_request(approval_token)
    if not request:
        return "유효하지 않거나 만료된 승인 토큰입니다."
    action_type = request["action_type"]
    payload = request["payload"]
    mcp_token = payload["mcp_token"]
    try:
        client = RedmineApiClient(mcp_token)
        if action_type == "create_project":
            create_data = {k: v for k, v in payload.items() if k != "mcp_token"}
            result = await client.create_project(create_data)
            p = result.get("project", {})
            return "프로젝트가 성공적으로 생성되었습니다. (ID: {}, 식별자: {})".format(
                p.get("id"), p.get("identifier")
            )
        elif action_type == "update_project":
            identifier = payload["identifier"]
            update_data = payload["update_data"]
            await client.update_project(identifier, update_data)
            return "프로젝트 정보가 성공적으로 수정되었습니다. (식별자: {})".format(identifier)
        return "알 수 없는 작업 유형입니다."
    except Exception as e:
        return "작업 실행 실패: {}".format(str(e))

@mcp.tool()
async def approve_action(approval_token: str) -> str:
    """발급받은 승인 토큰을 사용하여 요청된 작업을 최종 실행합니다."""
    return await approve_action_impl(approval_token)
