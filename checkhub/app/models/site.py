from typing import List, Optional
from pydantic import BaseModel


class Account(BaseModel):
    username: str
    password: str
    enabled: bool = True
    cookies: Optional[str] = None
    extra_data: Optional[dict] = None


class Site(BaseModel):
    id: str
    name: str
    enabled: bool = True
    checker_class: str
    accounts: List[Account] = []
    config: Optional[dict] = None
    
    @classmethod
    def from_config(cls, site_id: str, config: dict):
        accounts = [Account(**acc) for acc in config.get("accounts", [])]
        return cls(
            id=site_id,
            name=config.get("name", site_id),
            enabled=config.get("enabled", True),
            checker_class=config.get("checker_class", "BaseChecker"),
            accounts=accounts,
            config=config.get("config", {})
        )
