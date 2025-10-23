#!/bin/bash
set -e

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Building Frontend ==="
cd frontend

# Install pnpm
npm install -g pnpm

# Install frontend dependencies
pnpm install

# Build frontend
pnpm build

echo "=== Build Complete ==="
ls -la dist/
