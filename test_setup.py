#!/usr/bin/env python3
"""
Test script for Finance Manager Bot setup
"""

import os
import sys
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'telegram',
        'flask',
        'sqlalchemy',
        'dotenv'
    ]
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config import Config
        print("✅ Config loaded successfully")
        
        if not Config.TELEGRAM_TOKEN:
            print("⚠️  TELEGRAM_TOKEN not set")
        else:
            print("✅ TELEGRAM_TOKEN is set")
            
        print(f"✅ Supported currencies: {Config.SUPPORTED_CURRENCIES}")
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_database():
    """Test database connection and models"""
    print("\n🗄️ Testing database...")
    
    try:
        from models import create_tables, get_db
        from database import DatabaseManager
        
        # Create tables
        create_tables()
        print("✅ Database tables created")
        
        # Test database connection
        db = next(get_db())
        db_manager = DatabaseManager(db)
        print("✅ Database connection successful")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_webapp():
    """Test webapp setup"""
    print("\n🌐 Testing webapp...")
    
    try:
        from webapp import app
        print("✅ Flask app created successfully")
        
        # Test if routes are registered
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        print(f"✅ {len(routes)} routes registered")
        
        return True
    except Exception as e:
        print(f"❌ Webapp error: {e}")
        return False

def test_bot():
    """Test bot setup"""
    print("\n🤖 Testing bot...")
    
    try:
        from bot import FinanceBot
        print("✅ Bot class imported successfully")
        
        # Note: We can't test bot creation without a valid token
        if not os.getenv('TELEGRAM_TOKEN'):
            print("⚠️  Cannot test bot creation without TELEGRAM_TOKEN")
        else:
            print("✅ TELEGRAM_TOKEN available for bot testing")
        
        return True
    except Exception as e:
        print(f"❌ Bot error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Finance Manager Bot - Setup Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_database,
        test_webapp,
        test_bot
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Setup is ready.")
        print("\n📝 Next steps:")
        print("1. Create a .env file with your TELEGRAM_TOKEN")
        print("2. Run: python run.py")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 