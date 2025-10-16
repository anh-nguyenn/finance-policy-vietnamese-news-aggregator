from flask import Flask, render_template, jsonify
import feedparser
import requests
from datetime import datetime, timedelta
import threading
import time
import os
from typing import List, Dict
import re
from urllib.parse import urlparse
from summarizer import summarize_article, is_financial_news

app = Flask(__name__)

# RSS feed URLs
RSS_FEEDS = [
    "https://vnexpress.net/rss/kinh-doanh.rss",
    "https://cafef.vn/home.rss", 
    "https://ndh.vn/rss",
    "https://baodautu.vn/rss",
    "https://www.vietnamplus.vn/rss/kinhte.rss",
    "https://thoibaotaichinhvietnam.vn/rss"
]

# Source names mapping
SOURCE_NAMES = {
    "vnexpress.net": "VnExpress",
    "cafef.vn": "Cafef",
    "ndh.vn": "NDH",
    "baodautu.vn": "Báo Đầu Tư",
    "vietnamplus.vn": "VietnamPlus",
    "thoibaotaichinhvietnam.vn": "Thời Báo Tài Chính"
}

# Global variable to store articles
articles = []
last_update = None

def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_source_name(url: str) -> str:
    """Extract source name from URL"""
    try:
        domain = urlparse(url).netloc
        for source_domain, source_name in SOURCE_NAMES.items():
            if source_domain in domain:
                return source_name
        return domain
    except:
        return "Unknown"

def parse_timestamp(entry) -> datetime:
    """Parse timestamp from RSS entry"""
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            return datetime(*entry.published_parsed[:6])
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            return datetime(*entry.updated_parsed[:6])
        else:
            return datetime.now()
    except:
        return datetime.now()

def fetch_articles() -> List[Dict]:
    """Fetch articles from all RSS feeds"""
    all_articles = []
    
    for feed_url in RSS_FEEDS:
        try:
            print(f"Fetching from {feed_url}")
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                print(f"Warning: Feed {feed_url} has parsing issues")
            
            for entry in feed.entries[:20]:  # Limit to 20 articles per feed
                try:
                    title = clean_text(entry.get('title', ''))
                    content = clean_text(entry.get('summary', ''))
                    
                    # Only process financial/policy related articles
                    if not is_financial_news(title, content):
                        continue
                    
                    # Generate AI summary
                    ai_summary = summarize_article(title, content, use_openai=os.getenv('OPENAI_API_KEY') is not None)
                    
                    article = {
                        'title': title,
                        'url': entry.get('link', ''),
                        'source': get_source_name(entry.get('link', '')),
                        'timestamp': parse_timestamp(entry),
                        'summary': ai_summary or (content[:200] + '...' if content else ''),
                        'ai_summary': ai_summary is not None
                    }
                    
                    if article['title'] and article['url']:
                        all_articles.append(article)
                        
                except Exception as e:
                    print(f"Error parsing entry from {feed_url}: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error fetching {feed_url}: {e}")
            continue
    
    # Sort by timestamp (newest first)
    all_articles.sort(key=lambda x: x['timestamp'], reverse=True)
    return all_articles

def update_articles():
    """Update articles in background thread"""
    global articles, last_update
    while True:
        try:
            print("Updating articles...")
            articles = fetch_articles()
            last_update = datetime.now()
            print(f"Updated {len(articles)} articles at {last_update}")
        except Exception as e:
            print(f"Error updating articles: {e}")
        
        # Wait 10 minutes before next update
        time.sleep(600)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html', articles=articles, last_update=last_update)

@app.route('/api/articles')
def api_articles():
    """API endpoint for articles"""
    return jsonify({
        'articles': articles,
        'last_update': last_update.isoformat() if last_update else None,
        'count': len(articles)
    })

@app.route('/api/refresh')
def api_refresh():
    """Manual refresh endpoint"""
    global articles, last_update
    try:
        articles = fetch_articles()
        last_update = datetime.now()
        return jsonify({
            'success': True,
            'message': f'Refreshed {len(articles)} articles',
            'last_update': last_update.isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Start background thread for updating articles
    update_thread = threading.Thread(target=update_articles, daemon=True)
    update_thread.start()
    
    # Initial fetch
    print("Starting initial article fetch...")
    articles = fetch_articles()
    last_update = datetime.now()
    print(f"Initial fetch complete: {len(articles)} articles")
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
