#!/bin/bash
set -e

# Default to a generic user/password if not provided in environment variables
TTYD_USER=${TTYD_USER:-admin}
TTYD_PASSWORD=${TTYD_PASSWORD:-password123}

echo "Starting ttyd on port 7681 with Basic Auth..."
echo "Access URL: http://localhost:7681"
echo "Login with username: ${TTYD_USER}"

# Start ttyd with Basic Auth (-c)
ttyd -p 7681 -c "${TTYD_USER}:${TTYD_PASSWORD}" bash
