#!/bin/bash
set -e

# Deployment script for recipe-cookbook-manager-api production
# This script handles the complete deployment process with automatic SSL

# PROJECT_DIR can be set manually via CI/CD variables
if [ -z "$PROJECT_DIR" ]; then
  if [ -n "$CI_PROJECT_PATH_SLUG" ]; then
    PROJECT_DIR="/home/gitlab-runner/projects/$CI_PROJECT_PATH_SLUG"
  elif [ -n "$GITHUB_REPOSITORY" ]; then
    PROJECT_DIR="/home/github-runner/app"
  else
    PROJECT_DIR="/home/gitlab-runner/app"
  fi
fi

# Extract domain from ALLOWED_HOSTS
DOMAIN="${ALLOWED_HOSTS%% *}"
DOMAIN="${DOMAIN#http://}"
DOMAIN="${DOMAIN#https://}"
DOMAIN="${DOMAIN%%/*}"
DOMAIN="${DOMAIN%%:*}"
DOMAIN="${DOMAIN%% *}"

# Clean ALLOWED_HOSTS for Django
CLEAN_ALLOWED_HOSTS="${ALLOWED_HOSTS}"
CLEAN_ALLOWED_HOSTS="${CLEAN_ALLOWED_HOSTS#http://}"
CLEAN_ALLOWED_HOSTS="${CLEAN_ALLOWED_HOSTS#https://}"
CLEAN_ALLOWED_HOSTS="${CLEAN_ALLOWED_HOSTS%%/*}"
CLEAN_ALLOWED_HOSTS="${CLEAN_ALLOWED_HOSTS%%:*}"
CLEAN_ALLOWED_HOSTS="${CLEAN_ALLOWED_HOSTS%% *}"
export ALLOWED_HOSTS="$CLEAN_ALLOWED_HOSTS"

echo "🚀 Starting recipe-api deployment..."
echo "📂 Project directory: $PROJECT_DIR"
echo "🌐 Domain: $DOMAIN"

# Export environment variables
export POSTGRES_DB="${POSTGRES_DB}"
export POSTGRES_USER="${POSTGRES_USER}"
export POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"
export BACKEND_IMAGE="${BACKEND_IMAGE}"
export SECRET_KEY="${SECRET_KEY}"
export ALLOWED_HOSTS="${ALLOWED_HOSTS}"

# Determine SSL email
if [ -n "$DEFAULT_FROM_EMAIL" ]; then
  SSL_EMAIL="$DEFAULT_FROM_EMAIL"
elif [ -n "$EMAIL_HOST_USER" ] && [[ "$EMAIL_HOST_USER" =~ @ ]]; then
  SSL_EMAIL="$EMAIL_HOST_USER"
elif [ -n "$SSL_EMAIL" ]; then
  SSL_EMAIL="$SSL_EMAIL"
else
  SSL_EMAIL="admin@${DOMAIN}"
fi

SSL_EMAIL="${SSL_EMAIL#http://}"
SSL_EMAIL="${SSL_EMAIL#https://}"
SSL_EMAIL="${SSL_EMAIL%%/*}"
if [[ "$SSL_EMAIL" =~ @ ]]; then
  EMAIL_USER="${SSL_EMAIL%%@*}"
  EMAIL_DOMAIN="${SSL_EMAIL#*@}"
  EMAIL_DOMAIN="${EMAIL_DOMAIN#http://}"
  EMAIL_DOMAIN="${EMAIL_DOMAIN#https://}"
  EMAIL_DOMAIN="${EMAIL_DOMAIN%%/*}"
  EMAIL_DOMAIN="${EMAIL_DOMAIN%%:*}"
  SSL_EMAIL="${EMAIL_USER}@${EMAIL_DOMAIN}"
else
  SSL_EMAIL="${SSL_EMAIL%%:*}"
  SSL_EMAIL="admin@${SSL_EMAIL}"
fi
export SSL_EMAIL
echo "📧 SSL Email: $SSL_EMAIL"

# Change to project directory
ORIGINAL_DIR=$(pwd)
cd $PROJECT_DIR

# Check if SSL certificates exist
SSL_CERTS_EXIST=false
CERTBOT_VOLUMES=$(docker volume ls --format "{{.Name}}" | grep -i certbot || true)

echo "🔍 Checking for SSL certificates..."
if docker compose -f docker-compose.prod.yml run --rm --no-deps certbot ls /etc/letsencrypt/live/$DOMAIN/fullchain.pem > /dev/null 2>&1; then
  SSL_CERTS_EXIST=true
  echo "✅ SSL certificates detected via docker compose"
