#!/bin/bash
echo "🚀 Setting up Finance Terminal..."

python3 --version
if [ $? -ne 0 ]; then
  echo "❌ Python not found. Please install Python 3 first."
  exit 1
fi

echo "📦 Installing dependencies..."
pip install -r requirements.txt

mkdir -p logs
echo "✅ Setup complete. Try running:"
echo "python main.py stocks AAPL summary"
