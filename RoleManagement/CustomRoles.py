from RoleManagement.RoleGroup import RoleGroup


class CustomRoles(RoleGroup):
    """
    All variables are type RoleWrapper at runtime, excepting _roles, which is how they are assigned at runtime
    _roles follows the format "Name in class": "Name that discord can find"
    """
    _roles = {
        "top": "Top"
    }
    top = None