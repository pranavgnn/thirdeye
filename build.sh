#!/bin/bash
# Build script for Vercel

echo "Building frontend..."
cd frontend
pnpm install
pnpm build
cd ..

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Build complete!"
