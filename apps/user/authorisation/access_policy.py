from rest_access_policy import AccessPolicy


class UserAccessPolicy(AccessPolicy):
    statements = [{"action": ["create", "confirm_email"], "principal": "anonymous", "effect": "allow"}]
