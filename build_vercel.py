import subprocess
import sys
from pathlib import Path

def build_frontend():
    """Build the frontend during Vercel deployment"""
    print("=" * 60)
    print("Starting frontend build...")
    print("=" * 60)
    
    frontend_dir = Path(__file__).parent / "frontend"
    dist_dir = frontend_dir / "dist"
    
    # Check if already built
    if dist_dir.exists() and any(dist_dir.iterdir()):
        print("✅ Frontend already built, skipping...")
        return
    
    try:
        # Install pnpm globally
        print("📦 Installing pnpm...")
        subprocess.run(
            ["npm", "install", "-g", "pnpm"],
            check=True,
            cwd=str(frontend_dir)
        )
        
        # Install dependencies
        print("📦 Installing frontend dependencies...")
        subprocess.run(
            ["pnpm", "install"],
            check=True,
            cwd=str(frontend_dir)
        )
        
        # Build frontend
        print("🏗️  Building frontend...")
        subprocess.run(
            ["pnpm", "build"],
            check=True,
            cwd=str(frontend_dir)
        )
        
        print("=" * 60)
        print("✅ Frontend build complete!")
        print("=" * 60)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    build_frontend()
