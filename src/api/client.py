import requests
from typing import List
from src.api.models import Project

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.jwt = None

    def login_with_api_token(self, api_token: str) -> str:
        """Authenticate using a general API token and save the JWT."""
        url = f"{self.base_url}/api/login"
        response = self.session.post(url, json={"api_token": api_token})
        
        if not response.ok:
            raise RuntimeError(f"Login failed: {response.status_code} - {response.text}")
            
        self.jwt = response.json().get("jwt")
        self.session.headers.update({"Authorization": self.jwt})
        return self.jwt

    def get_projects(self) -> List[Project]:
        """Get all projects for the user. Requires authentication."""
        if not self.jwt:
            raise ValueError("Not authenticated. Please call login_with_api_token() first.")
        
        url = f"{self.base_url}/api/projects"
        response = self.session.get(url)
        
        if not response.ok:
            raise RuntimeError(f"Failed to get projects: {response.status_code} - {response.text}")
            
        return [Project.from_dict(p) for p in response.json().get("data", [])]

    def get_project_users(self, project_id: str) -> list:
        """Get all users for a specific project. Requires authentication."""
        if not self.jwt:
            raise ValueError("Not authenticated. Please call login_with_api_token() first.")
            
        url = f"{self.base_url}/api/{project_id}/users"
        response = self.session.get(url)
        
        if not response.ok:
            raise RuntimeError(f"Failed to get users for project {project_id}: {response.status_code} - {response.text}")
            
        return response.json().get("data", [])

    def get_suites(self, project_id: str) -> list:
        """Get all suites for a specific project. Requires authentication."""
        if not self.jwt:
            raise ValueError("Not authenticated. Please call login_with_api_token() first.")
            
        url = f"{self.base_url}/api/{project_id}/suites"
        response = self.session.get(url)
        
        if not response.ok:
            raise RuntimeError(f"Failed to get suites for project {project_id}: {response.status_code} - {response.text}")
            
        return response.json().get("data", [])

    def get_projects_with_suites(self) -> List[Project]:
        """Get a list of projects that have at least one suite."""
        all_projects = self.get_projects()
        return [project for project in all_projects if self.get_suites(project.id)]

    def delete_project(self, project_id: str) -> None:
        """Delete a specific project by its ID. Requires authentication."""
        if not self.jwt:
            raise ValueError("Not authenticated. Please call login_with_api_token() first.")
            
        url = f"{self.base_url}/api/projects/{project_id}"
        response = self.session.delete(url)
        
        if not response.ok:
            raise RuntimeError(f"Failed to delete project {project_id}: {response.status_code} - {response.text}")
