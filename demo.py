#!/usr/bin/env python3
"""
Demo script to show the Vietnamese Finance News Aggregator working
"""

import time
from app import fetch_articles, summarize_article

def main():
    print("Vietnamese Finance News Aggregator - Demo")
    print("=" * 60)
    
    print("\nFetching latest articles...")
    articles = fetch_articles()
    
    print(f"\nSuccessfully fetched {len(articles)} articles")
    print("\nSample articles:")
    print("-" * 60)
    
    for i, article in enumerate(articles[:5], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Time: {article['timestamp'].strftime('%d/%m/%Y %H:%M')}")
        print(f"   URL: {article['url']}")
        
        if article['summary']:
            print(f"   Summary: {article['summary']}")
        
        print("-" * 60)
    
    print(f"\nStatistics:")
    print(f"   Total articles: {len(articles)}")
    
    # Count by source
    sources = {}
    for article in articles:
        source = article['source']
        sources[source] = sources.get(source, 0) + 1
    
    print(f"   Articles by source:")
    for source, count in sources.items():
        print(f"     - {source}: {count} articles")
    
    print(f"\nDemo completed successfully!")
    print(f"   The app is ready to run with: python3 app.py")
    print(f"   Or use the startup script: ./start.sh")

if __name__ == "__main__":
    main()

