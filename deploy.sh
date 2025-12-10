#!/usr/bin/env bash
# Fail fast on errors, unset vars, and pipefail for robust scripts
set -euo pipefail

# Configurable options (override with env vars if needed)
RUN_MIGRATIONS="${RUN_MIGRATIONS:-false}"  # set to "true" to run migrations on deploy
DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-personalBlog.settings}"  # replace with your actual settings module
STATIC_ROOT="${STATIC_ROOT:-/app/static}"

echo "Starting deployment script..."

# 0) Export Django settings module
export DJANGO_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE"

# 1) Upgrade pip and setuptools (fixes distutils missing issue on Python 3.13)
echo "Upgrading pip and setuptools..."
pip install --upgrade pip setuptools

# 2) Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# 3) Collect static files
echo "Collecting static files (collectstatic) ..."
python manage.py collectstatic --noinput

# 4) Optional: Apply database migrations
if [ "$RUN_MIGRATIONS" = "true" ]; then
  echo "Applying database migrations..."
  python manage.py migrate --noinput
else
  echo "Skipping migrations (RUN_MIGRATIONS=$RUN_MIGRATIONS)."
fi

echo "Deployment steps completed successfully."
