#!/usr/bin/env python3
"""
Setup script for Render deployment
"""

import os
import sys

def check_files():
    """Check if all required files exist"""
    print("🔍 Checking required files...")
    
    required_files = [
        'requirements.txt',
        'webapp.py',
        'models.py',
        'database.py',
        'config.py',
        'templates/index.html',
        'static/css/style.css',
        'static/js/app.js',
        'render.yaml',
        'Procfile',
        'runtime.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def check_requirements():
    """Check requirements.txt"""
    print("\n📦 Checking requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
            
        required_packages = [
            'flask',
            'gunicorn',
            'sqlalchemy',
            'psycopg2-binary'
        ]
        
        for package in required_packages:
            if package in content:
                print(f"✅ {package}")
            else:
                print(f"❌ {package} - missing")
                return False
                
        return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def check_config():
    """Check configuration"""
    print("\n⚙️ Checking configuration...")
    
    try:
        from config import Config
        print("✅ Config loaded successfully")
        
        # Check if webapp can be imported
        from webapp import app
        print("✅ Webapp can be imported")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def generate_env_template():
    """Generate .env template for Render"""
    print("\n📝 Generating .env template...")
    
    env_content = """# Render Deployment Configuration
# Copy this to your Render environment variables

TELEGRAM_TOKEN=your_telegram_bot_token_here
SECRET_KEY=your-secret-key-here-change-this-in-production
DATABASE_URL=postgresql://user:password@host:port/database
WEBAPP_URL=https://your-app-name.onrender.com
DEBUG=false
"""
    
    with open('.env.render', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env.render template")
    print("📋 Copy these variables to Render environment settings")

def main():
    """Main setup function"""
    print("🚀 Render Deployment Setup")
    print("=" * 50)
    
    checks = [
        check_files,
        check_requirements,
        check_config
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Setup Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 Your project is ready for Render deployment!")
        print("\n📋 Next steps:")
        print("1. Create GitHub repository")
        print("2. Push code to GitHub")
        print("3. Create Render account")
        print("4. Deploy using DEPLOYMENT.md instructions")
        
        generate_env_template()
        return 0
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 