#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-fit-zfjw-api}"
INSTALL_DIR="${INSTALL_DIR:-/opt/fit-zfjw-api}"
REPO_URL="${REPO_URL:-https://github.com/Lecheeel/fit-zfjw-api.git}"
BRANCH="${BRANCH:-main}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-49031}"
BASE_URL="${BASE_URL:-http://oaa.fitedu.net/jwglxt}"
START_DATE="${START_DATE:-2026-03-04}"
RUN_USER="${RUN_USER:-fitapi}"
ENV_FILE="${INSTALL_DIR}/fit-api.env"
VENV_DIR="${INSTALL_DIR}/.venv"

if [ "$(id -u)" -ne 0 ]; then
  echo "Please run this script as root, for example: curl -fsSL <url> | sudo bash" >&2
  exit 1
fi

if [ -r /etc/os-release ]; then
  . /etc/os-release
else
  echo "Cannot read /etc/os-release." >&2
  exit 1
fi

if [ "${ID:-}" != "debian" ] || [ "${VERSION_ID:-}" != "13" ]; then
  echo "This installer currently supports Debian 13 only. Detected: ${PRETTY_NAME:-unknown}" >&2
  exit 1
fi

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
  ca-certificates \
  curl \
  git \
  python3 \
  python3-pip \
  python3-venv \
  build-essential \
  libgl1 \
  libglib2.0-0

if ! id -u "${RUN_USER}" >/dev/null 2>&1; then
  useradd --system --home "${INSTALL_DIR}" --shell /usr/sbin/nologin "${RUN_USER}"
fi

if [ -d "${INSTALL_DIR}/.git" ]; then
  git -C "${INSTALL_DIR}" fetch --depth 1 origin "${BRANCH}"
  git -C "${INSTALL_DIR}" checkout "${BRANCH}"
  git -C "${INSTALL_DIR}" reset --hard "origin/${BRANCH}"
elif [ -d "${INSTALL_DIR}" ] && [ -n "$(find "${INSTALL_DIR}" -mindepth 1 -maxdepth 1 -print -quit)" ]; then
  echo "Install directory exists and is not a git repository: ${INSTALL_DIR}" >&2
  echo "Move it away or choose another INSTALL_DIR." >&2
  exit 1
else
  git clone --depth 1 --branch "${BRANCH}" "${REPO_URL}" "${INSTALL_DIR}"
fi

python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/python" -m pip install --upgrade pip setuptools wheel
"${VENV_DIR}/bin/python" -m pip install -e "${INSTALL_DIR}[server]"

mkdir -p "${INSTALL_DIR}/data"

if [ ! -f "${ENV_FILE}" ]; then
  cat > "${ENV_FILE}" <<EOF
FIT_API_HOST=${HOST}
FIT_API_PORT=${PORT}
FIT_API_BASE_URL=${BASE_URL}
FIT_API_START_DATE=${START_DATE}
FIT_API_DATA_DIR=${INSTALL_DIR}/data
EOF
fi

chown -R "${RUN_USER}:${RUN_USER}" "${INSTALL_DIR}"

cat > "/etc/systemd/system/${SERVICE_NAME}.service" <<EOF
[Unit]
Description=FIT ZFJW API
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${RUN_USER}
Group=${RUN_USER}
WorkingDirectory=${INSTALL_DIR}
EnvironmentFile=${ENV_FILE}
ExecStart=${VENV_DIR}/bin/python ${INSTALL_DIR}/course_server.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now "${SERVICE_NAME}.service"
systemctl restart "${SERVICE_NAME}.service"

echo "FIT ZFJW API has been installed."
echo "Service: ${SERVICE_NAME}.service"
echo "Config: ${ENV_FILE}"
echo "URL: http://${HOST}:${PORT}"
