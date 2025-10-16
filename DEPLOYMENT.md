# Production Deployment Guide

## **Important: Background Threads Don't Work in Production**

The auto-refresh feature using background threads **will NOT work** when deployed to:

- Vercel
- Render
- Netlify
- Heroku
- Any serverless platform

**Why?** These platforms use serverless functions that only run when requested, not continuously.

## 🔧 **Solution: Use Cron Jobs**

### **Step 1: Deploy Your App**

Deploy using any of these methods:

#### **Vercel (Recommended)**

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# OPENAI_API_KEY=your_key_here
```

#### **Render**

1. Connect your GitHub repo to Render
2. Create a new Web Service
3. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app_production.py`
   - Environment: `Python 3`

#### **Netlify**

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod
```

### **Step 2: Set Up Cron Jobs**

#### **Option A: cron-job.org (Free)**

1. Go to [cron-job.org](https://cron-job.org)
2. Create a free account
3. Add a new cron job:
   - **URL**: `https://your-app.vercel.app/cron/update`
   - **Schedule**: `*/10 * * * *` (every 10 minutes)
   - **Method**: GET
   - **Title**: "Vietnamese News Update"

#### **Option B: EasyCron (Free tier)**

1. Go to [EasyCron](https://www.easycron.com)
2. Create account
3. Add cron job:
   - **URL**: `https://your-app.vercel.app/cron/update`
   - **Schedule**: Every 10 minutes
   - **Method**: GET

#### **Option C: Vercel Cron (Pro feature)**

If you have Vercel Pro, add to `vercel.json`:

```json
{
  "crons": [
    {
      "path": "/cron/update",
      "schedule": "*/10 * * * *"
    }
  ]
}
```

### **Step 3: Test Your Cron Job**

1. **Test the endpoint manually**:

   ```bash
   curl https://your-app.vercel.app/cron/update
   ```

2. **Check the response**:

   ```json
   {
     "success": true,
     "message": "Cron updated 16 articles",
     "last_update": "2025-10-16T02:30:00",
     "timestamp": "2025-10-16T02:30:00"
   }
   ```

3. **Monitor your app**:
   ```bash
   curl https://your-app.vercel.app/health
   ```

## **How It Works in Production**

### **Local Development:**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User visits   │--->│   Flask app      │--->│  Background     │
│   localhost     │    │   serves page    │    │  thread updates │
└─────────────────┘    └──────────────────┘    │  every 10 min   │
                                               └─────────────────┘
```

### **Production:**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Cron job      │--->│   /cron/update   │--->│  Updates        │
│   every 10 min  │    │   endpoint       │    │  articles       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                ▲
                                │
┌─────────────────┐             │
│   User visits   │─────────────┘
│   your-app.com  │
└─────────────────┘
```

## **Monitoring Your App**

### **Health Check Endpoint**

```bash
curl https://your-app.vercel.app/health
```

Response:

```json
{
  "status": "healthy",
  "articles_count": 16,
  "last_update": "2025-10-16T02:30:00",
  "timestamp": "2025-10-16T02:30:00"
}
```

### **Manual Refresh**

```bash
curl https://your-app.vercel.app/api/refresh
```

## **Troubleshooting**

### **Cron Job Not Working?**

1. **Check the URL**: Make sure it's correct
2. **Test manually**: Use curl to test the endpoint
3. **Check logs**: Look at your platform's logs
4. **Verify schedule**: Make sure cron is set to run every 10 minutes

### **Articles Not Updating?**

1. **Check cron job status**: Is it running?
2. **Test endpoint**: Does `/cron/update` work?
3. **Check RSS feeds**: Are they accessible?
4. **Monitor logs**: Look for error messages

### **Performance Issues?**

1. **Limit articles**: Reduce from 10 to 5 per feed
2. **Add caching**: Use Redis or similar
3. **Optimize queries**: Reduce API calls

## 📈 **Advanced Features**

### **Database Storage (Optional)**

For better performance, store articles in a database:

```python
# Add to requirements.txt
# sqlite3 (built-in) or psycopg2 for PostgreSQL

import sqlite3
from datetime import datetime, timedelta

def store_articles(articles):
    conn = sqlite3.connect('articles.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            url TEXT UNIQUE,
            source TEXT,
            timestamp TEXT,
            summary TEXT,
            created_at TEXT
        )
    ''')

    # Clear old articles (older than 24 hours)
    cursor.execute("DELETE FROM articles WHERE created_at < ?",
                   (datetime.now() - timedelta(hours=24),))

    # Insert new articles
    for article in articles:
        cursor.execute("""
            INSERT OR REPLACE INTO articles
            (title, url, source, timestamp, summary, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            article['title'], article['url'], article['source'],
            article['timestamp'].isoformat(), article['summary'],
            datetime.now().isoformat()
        ))

    conn.commit()
    conn.close()
```

## **Summary**

**What works in production:**

- Manual refresh (`/api/refresh`)
- Cron job updates (`/cron/update`)
- Health monitoring (`/health`)
- All RSS feed parsing
- AI summarization

**What doesn't work in production:**

- Background threads
- Auto-refresh every 10 minutes without cron jobs

**Solution:** Use external cron services to call your `/cron/update` endpoint every 10 minutes.

Your app will work perfectly in production with this setup!
