from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

# Import Stream Service
from api.services.stream_service import stream_service

# For agent security (RBAC / Okta)
try:
    from api.middleware.agent_security import AgentSecurity

    require_roles = AgentSecurity.require_roles
except ImportError:
    # Fallback mock for testing if security modules aren't fully configured
    def require_roles(roles):
        def _mock_dependency():
            return {"sub": "mock-user"}

        return _mock_dependency


router = APIRouter(prefix="/stream", tags=["stream", "social", "chat"])


class StreamTokenRequest(BaseModel):
    user_id: str
    username: Optional[str] = None
    image_url: Optional[str] = None


class StreamTokenResponse(BaseModel):
    chat_token: str
    feed_token: str
    user_id: str


@router.on_event("startup")
async def startup_event():
    """Initialize Stream connections on startup"""
    stream_service.initialize()


@router.post("/token", response_model=StreamTokenResponse)
async def generate_stream_tokens(
    request: StreamTokenRequest,
    current_user: dict = Depends(require_roles(["trader", "admin", "agent"])),
):
    """
    Generate authentication tokens for Stream Chat and Feeds.
    Requires an authenticated user session (verified by Okta/JWT).
    """
    user_id = request.user_id

    # Optionally upsert user data in Stream Chat to keep profiles in sync
    if request.username:
        user_data = {"name": request.username}
        if request.image_url:
            user_data["image"] = request.image_url

        stream_service.upsert_user(user_id, user_data)

    chat_token = stream_service.generate_chat_token(user_id)
    feed_token = stream_service.generate_feed_token(user_id)

    if not chat_token or not feed_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate Stream tokens. Check API configuration.",
        )

    return StreamTokenResponse(
        chat_token=chat_token, feed_token=feed_token, user_id=user_id
    )


@router.get("/status")
async def get_stream_status():
    """Check the health status of Stream Integrations"""
    chat_initialized = stream_service.chat_client is not None
    feed_initialized = stream_service.feed_client is not None

    return {
        "chat_enabled": chat_initialized,
        "feed_enabled": feed_initialized,
        "status": (
            "connected" if chat_initialized and feed_initialized else "disconnected"
        ),
    }
