from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class ProjectAttributes:
    title: str
    lang: Optional[str] = None
    framework: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    tests_count: Optional[int] = None
    environments: List[str] = field(default_factory=list)
    url: Optional[str] = None
    testomatio_url: Optional[str] = None
    demo: Optional[bool] = None
    # raw_data catches all other attributes that are not explicitly defined above
    raw_data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> 'ProjectAttributes':
        if not data:
            data = {}
        return cls(
            title=data.get("title", ""),
            lang=data.get("lang"),
            framework=data.get("framework"),
            status=data.get("status"),
            created_at=data.get("created-at"),
            tests_count=data.get("tests-count"),
            environments=data.get("environments") or [],
            url=data.get("url"),
            testomatio_url=data.get("testomatio-url"),
            demo=data.get("demo"),
            raw_data=data
        )

@dataclass
class Project:
    id: str
    type: str
    attributes: ProjectAttributes
    relationships: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> 'Project':
        return cls(
            id=data.get("id", ""),
            type=data.get("type", "project"),
            attributes=ProjectAttributes.from_dict(data.get("attributes", {})),
            relationships=data.get("relationships", {})
        )

@dataclass
class ProjectsResponse:
    data: List[Project]

    @classmethod
    def from_dict(cls, data: dict) -> 'ProjectsResponse':
        return cls(
            data=[Project.from_dict(p) for p in data.get("data", [])]
        )
