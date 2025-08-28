#!/bin/bash

# Script to run both thumbnail extractor and gallery generator

echo "🎬 Douyin Thumbnail Extractor & Gallery Generator"
echo "================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if requests module is installed
if ! python3 -c "import requests" &> /dev/null; then
    echo "Installing requests module..."
    pip3 install requests
fi

# Run thumbnail extractor
echo "Step 1: Extracting thumbnails..."
echo "--------------------------------"
python3 douyin_thumbnail_extractor.py

echo ""
echo "Step 2: Generating gallery..."
echo "-----------------------------"
python3 generate_gallery.py

echo ""
echo "✅ All done!"
echo ""
echo "To view your gallery:"
echo "  • Open 'gallery.html' in your browser"
echo "  • Or run: open gallery.html (on macOS)"
echo ""
echo "Press Enter to exit..."
read
