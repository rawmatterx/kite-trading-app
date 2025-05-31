#!/bin/bash

# Exit on error
set -e

echo "🚀 Setting up Kite Trading App development environment..."

# Create required directories
echo "📁 Creating required directories..."
mkdir -p logs/backend logs/frontend data/db

# Copy environment files
echo "📋 Copying environment files..."
cp -n .env.example .env
cp -n backend/.env.example backend/.env
cp -n frontend/.env.example frontend/.env

# Build and start services
echo "🚀 Building and starting services with Docker Compose..."
docker-compose up --build -d

echo "✅ Setup complete! Services are starting in the background."
echo ""
echo "📋 Services:"
echo "- Backend API:    http://localhost:8000"
echo "- Frontend:       http://localhost:3000"
echo "- API Docs:       http://localhost:8000/api/docs"
echo "- pgAdmin:        http://localhost:5050"
echo "  - Email:        admin@example.com"
echo "  - Password:     admin"
echo ""
echo "To view logs, run: docker-compose logs -f"
echo "To stop services: docker-compose down"

# Make the script executable
chmod +x setup.sh
