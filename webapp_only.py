#!/usr/bin/env python3
"""
Finance Manager Web App - Web Only Version
For deployment on platforms like Render, Railway, etc.
"""

import os
from dotenv import load_dotenv
from webapp import app

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 