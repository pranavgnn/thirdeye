import sys
from pathlib import Path

# Add project root to path so imports work
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from server import app

# Export app for Vercel's ASGI handler
# Vercel will automatically wrap this FastAPI app
app = app