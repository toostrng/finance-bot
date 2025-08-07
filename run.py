#!/usr/bin/env python3
"""
Finance Manager Bot - Main Runner
Runs both the Telegram bot and Flask web application
"""

import os
import sys
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def run_webapp():
    """Run Flask web application"""
    from webapp import app
    print("🌐 Starting Flask web application...")
    app.run(debug=False, host='0.0.0.0', port=5000)

def run_bot():
    """Run Telegram bot"""
    from bot import main as bot_main
    print("🤖 Starting Telegram bot...")
    bot_main()

def main():
    """Main function to run both services"""
    print("🚀 Starting Finance Manager Bot...")
    
    # Check required environment variables
    required_vars = ['TELEGRAM_TOKEN']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Missing TELEGRAM_TOKEN - running web app only")
        print("To run the full bot, set TELEGRAM_TOKEN environment variable")
        
        # Run only web app
        run_webapp()
        return
    
    # Set default values for optional variables
    if not os.getenv('WEBAPP_URL'):
        os.environ['WEBAPP_URL'] = 'http://localhost:5000'
        print("⚠️  WEBAPP_URL not set, using default: http://localhost:5000")
    
    if not os.getenv('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
        print("⚠️  SECRET_KEY not set, using default (change in production)")
    
    # Start web application in a separate thread
    webapp_thread = threading.Thread(target=run_webapp, daemon=True)
    webapp_thread.start()
    
    # Wait a moment for webapp to start
    time.sleep(2)
    
    # Start bot in main thread
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Error running bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 