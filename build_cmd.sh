#!/bin/bash
set -e

echo "Installing frontend dependencies..."
cd frontend
npm install -g pnpm
pnpm install

echo "Building frontend..."
pnpm build

echo "Frontend build complete!"
ls -la dist/
