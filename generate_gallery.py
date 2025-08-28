#!/usr/bin/env python3
"""
Generate HTML gallery from Douyin thumbnails
Reads input.txt for video URLs and output.txt for thumbnail URLs
Creates gallery.html with clickable thumbnail images
"""

def generate_gallery():
    """Generate HTML gallery from input and output files"""
    
    # Read video URLs from input.txt
    try:
        with open('input.txt', 'r', encoding='utf-8') as f:
            video_urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    except FileNotFoundError:
        print("Error: input.txt not found!")
        return False
    
    # Read thumbnail URLs from output.txt
    try:
        with open('output.txt', 'r', encoding='utf-8') as f:
            thumbnail_urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: output.txt not found!")
        print("Please run douyin_thumbnail_extractor.py first.")
        return False
    
    # Create HTML gallery
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Douyin Video Gallery</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #0a0a0a;
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }
        
        h1 {
            text-align: center;
            color: #fe2c55;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        
        .gallery {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .video-card {
            position: relative;
            border-radius: 12px;
            overflow: hidden;
            background-color: #161823;
            transition: transform 0.2s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .video-card:hover {
            transform: scale(1.05);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        }
        
        .video-card a {
            display: block;
            text-decoration: none;
        }
        
        .video-card img {
            width: 100%;
            height: auto;
            display: block;
            aspect-ratio: 9/16;
            object-fit: cover;
        }
        
        .video-info {
            padding: 12px;
            background-color: #161823;
        }
        
        .video-number {
            color: #8a8b91;
            font-size: 0.9em;
            margin-bottom: 4px;
        }
        
        .video-link {
            color: #fe2c55;
            font-size: 0.85em;
            word-break: break-all;
            opacity: 0.8;
        }
        
        .no-videos {
            text-align: center;
            color: #8a8b91;
            font-size: 1.2em;
            margin-top: 50px;
        }
        
        .stats {
            text-align: center;
            color: #8a8b91;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        @media (max-width: 1200px) {
            .gallery {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        @media (max-width: 900px) {
            .gallery {
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
            }
        }
        
        @media (max-width: 600px) {
            .gallery {
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }
            
            h1 {
                font-size: 1.8em;
            }
        }
    </style>
</head>
<body>
    <h1>🎥 Douyin Video Gallery</h1>
"""
    
    # Calculate how many thumbnails we can display
    num_pairs = min(len(video_urls), len(thumbnail_urls))
    
    if num_pairs > 0:
        html_content += f'    <div class="stats">Showing {num_pairs} videos</div>\n'
        html_content += '    <div class="gallery">\n'
        
        for i in range(num_pairs):
            video_url = video_urls[i]
            thumbnail_url = thumbnail_urls[i]
            
            html_content += f'''        <div class="video-card">
            <a href="{video_url}" target="_blank" rel="noopener noreferrer">
                <img src="{thumbnail_url}" alt="Video {i+1}" loading="lazy">
                <div class="video-info">
                    <div class="video-number">Video #{i+1}</div>
                    <div class="video-link">{video_url}</div>
                </div>
            </a>
        </div>
'''
        
        html_content += '    </div>\n'
    else:
        html_content += '    <div class="no-videos">No videos to display. Please run the thumbnail extractor first.</div>\n'
    
    html_content += """</body>
</html>"""
    
    # Save HTML file
    with open('gallery.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Gallery created successfully!")
    print(f"📊 Generated gallery with {num_pairs} videos")
    print(f"🌐 Open 'gallery.html' in your browser to view")
    
    # Note about mismatched counts
    if len(video_urls) != len(thumbnail_urls):
        print(f"\n⚠️  Warning: Found {len(video_urls)} video URLs but {len(thumbnail_urls)} thumbnails")
        print("   Some videos might not have thumbnails extracted.")
        print("   The gallery shows only videos with thumbnails.")
    
    return True

if __name__ == "__main__":
    generate_gallery()
