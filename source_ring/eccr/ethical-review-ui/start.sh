#!/bin/bash

# ECCR Ethical Review UI - Quick Start Script
# This script helps you get the interface running quickly

echo ""
echo "∞Δ═══════════════════════════════════════════════════════════════∞Δ"
echo ""
echo "   🌊 ECCR Ethical Review UI - Quick Start"
echo "   Sandcastle Sequence v0.3 | ESC-1 Protocol"
echo ""
echo "∞Δ═══════════════════════════════════════════════════════════════∞Δ"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
  echo "📦 Installing dependencies..."
  npm install
  echo ""
fi

# Check if both terminals should be opened
echo "🚀 Starting services..."
echo ""
echo "   You need TWO terminal windows:"
echo "   Terminal 1: Mock Server (port 5550)"
echo "   Terminal 2: React App (port 5173)"
echo ""
echo "   Would you like to:"
echo "   1) Start Mock Server only"
echo "   2) Start React App only"
echo "   3) Get manual instructions"
echo ""
read -p "   Enter choice (1-3): " choice

case $choice in
  1)
    echo ""
    echo "   Starting Mock Server on http://localhost:5550..."
    echo ""
    npm run mock-server
    ;;
  2)
    echo ""
    echo "   Starting React App on http://localhost:5173..."
    echo ""
    npm run dev
    ;;
  3)
    echo ""
    echo "   Manual Instructions:"
    echo "   ────────────────────"
    echo ""
    echo "   Terminal 1:"
    echo "   $ cd $(pwd)"
    echo "   $ npm run mock-server"
    echo ""
    echo "   Terminal 2:"
    echo "   $ cd $(pwd)"
    echo "   $ npm run dev"
    echo ""
    echo "   Then open: http://localhost:5173"
    echo ""
    ;;
  *)
    echo "   Invalid choice. Run './start.sh' again."
    ;;
esac

echo ""
