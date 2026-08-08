import sys
import os

# Add the root project directory to the Python path so it can find 'backend' and 'core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.wsgi import application

# Vercel automatically looks for a variable named 'app' in the api/ directory
app = application
