import logging
from typing import Callable, Any, List

from fastapi import Depends, HTTPException, status, Request
from ..utils.okta_auth import get_okta_user

logger = logging.getLogger(__name__)

class AgentSecurity:
    """
    Implements the blueprint for a secure agentic enterprise:
    1. Visibility (Where are my agents?)
    2. Connection Control (What can they connect to?)
    3. Runtime Enforcement (What can they do?)
    """

    @staticmethod
    def require_roles(required_roles: List[str]):
        """
        Dependency factory to secure endpoints with specific role requirements.
        """
        async def verify_agent_action(request: Request, user: dict = Depends(get_okta_user)):
            # 1. Visibility: Log the agent's attempt to connect
            agent_id = user.get("agent_id") or user.get("sub", "unknown_entity")
            client_host = request.client.host if request.client else "unknown_host"

            logger.info(f"[AGENT SECURITY] Visibility: Entity '{agent_id}' from '{client_host}' is accessing '{request.url.path}'.")

            # 2. Connection Control: Ensure the agent has the basic required roles
            roles = user.get("roles", [])
            has_required_role = False
            for role in required_roles:
                if role in roles:
                    has_required_role = True
                    break

            # Allow local dev agent in testing
            if "local_dev_agent" in agent_id:
                has_required_role = True

            if not has_required_role:
                logger.warning(f"[AGENT SECURITY] Connection Control Blocked: Entity '{agent_id}' lacks required roles {required_roles}.")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions to connect. Required roles: {required_roles}"
                )

            logger.info(f"[AGENT SECURITY] Action Approved for '{agent_id}' on '{request.url.path}'.")
            return user

        return verify_agent_action