else
  if [ -n "$CERTBOT_VOLUMES" ]; then
    for vol in $CERTBOT_VOLUMES; do
      if docker run --rm -v "$vol:/certs:ro" alpine ls /certs/live/$DOMAIN/fullchain.pem > /dev/null 2>&1; then
        SSL_CERTS_EXIST=true
        echo "✅ SSL certificates detected in volume '$vol'"
        break
      fi
    done
  fi

  if [ "$SSL_CERTS_EXIST" = false ]; then
    echo "⚠️  SSL certificates not detected - will attempt automatic setup"
  fi
fi

# Set up host-level nginx FIRST (so port 80 is configured and certbot webroot can be served)
echo "🔧 Setting up host-level nginx (required for SSL and routing)..."
cd "$PROJECT_DIR"

if [ -f "scripts/setup-host-nginx-auto.sh" ] && [ -d "nginx/sites-available" ]; then
  export COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-recipe-api}"
  sudo /bin/bash "$PROJECT_DIR/scripts/setup-host-nginx-auto.sh" "$PROJECT_DIR" "$ALLOWED_HOSTS" "${COMPOSE_PROJECT_NAME:-recipe-api}" || {
    echo "⚠️  Host nginx setup failed."
    echo "   On the server, add NOPASSWD for the setup script. See GITHUB_SETUP.md → Server sudoers for SSL."
  }
else
  echo "⚠️  setup-host-nginx-auto.sh or nginx templates not found"
fi

# Check SSL certificates status and handle setup/renewal (after host nginx is up)
echo "🔒 Checking SSL certificates..."
if [ "$SSL_CERTS_EXIST" = true ]; then
  echo "✅ SSL certificates found for $DOMAIN - renewing if needed..."
  docker compose -f docker-compose.prod.yml run --rm certbot renew --quiet 2>/dev/null || true
else
  echo "⚠️  SSL certificates not found for $DOMAIN"
  echo "🔐 Attempting automatic SSL certificate setup (webroot via host nginx)..."

  if [[ ! "$SSL_EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "⚠️  Invalid email format: $SSL_EMAIL"
    SSL_EMAIL="admin@${DOMAIN}"
    export SSL_EMAIL
  fi

  if docker compose -f docker-compose.prod.yml run --rm -v /var/www/html:/var/www/certbot certbot certonly --webroot \
    -w /var/www/certbot \
    -d "$DOMAIN" \
    --email "$SSL_EMAIL" \
    --agree-tos \
    --non-interactive 2>&1; then
    echo "✅ SSL certificate obtained successfully!"
    SSL_CERTS_EXIST=true
    sudo /bin/bash "$PROJECT_DIR/scripts/setup-host-nginx-auto.sh" "$PROJECT_DIR" "$ALLOWED_HOSTS" "${COMPOSE_PROJECT_NAME:-recipe-api}" || true
  else
    echo "⚠️  SSL certificate setup failed or skipped"
    echo "   Ensure host nginx is set up and port 80 is open."
  fi
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
export POSTGRES_DB POSTGRES_USER POSTGRES_PASSWORD BACKEND_IMAGE SECRET_KEY ALLOWED_HOSTS
docker compose -f docker-compose.prod.yml down --remove-orphans || true

# Pull latest images
echo "📥 Pulling latest images..."
docker pull $BACKEND_IMAGE || echo "⚠️  Failed to pull image, will use existing"

# Start services
echo "🚀 Starting services..."
if [ -z "$BACKEND_IMAGE" ]; then
  echo "❌ ERROR: BACKEND_IMAGE not set!"
  exit 1
fi

docker compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Run migrations
echo "🔄 Running database migrations..."
docker compose -f docker-compose.prod.yml exec -T backend python manage.py migrate --noinput || {
  echo "⚠️  Migrations failed, but continuing..."
}

# Ensure staticfiles is writable by app user
echo "📂 Fixing staticfiles permissions..."
docker compose -f docker-compose.prod.yml run --rm -u root backend chown -R 1000:1000 /app/staticfiles 2>/dev/null || true

# Collect static files
echo "📦 Collecting static files..."
docker compose -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput || {
  echo "⚠️  Static file collection failed, but continuing..."
}

echo "✅ Deployment completed!"
echo "🌐 Application should be available at: https://$DOMAIN"
