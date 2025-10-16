#!/usr/bin/env python3
"""
Test script to verify RSS feeds are working correctly
"""

import feedparser
from datetime import datetime

# RSS feed URLs
RSS_FEEDS = [
    "https://vnexpress.net/rss/kinh-doanh.rss",
    "https://cafef.vn/home.rss", 
    "https://ndh.vn/rss",
    "https://baodautu.vn/rss",
    "https://www.vietnamplus.vn/rss/kinhte.rss",
    "https://thoibaotaichinhvietnam.vn/rss"
]

def test_feed(feed_url):
    """Test a single RSS feed"""
    print(f"\nTesting: {feed_url}")
    print("-" * 60)
    
    try:
        feed = feedparser.parse(feed_url)
        
        if feed.bozo:
            print("Warning: Feed has parsing issues")
            if hasattr(feed, 'bozo_exception'):
                print(f"   Error: {feed.bozo_exception}")
        
        print(f"Feed Title: {feed.feed.get('title', 'Unknown')}")
        print(f"Entries: {len(feed.entries)}")
        
        if feed.entries:
            print("\nSample articles:")
            for i, entry in enumerate(feed.entries[:3]):
                title = entry.get('title', 'No title')[:80]
                link = entry.get('link', 'No link')
                published = entry.get('published', 'No date')
                print(f"   {i+1}. {title}...")
                print(f"      Link: {link}")
                print(f"      Published: {published}")
                print()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Test all RSS feeds"""
    print("Testing Vietnamese Finance News RSS Feeds")
    print("=" * 60)
    
    success_count = 0
    total_count = len(RSS_FEEDS)
    
    for feed_url in RSS_FEEDS:
        if test_feed(feed_url):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {success_count}/{total_count} feeds working")
    
    if success_count == total_count:
        print("All feeds are working correctly!")
    else:
        print("Some feeds may have issues. Check the output above.")
    
    print("\nIf you see errors, the feeds might be temporarily unavailable.")
    print("   The app will handle these gracefully and continue working.")

if __name__ == "__main__":
    main()

