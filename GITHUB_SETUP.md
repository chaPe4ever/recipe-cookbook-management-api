# GitHub Actions Setup for Recipe Cookbook Manager API

Same multi-domain pattern as motion-api: host nginx on the droplet, one server block per domain, SSL via Let's Encrypt.

## One-Time Server Setup (required for SSL)

On the server, allow the deploy to run the nginx setup script without a password:

```bash
sudo visudo
```

Add (use the path that matches your `PROJECT_DIR` secret; `*` is required):

```
runner ALL=(ALL) NOPASSWD: /bin/bash /home/runner/recipe-api/scripts/setup-host-nginx-auto.sh *
```

Replace `runner` with your `SERVER_USER` and the path with your actual project directory.

## GitHub Secrets

| Secret | Description | Example |
|--------|-------------|---------|
| `SERVER_USER` | SSH user on server | `runner` |
| `SERVER_HOST` | Server IP or hostname | `165.227.158.51` |
| `PROJECT_DIR` | Deploy directory on server | `/home/runner/recipe-api` |
| `SSH_PRIVATE_KEY` | Private key for SSH | contents of `~/.ssh/id_ed25519_github` |
| `SECRET_KEY` | Django SECRET_KEY | `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `ALLOWED_HOSTS` | Your API domain | `recipe-api.domain.com` |
| `POSTGRES_DB` | PostgreSQL database name | `recipe_api_db` |
| `POSTGRES_USER` | PostgreSQL user | `recipe_api_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | (strong password) |

Use a **different domain** and **different `PROJECT_DIR`** from plannr and motion-api if they run on the same droplet. Backend is exposed on **port 8002** (motion-api uses 8001, plannr uses 8080).

## After Setup

1. Point your domain’s DNS A record to the server IP.
2. Push to `main` or `master` to trigger build and deploy.
3. First run: host nginx is configured (HTTP), certbot obtains the certificate, then HTTPS is enabled.
4. API: `https://<your-domain>/`, Swagger: `https://<your-domain>/swagger/`, ReDoc: `https://<your-domain>/redoc/`.
