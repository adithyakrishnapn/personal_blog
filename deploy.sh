#!/usr/bin/env bash
# Fail fast on errors, unset vars, and pipefail for robust scripts
set -euo pipefail

# Configurable options (override with env vars if needed)
RUN_MIGRATIONS="${RUN_MIGRATIONS:-false}"  # set to "true" to run migrations on deploy
DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-project.settings}"
STATIC_ROOT="${STATIC_ROOT:-/app/static}"

echo "Starting deployment script..."

# 1) Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# 2) Collect static files (pre-deploy)
echo "Collecting static files (collectstatic) ..."
python manage.py collectstatic --noinput

# 3) Optional: Apply database migrations
if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Applying database migrations..."
  # Ensure the correct settings module is used
  export DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE"
  python manage.py migrate --noinput
else
  echo "Skipping migrations (RUN_MIGRATIONS=$RUN_MIGRATIONS)."
fi

echo "Deployment steps completed successfully."