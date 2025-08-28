# Douyin Thumbnail Extractor

A simple Python script that extracts thumbnail URLs from m.douyin.com links.

## Setup

1. Install Python 3 (if not already installed)
2. Install the required package:
   ```bash
   pip install -r requirements.txt
   ```
   OR just run:
   ```bash
   pip install requests
   ```

## Usage

1. Add your m.douyin.com links to `input.txt` (one URL per line)
2. Run the script:
   ```bash
   python douyin_thumbnail_extractor.py
   ```
3. Check `output.txt` for the results

## Input Format

The `input.txt` file should contain one m.douyin.com URL per line:
```
https://m.douyin.com/share/video/1234567890
https://m.douyin.com/share/video/0987654321
```

## Output Format

The `output.txt` file will contain only the thumbnail URLs, one per line:
```
https://example.byteimg.com/thumbnail.jpg
https://example.byteimg.com/another.jpg
```

URLs without thumbnails are skipped and not included in the output.

## HTML Gallery Feature

After extracting thumbnails, you can generate a visual gallery:

1. Run `python3 generate_gallery.py`
2. Open `gallery.html` in your browser
3. Click any thumbnail to go to the original Douyin video

The gallery shows:
- Thumbnail images in a responsive grid layout
- Video number and URL below each thumbnail
- Dark theme matching Douyin's style
- Mobile-friendly responsive design

## How It Works

The script mimics your browser console code:
1. Fetches the HTML page
2. Looks for thumbnail URLs in:
   - Meta tags (og:image, twitter:image)
   - Video poster attributes
   - Embedded JSON data (RENDER_DATA, SIGI_STATE)
   - Cover/origin_cover patterns
3. Filters for Douyin/ByteImg image URLs
4. Returns the best quality thumbnail (usually the last one found)

## Quick Start

For the easiest way to run everything (extract + gallery):
- On macOS/Linux: Double-click `run_all.sh` or run `./run_all.sh` in terminal
- On Windows: Run both scripts:
  1. `python3 douyin_thumbnail_extractor.py`
  2. `python3 generate_gallery.py`

For just the extractor:
- On macOS/Linux: Double-click `run_extractor.sh` or run `./run_extractor.sh` in terminal
- On Windows: Just run `python3 douyin_thumbnail_extractor.py`

## Troubleshooting

- Make sure you're using m.douyin.com URLs (not www.douyin.com)
- The script includes a 1-second delay between requests to be polite to the server
- If you get connection errors, check your internet connection
- Some videos might not have accessible thumbnails

## How the Solution Works

The script successfully extracts thumbnails by:
1. Removing compression headers to get readable HTML
2. Parsing JSON data embedded in script tags
3. Unescaping HTML entities in URLs
4. Prioritizing actual video thumbnails (douyinpic.com) over static assets

## File Directory

- `douyin_thumbnail_extractor.py` - Main Python script for extracting thumbnails
- `generate_gallery.py` - Script to generate HTML gallery from thumbnails
- `input.txt` - Input file for Douyin URLs
- `output.txt` - Output file with thumbnail URLs
- `gallery.html` - Generated HTML gallery (created after running generate_gallery.py)
- `requirements.txt` - Python dependencies
- `run_extractor.sh` - Shell script for running just the extractor
- `run_all.sh` - Shell script for running extractor + gallery generator
- `Dev console code` - Original JavaScript code for reference

