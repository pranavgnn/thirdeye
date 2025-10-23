#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

def main():
    print("Building frontend...")
    frontend_dir = Path(__file__).parent / "frontend"
    
    # Install pnpm if needed and build
    try:
        subprocess.run(["pnpm", "install"], cwd=frontend_dir, check=True)
        subprocess.run(["pnpm", "build"], cwd=frontend_dir, check=True)
        print("Frontend build successful!")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
