import httpx
from typing import Dict, Any, Optional
from src.redmine_django_mcp.services.auth import auth_service

class RedmineApiClient:
    BASE_URL = "http://localhost:8000"

    def __init__(self, mcp_token: str):
        self.api_key = auth_service.get_redmine_key(mcp_token)
        if not self.api_key:
            raise ValueError("Invalid or expired MCP token")
        
        self.headers = {
            "X-Redmine-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.BASE_URL) as client:
            response = await client.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.BASE_URL) as client:
            response = await client.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()

    async def put(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.BASE_URL) as client:
            response = await client.put(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()

    async def list_projects(self, status: Optional[str] = "active", offset: int = 0, limit: int = 25) -> Dict[str, Any]:
        params = {
            "status": status,
            "offset": offset,
            "limit": limit
        }
        return await self.get("/projects.json", params=params)

    async def get_project(self, identifier: str) -> Dict[str, Any]:
        return await self.get("/projects/{}.json".format(identifier), params={"include": "parent,subprojects"})


