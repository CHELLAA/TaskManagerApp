# Deployment Guide for TaskFlow

This guide covers multiple deployment options to make your TaskFlow app accessible to everyone.

---

## Option 1: Simple VPS/Cloud Server (Recommended for Production)

### 1.1 Server Setup

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Python, pip, and nginx
apt install -y python3 python3-pip nginx

# Install dependencies
cd /opt/taskflow
pip3 install -r requirements.txt

# Create systemd service
cat > /etc/systemd/system/taskflow.service << EOF
[Unit]
Description=TaskFlow FastAPI Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/taskflow/backend
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Copy app to server
scp -r backend user@your-server:/opt/taskflow/

# Enable and start service
systemctl enable taskflow
systemctl start taskflow
```

### 1.2 Nginx Reverse Proxy Configuration

```bash
cat > /etc/nginx/sites-available/taskflow << 'EOF'
server {
    listen 80;
    server_name your-domain.com;  # or your-server-ip

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    location /static {
        alias /opt/taskflow/frontend;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
ln -s /etc/nginx/sites-available/taskflow /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

### 1.3 SSL Certificate (Let's Encrypt)

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

---

## Option 2: Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - SECRET_KEY=your-production-secret-key
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - app
```

### Create nginx.conf

```nginx
server {
    listen 80;
    server_name _;

    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Run with Docker

```bash
docker-compose up -d
```

---

## Option 3: Railway.app (Easiest - Free Tier)

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. "New Project" → "Deploy from GitHub"
4. Select your repository
5. Set start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Deploy!

---

## Option 4: Render.com (Free Tier)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. "New" → "Web Service"
4. Connect GitHub repo
5. Settings:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Deploy!

---

## Option 5: Fly.io (Free Tier)

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch
fly launch

# Set secrets
fly secrets set SECRET_KEY=your-production-secret-key

# Deploy
fly deploy
```

---

## Option 6: AWS EC2

```bash
# Launch EC2 instance (Ubuntu 22.04)
# Open ports 80 and 443 in security group

# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install
apt update && apt install -y python3-pip nginx

# Deploy
cd /opt/taskflow
pip3 install -r backend/requirements.txt

# Run with systemd (see Option 1)
# Configure nginx (see Option 1)
```

---

## Option 7: Google Cloud Run

```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash
gcloud init

# Build and deploy
gcloud run deploy taskflow \
  --source . \
  --region us-central1 \
  --platform managed
```

---

## Production Checklist

### Security
- [ ] Change `SECRET_KEY` in production
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Use environment variables for secrets

### Performance
- [ ] Enable gzip compression in nginx
- [ ] Set up caching headers
- [ ] Consider using a CDN for static files
- [ ] Database connection pooling

### Monitoring
- [ ] Set up logging
- [ ] Configure health checks
- [ ] Set up alerts
- [ ] Enable error tracking (Sentry)

### Backup
- [ ] Set up automated database backups
- [ ] Test restore process

---

## Quick Start Commands

```bash
# Clone repository
git clone https://github.com/yourusername/taskflow.git
cd taskflow

# Development
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Production (VPS)
# Follow Option 1 above

# Docker
docker-compose up -d
```

---

## Environment Variables

Create a `.env` file for production:

```env
SECRET_KEY=your-super-secret-production-key-change-this
DATABASE_URL=sqlite:///./todos.db
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ALGORITHM=HS256
```

---

## Troubleshooting

### App not starting?
```bash
# Check logs
journalctl -u taskflow -f

# Check if port is in use
lsof -i :8000

# Test manually
cd /opt/taskflow/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Nginx errors?
```bash
# Test config
nginx -t

# Check logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### Database issues?
```bash
# Reset database
rm backend/todos.db
# Restart app - will recreate
```
