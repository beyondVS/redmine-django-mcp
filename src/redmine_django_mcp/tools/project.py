from typing import Optional
from redmine_django_mcp.server import mcp
from redmine_django_mcp.services.redmine_api import RedmineApiClient

async def list_projects_impl(
    mcp_token: str,
    status: Optional[str] = "active",
    offset: int = 0,
    limit: int = 25
) -> str:
    """프로젝트 목록 조회의 실제 구현 로직"""
    try:
        client = RedmineApiClient(mcp_token)
        result = await client.list_projects(status=status, offset=offset, limit=limit)
        
        projects = result.get("projects", [])
        total = result.get("total_count", 0)
        
        if not projects:
            return "조회된 프로젝트가 없습니다."
            
        header = "총 {}개의 프로젝트 중 {}개를 조회했습니다.\n".format(total, len(projects))
        summary = [header]
        for p in projects:
            line = "- {} (ID: {}, 식별자: {}, 상태: {})".format(
                p.get('name'), p.get('id'), p.get('identifier'), p.get('status', 'N/A')
            )
            summary.append(line)
            
        if total > offset + limit:
            summary.append("\n* 다음 페이지가 존재합니다. (offset={}으로 다시 조회 가능)".format(offset + limit))
            
        return "\n".join(summary)
    except Exception as e:
        return "프로젝트 목록 조회 실패: {}".format(str(e))

async def get_project_details_impl(
    mcp_token: str,
    identifier: str
) -> str:
    """프로젝트 상세 조회의 실제 구현 로직"""
    try:
        client = RedmineApiClient(mcp_token)
        result = await client.get_project(identifier)
        
        p = result.get("project")
        if not p:
            return "프로젝트 정보를 찾을 수 없습니다."
            
        details = [
            "프로젝트 상세 정보:",
            "- 이름: {}".format(p.get("name")),
            "- 식별자: {}".format(p.get("identifier")),
            "- 설명: {}".format(p.get("description", "없음")),
            "- 홈페이지: {}".format(p.get("homepage", "없음")),
            "- 상태: {}".format(p.get("status")),
            "- 공개 여부: {}".format("예" if p.get("is_public") else "아니오")
        ]
        
        # 계층 구조
        parent = p.get("parent")
        if parent:
            details.append("- 상위 프로젝트: {} (ID: {})".format(parent.get("name"), parent.get("id")))
            
        subprojects = p.get("subprojects")
        if subprojects:
            sub_names = [s.get("name") for s in subprojects]
            details.append("- 하위 프로젝트: {}".format(", ".join(sub_names)))
            
        return "\n".join(details)
    except Exception as e:
        return "프로젝트 상세 조회 실패: {}".format(str(e))

async def list_project_members_impl(
    mcp_token: str,
    identifier: str,
    offset: int = 0,
    limit: int = 100
) -> str:
    """프로젝트 멤버 조회의 실제 구현 로직"""
    try:
        client = RedmineApiClient(mcp_token)
        result = await client.get_memberships(identifier, offset=offset, limit=limit)
        
        memberships = result.get("memberships", [])
        total = result.get("total_count", 0)
        
        if not memberships:
            return "프로젝트에 등록된 멤버가 없습니다."
            
        header = "프로젝트 멤버 목록 (총 {}명):\n".format(total)
        summary = [header]
        for m in memberships:
            user = m.get("user", {})
            roles = m.get("roles", [])
            role_names = [r.get("name") for r in roles]
            
            line = "- {} (ID: {}, 역할: {})".format(
                user.get("name"), user.get("id"), ", ".join(role_names)
            )
            summary.append(line)
            
        if total > offset + limit:
            summary.append("\n* 추가 멤버가 존재합니다. (offset={}으로 다시 조회 가능)".format(offset + limit))
            
        return "\n".join(summary)
    except Exception as e:
        return "멤버 목록 조회 실패: {}".format(str(e))

@mcp.tool()
async def list_project_members(
    mcp_token: str,
    identifier: str,
    offset: int = 0,
    limit: int = 100
) -> str:
    """
    특정 프로젝트에 참여 중인 멤버와 그들의 역할 목록을 조회합니다.
    """
    return await list_project_members_impl(mcp_token, identifier, offset, limit)

@mcp.tool()
async def get_project_details(
    mcp_token: str,
    identifier: str
) -> str:
    """
    특정 프로젝트의 상세 정보를 조회합니다. 식별자(Slug)를 사용합니다.
    """
    return await get_project_details_impl(mcp_token, identifier)

@mcp.tool()
async def list_projects(
    mcp_token: str,
    status: Optional[str] = "active",
    offset: int = 0,
    limit: int = 25
) -> str:
    """
    Redmine의 프로젝트 목록을 조회합니다.
    """
    return await list_projects_impl(mcp_token, status, offset, limit)
