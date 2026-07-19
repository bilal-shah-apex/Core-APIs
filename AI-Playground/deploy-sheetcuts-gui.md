# Deploying the SheetCuts GUI to Your Own Website/Domain

This document outlines the main steps required to deploy the `01-Area-Partition/gui` FastAPI-based frontend/backend wrapper onto a host and map it to a domain you own.

## 1. Decide your hosting model

Choose one of these common hosting options:

- **Virtual Private Server (VPS)**: e.g. DigitalOcean, Linode, AWS EC2, Google Compute Engine
- **Managed App Platform**: e.g. Render, Railway, Azure App Service, Fly.io
- **Container-based hosting**: Docker on a VPS or a container service like Amazon ECS, Azure Container Apps, or Docker Hub + a server

For a small test deployment, a single Linux VPS is the simplest and most flexible.

## 2. Prerequisites

- A registered domain name
- Control of DNS for that domain
- A host machine or service with a public IP
- Python 3.14 installed on the host
- Git access to the repository (or a ZIP upload of the code)
- A TLS/HTTPS certificate (Let’s Encrypt is recommended)
- Optionally: Docker, nginx, certbot, and a process manager (`systemd` or supervisor)

## 3. Prepare the app on the server

### 3.1 Clone the repo

```bash
cd /opt
git clone <your-repo-url> sheetcuts-api
cd sheetcuts-api/01-Area-Partition
```

### 3.2 Create a Python environment

```bash
python3.14 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn
```

### 3.3 Optionally install dependencies

The core package has no runtime dependencies in `requirements.txt`, so for the GUI wrapper you only need the FastAPI stack.

### 3.4 Check the app locally

```bash
uvicorn gui.app:app --host 0.0.0.0 --port 8000
```

Then open `http://<server-ip>:8000` to verify it loads.

## 4. Configure the domain DNS

- Add an `A` record for `example.com` pointing to your server IP
- Optionally add a `CNAME` for `www.example.com` pointing to `example.com`

DNS changes may take a few minutes to propagate.

## 5. Set up a production server process

For a stable deployment, do not run `uvicorn --reload` in production. Use an app server and optionally a process manager.

### Option A: Use `uvicorn` directly with `systemd`

Create a service file like `/etc/systemd/system/sheetcuts-gui.service`:

```ini
[Unit]
Description=SheetCuts GUI service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/sheetcuts-api/01-Area-Partition
Environment="PATH=/opt/sheetcuts-api/01-Area-Partition/venv/bin"
ExecStart=/opt/sheetcuts-api/01-Area-Partition/venv/bin/uvicorn gui.app:app --host 127.0.0.1 --port 8000

[Install]
WantedBy=multi-user.target
```

Then enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable sheetcuts-gui
sudo systemctl start sheetcuts-gui
```

### Option B: Use `gunicorn` with Uvicorn workers

Install:

```bash
pip install gunicorn uvicorn
```

Start with:

```bash
gunicorn -k uvicorn.workers.UvicornWorker gui.app:app --bind 127.0.0.1:8000 --workers 3
```

## 6. Add a reverse proxy and HTTPS

### 6.1 Install nginx

```bash
sudo apt update
sudo apt install nginx
```

### 6.2 Configure nginx for the domain

Create a site file like `/etc/nginx/sites-available/sheetcuts`:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable it and restart nginx:

```bash
sudo ln -s /etc/nginx/sites-available/sheetcuts /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6.3 Enable HTTPS with Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d example.com -d www.example.com
```

Certbot will update nginx and install trusted TLS certificates.

## 7. Test the deployed site

- Visit `https://example.com`
- Verify the GUI loads
- Submit a sample request and ensure the JSON response + diagram appear

## 8. Optional improvements

- Add a `requirements.txt` for the GUI wrapper or a `gui/requirements.txt`
- Use Docker to containerize the app
- Add a continuous deployment pipeline (GitHub Actions, GitLab CI, etc.)
- Set up monitoring and logs for the `uvicorn`/`gunicorn` process
- Add authentication if you want restricted access

## 9. Notes specific to this repo

- The web wrapper lives at `01-Area-Partition/gui/app.py`
- Static assets are in `01-Area-Partition/gui/static/`
- The backend core remains in `01-Area-Partition/sheetcuts/`
- The site is ready for manual testing and can later be turned into a production REST API

## Recommended next step

If you want, I can also create a `Dockerfile` and a `gui/requirements.txt` so deployment becomes even easier and more portable.
