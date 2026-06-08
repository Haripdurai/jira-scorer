#!/bin/bash

echo "🎯 JIRA Ticket Scorer - Setup Script"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend setup
echo -e "${YELLOW}Setting up Backend...${NC}"
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit backend/.env with your credentials${NC}"
fi

echo -e "${GREEN}✓ Backend setup complete!${NC}"
echo ""

# Frontend setup
echo -e "${YELLOW}Setting up Frontend...${NC}"
cd ../frontend

# Install npm dependencies
echo "Installing npm dependencies..."
npm install --silent

# Copy .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo -e "${GREEN}✓ Frontend setup complete!${NC}"
echo ""

# Final instructions
echo "======================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env with your JIRA and Anthropic credentials"
echo "2. Start the backend:"
echo "   cd backend && source venv/bin/activate && python app.py"
echo "3. In a new terminal, start the frontend:"
echo "   cd frontend && npm run dev"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "For Jupyter notebook:"
echo "   cd backend && jupyter notebook jira_scorer.ipynb"
echo ""
echo "Happy scoring! 🎯"
