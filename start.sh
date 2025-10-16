#!/bin/bash

echo "Vietnamese Finance News Aggregator"
echo "======================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp env.example .env
    echo ".env file created. Edit it to add your OpenAI API key if needed."
fi

# Start the application
echo "Starting the application..."
echo "   Open your browser and go to: http://localhost:5000"
echo "   Press Ctrl+C to stop the server"
echo "======================================"

python3 app.py
