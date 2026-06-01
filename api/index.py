import sys
import os

# Add the root directory to the python path so we can import our app
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from app import app
