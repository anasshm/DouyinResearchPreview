#!/bin/bash

# Simple script to run the Douyin thumbnail extractor

echo "Douyin Thumbnail Extractor"
echo "========================="
echo ""
echo "Make sure your m.douyin.com links are in input.txt"
echo "Results will be saved to output.txt"
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

# Run the extractor
python3 douyin_thumbnail_extractor.py

echo ""
echo "Press Enter to exit..."
read

