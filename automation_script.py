from playwright.sync_api import sync_playwright
import os
from datetime import datetime
from db_utils import WebsiteDB

def load_websites():
    """Load websites from MongoDB database"""
    try:
        # Get MongoDB connection string from environment variable
        mongodb_uri = os.environ.get("MONGODB_URI")
        if not mongodb_uri:
            print("⚠️  MONGODB_URI environment variable not set")
            return []
        
        db = WebsiteDB(mongodb_uri)
        websites = db.get_all_websites()
        db.close()
        return websites
    except Exception as e:
        print(f"❌ Error loading websites from database: {e}")
        return []

def wake_up_website(page, url):
    """Wake up a single website"""
    try:
        print(f"\n{'='*60}")
        print(f"Processing: {url}")
        print(f"{'='*60}")
        
        page.goto(url, timeout=30000)
        page.wait_for_load_state("networkidle", timeout=30000)
        
        # Try to find and click the wake-up button
        try:
            button = page.get_by_role("button", name="Yes, get this app back up!")
            
            if button.is_visible(timeout=10000):
                print("✅ Wake-up button found! Clicking...")
                button.click()
                print("✅ Button clicked successfully.")
                page.wait_for_timeout(3000)  # Wait for app to wake up
            else:
                print("ℹ️  App is already awake (no wake-up button found)")
                
        except Exception as e:
            print(f"ℹ️  App is already awake or button not found: {e}")
        
        print(f"✅ Successfully processed: {url}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {url}: {e}")
        return False

def run():
    """Main function to wake up all websites"""
    print(f"\n🚀 Starting wake-up script at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load websites from MongoDB
    websites = load_websites()
    
    if not websites:
        print("⚠️  No websites found in database")
        return
    
    print(f"📋 Found {len(websites)} website(s) to wake up")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Process each website
        success_count = 0
        for url in websites:
            if wake_up_website(page, url):
                success_count += 1
        
        browser.close()
    
    print(f"\n{'='*60}")
    print(f"✅ Completed: {success_count}/{len(websites)} websites processed successfully")
    print(f"🕐 Finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    run()
