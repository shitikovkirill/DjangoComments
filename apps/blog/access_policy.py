from rest_access_policy import AccessPolicy


class PostAccessPolicy(AccessPolicy):
    statements = [
        {"action": ["list", "retrieve"], "principal": "*", "effect": "allow"},
        {
            "action": ["create"],
            "principal": "authenticated",
            "effect": "allow",
        },
    ]
