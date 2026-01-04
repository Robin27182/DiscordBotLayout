from typing import List

from DataClasses.UserConfig import UserConfig
from FileManager.FileInterpreterABC import FileInterpreterABC
import json
from RoleManagement.RoleGroup import RoleGroup
from RoleManagement.RoleWrapper import RoleWrapper


class UserConfigInterpreter(FileInterpreterABC):
    @property
    def extension(self) -> str:
        return ".json"

    def write(self, config: UserConfig) -> str:
        """
        Serialize a UserConfig instance into a JSON string.
        Stores only role names; reconstruction will handle RoleGroup lookup.
        """
        roles = config.roles or []

        # Map each role to its name via its RoleGroup
        role_names = []
        for role in roles:
            # Find the group that owns this role
            for group_cls in RoleGroup.__subclasses__():
                name = group_cls.get_name_by_role(role)
                if name:
                    role_names.append({"name": name})
                    break
            else:
                # Optional: warn or raise if a role cannot be mapped
                raise ValueError(f"Role '{role}' could not be mapped to any RoleGroup")

        data = {
            "username": config.username,
            "nickname": config.nickname,
            "roles": role_names
        }

        return json.dumps(data, indent=4)

    def _find_role_wrapper(self, role_name: str) -> RoleWrapper:
        for group_cls in RoleGroup.__subclasses__():
            existing = group_cls.get_role_by_name(role_name, give_error=False)
            if existing:
                # Return a new RoleWrapper tied to this UserConfig
                return RoleWrapper(group_cls, existing.raw, existing.name)
        raise ValueError(f"Role '{role_name}' not found in any RoleGroup")

    def read(self, file_contents: str) -> UserConfig:
        """
        Deserialize a JSON string into a UserConfig instance.
        Reconstructs RoleWrapper objects by looking up their corresponding RoleGroup subclasses.
        """
        raw = json.loads(file_contents)


        roles = [self._find_role_wrapper(r["name"]) for r in raw.get("roles", [])]

        return UserConfig(
            username=raw.get("username"),
            nickname=raw.get("nickname"),
            roles=roles
        )

