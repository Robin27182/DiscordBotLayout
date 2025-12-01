from dataclasses import dataclass
from typing import List

from RoleManagement.RoleWrapper import RoleWrapper


@dataclass
class UserConfig:
    username: str
    nickname: str
    roles: List[RoleWrapper]