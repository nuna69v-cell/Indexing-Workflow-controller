import logging
import os
import time
from typing import Optional
from urllib.request import Request, urlopen
import json

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

try:
    from jose import JWTError, jwt
except Exception:
    JWTError = Exception
    jwt = None

from ..config import settings

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

# Simple cache for JWKS to avoid fetching on every request
_jwks_cache = {}
_jwks_cache_time = 0
JWKS_CACHE_TTL = 3600  # 1 hour


def get_okta_jwks():
    """Fetches the JWKS from Okta to verify JWT signatures."""
    global _jwks_cache, _jwks_cache_time

    if not settings.OKTA_DOMAIN:
        return None

    # Return cached keys if valid
    if _jwks_cache and (time.time() - _jwks_cache_time) < JWKS_CACHE_TTL:
        return _jwks_cache

    try:
        # The standard Okta default authorization server JWKS endpoint
        # E.g. https://{yourOktaDomain}/oauth2/default/v1/keys
        jwks_url = f"https://{settings.OKTA_DOMAIN}/oauth2/default/v1/keys"
        req = Request(jwks_url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=10) as response:
            jwks_data = json.loads(response.read().decode())
            _jwks_cache = jwks_data
            _jwks_cache_time = time.time()
            return jwks_data
    except Exception as e:
        logger.error(f"Failed to fetch Okta JWKS: {e}")
        return None


def get_okta_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> dict:
    """
    FastAPI dependency to verify an Okta access token and extract the user/agent context.

    This implements the foundational identity check for the secure agentic enterprise.
    """
    # For explicitly testing without Okta configured, return a mock agent
    # Ensure this doesn't fail open in production
    if os.getenv("TESTING"):
        return {
            "sub": "local_dev_agent",
            "agent_id": "test_agent_1",
            "roles": ["ai_agent_read", "ai_agent_write"],
        }

    if not settings.OKTA_DOMAIN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Okta authentication is required but OKTA_DOMAIN is not configured.",
        )

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (Okta token required)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if jwt is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT library not installed. Cannot verify Okta tokens.",
        )

    token = credentials.credentials
    jwks = get_okta_jwks()

    if not jwks:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve Okta public keys.",
        )

    try:
        # Extract the unverified header to get the key ID (kid)
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks.get("keys", []):
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
                break

        if not rsa_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to find appropriate key for token verification.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify the token
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=settings.OKTA_AUDIENCE,
            issuer=f"https://{settings.OKTA_DOMAIN}/oauth2/default",
        )

        return payload

    except JWTError as e:
        logger.warning(f"Okta JWT verification failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Unexpected error validating Okta token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during authentication.",
        )
