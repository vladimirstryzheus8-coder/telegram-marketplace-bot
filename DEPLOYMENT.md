# Comprehensive Deployment Guide

## Quick Start (Local Development)

### Prerequisites
- Python 3.8+
- pip
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/vladimirstryzheus8-coder/telegram-marketplace-bot.git
cd telegram-marketplace-bot
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Setup Environment
```bash
cp .env.example .env
```

### Step 4: Initialize Database
```bash
python db_init.py
```

### Step 5: Run the Bot (Terminal 1)
```bash
python bot.py
```

### Step 6: Run Admin Panel (Terminal 2)
```bash
python admin_panel.py
```

### Access
- **Telegram Bot**: Search for your bot on Telegram
- **Admin Panel**: http://localhost:5000
  - Username: admin
  - Password: admin123

---

## Production Deployment (Railway)

### Why Railway?
- Free tier available
- Easy GitHub integration
- Auto-deploy on git push
- 24/7 uptime

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project

### Step 2: Connect GitHub Repository
1. Click "Create new" → "GitHub Repo"
2. Select your repository
3. Railway auto-detects Python

### Step 3: Add Environment Variables
1. Go to Variables tab
2. Copy from `.env.example`:
   - TELEGRAM_BOT_TOKEN
   - ADMIN_ID
   - FLASK_SECRET_KEY (generate random string)
   - etc.

### Step 4: Deploy
```bash
git push origin main
```
Railway auto-deploys!

---

## Production Deployment (Heroku Alternative)

### Step 1: Install Heroku CLI
```bash
npm install -g heroku
heroku login
```

### Step 2: Create Heroku App
```bash
heroku create your-marketplace-bot
```

### Step 3: Set Environment Variables
```bash
heroku config:set TELEGRAM_BOT_TOKEN="8876332968:AAHzETdVNXFMbjyyK_JWFMYbTTDfGKqwq2U"
heroku config:set ADMIN_ID="8517586725"
heroku config:set FLASK_SECRET_KEY="random-secret-key"
```

### Step 4: Deploy
```bash
git push heroku main
```

---

## Database Backup

### Backup Local Database
```bash
cp marketplace.db marketplace.backup.db
```

### Upgrade to PostgreSQL (Production)
1. In `.env`, change:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/marketplace
   ```
2. Install PostgreSQL
3. Run migrations:
   ```bash
   python db_init.py
   ```

---

## Monitoring & Logs

### View Logs (Railway)
```bash
railway logs
```

### View Logs (Heroku)
```bash
heroku logs --tail
```

---

## Troubleshooting

### Bot Not Responding
1. Check if bot is running: `python bot.py`
2. Verify token in `.env`
3. Check logs for errors

### Admin Panel Not Accessible
1. Verify Flask is running: `python admin_panel.py`
2. Open http://localhost:5000
3. Check credentials (admin/admin123)

### Database Issues
1. Delete old database: `rm marketplace.db`
2. Reinitialize: `python db_init.py`
3. Check file permissions

---

## Support
For issues, check logs or contact admin.
