import sys
from pathlib import Path

root = Path(__file__).parent.parent
sys.path.insert(0, str(root))

from server import app

app = app