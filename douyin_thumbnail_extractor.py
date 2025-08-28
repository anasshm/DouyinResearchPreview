#!/usr/bin/env python3
"""
Simple Douyin Thumbnail Extractor
Reads m.douyin links from input.txt and saves thumbnail URLs to output.txt
"""

import re
import json
import requests
from urllib.parse import unquote
import html as html_module
import time

def extract_thumbnail(url):
    """Extract thumbnail URL from a m.douyin link"""
    try:
        # Add headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
        }
        
        # Fetch the page
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        html = response.text
        
        candidates = set()
        
        # 1) Look for meta tags
        meta_patterns = [
            r'<meta\s+property="og:image"\s+content="([^"]+)"',
            r'<meta\s+name="og:image"\s+content="([^"]+)"',
            r'<meta\s+name="twitter:image"\s+content="([^"]+)"',
            r'<meta\s+property="twitter:image"\s+content="([^"]+)"'
        ]
        for pattern in meta_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            candidates.update(matches)
        
        # 2) Look for video poster attributes
        video_poster = re.findall(r'<video[^>]+poster="([^"]+)"', html, re.IGNORECASE)
        candidates.update(video_poster)
        
        # 3) Look for embedded JSON data
        # Look for script tags with type="application/json"
        json_script_pattern = r'<script[^>]*type="application/json"[^>]*>([^<]+)</script>'
        json_scripts = re.findall(json_script_pattern, html, re.DOTALL)
        
        for script_content in json_scripts:
            try:
                # Unescape HTML entities
                script_content = html_module.unescape(script_content)
                data = json.loads(script_content)
                # Walk through the JSON looking for URLs
                extract_urls_from_json(data, candidates)
            except:
                pass
        
        # Find script tags with JSON content
        script_patterns = [
            r'<script[^>]*>([^<]+)</script>',
            r'window\._ROUTER_DATA\s*=\s*({[^;]+});',
            r'window\.RENDER_DATA\s*=\s*({[^;]+});',
            r'window\._SIGI_STATE\s*=\s*({[^;]+});',
            r'window\._MODERNJS_ROUTE_MANIFEST\s*=\s*({[^;]+});'
        ]
        
        for pattern in script_patterns:
            matches = re.findall(pattern, html, re.DOTALL)
            for match in matches:
                try:
                    # Try to parse as JSON
                    data = json.loads(match)
                    # Walk through the JSON looking for URLs
                    extract_urls_from_json(data, candidates)
                except:
                    # Try URL decoding first
                    try:
                        decoded = unquote(match)
                        data = json.loads(decoded)
                        extract_urls_from_json(data, candidates)
                    except:
                        pass
        
        # 4) Fallback: Look for cover/origin_cover patterns in raw HTML
        cover_patterns = [
            r'"origin_cover"[^}]*?"url_list"\s*:\s*\[([^\]]+)\]',
            r'"cover"[^}]*?"url_list"\s*:\s*\[([^\]]+)\]',
            r'"dynamic_cover"[^}]*?"url_list"\s*:\s*\[([^\]]+)\]'
        ]
        
        for pattern in cover_patterns:
            matches = re.findall(pattern, html, re.DOTALL)
            for match in matches:
                urls = re.findall(r'"(https?://[^"]+)"', match)
                candidates.update(urls)
        
        # 5) Very loose fallback: any Douyin/Bytedance image URLs
        loose_urls = re.findall(r'https?://[^\s"\'()]+?(?:douyin|byteimg|pstatp|douyinpic)[^\s"\'()]*', html)
        candidates.update(loose_urls)
        
        # Filter for image URLs
        image_extensions = r'\.(jpe?g|png|webp|bmp|heic)(?:$|\?)'
        douyin_domains = r'(?:douyin|byteimg|pstatp|douyinpic)'
        
        image_urls = []
        for candidate in candidates:
            if candidate:
                # Unescape HTML entities in URL
                candidate = html_module.unescape(candidate)
                if re.search(douyin_domains, candidate):
                    # Check if it looks like an image URL
                    if re.search(image_extensions, candidate.split('?')[0], re.IGNORECASE):
                        image_urls.append(candidate)
        
        # If no strict image URLs found, try loose matches
        if not image_urls:
            image_urls = []
            for url in candidates:
                if url:
                    url = html_module.unescape(url)
                    if re.search(douyin_domains, url):
                        image_urls.append(url)
        
        # Prioritize douyinpic.com URLs (actual video thumbnails) over static assets
        if image_urls:
            # Look for douyinpic URLs first
            douyinpic_urls = [url for url in image_urls if 'douyinpic.com' in url]
            if douyinpic_urls:
                return douyinpic_urls[-1]  # Return the last (usually highest quality)
            
            # Then look for byteimg URLs with certain patterns
            byteimg_urls = [url for url in image_urls if 'byteimg.com' in url and any(x in url for x in ['tos-cn-i', 'img-cn-i', 'p3-sign', 'p9-sign'])]
            if byteimg_urls:
                return byteimg_urls[-1]
            
            # Fallback to any image URL, but avoid common static assets
            filtered_urls = [url for url in image_urls if not any(x in url for x in ['logo', 'favicon', 'icon', 'static', 'eden-cn'])]
            if filtered_urls:
                return filtered_urls[-1]
            
            # Last resort: return any image URL
            return image_urls[-1]
        else:
            return None
            
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None

def extract_urls_from_json(obj, candidates):
    """Recursively extract URLs from JSON object"""
    if isinstance(obj, dict):
        # Check for specific keys
        for key in ['url_list', 'cover', 'origin_cover', 'dynamic_cover', 'poster', 'download_addr', 'play_addr']:
            if key in obj:
                value = obj[key]
                if isinstance(value, str):
                    candidates.add(value)
                elif isinstance(value, dict) and 'url_list' in value:
                    if isinstance(value['url_list'], list):
                        candidates.update([u for u in value['url_list'] if isinstance(u, str)])
                elif isinstance(value, list):
                    candidates.update([u for u in value if isinstance(u, str)])
        
        # Recurse through all values
        for value in obj.values():
            extract_urls_from_json(value, candidates)
            
    elif isinstance(obj, list):
        for item in obj:
            extract_urls_from_json(item, candidates)

def main():
    """Main function to process batch of URLs"""
    input_file = 'input.txt'
    output_file = 'output.txt'
    
    print(f"Reading URLs from {input_file}...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    except FileNotFoundError:
        print(f"Error: {input_file} not found!")
        print("Please create an input.txt file with one m.douyin.com URL per line.")
        return
    
    if not urls:
        print("No URLs found in input.txt")
        return
    
    print(f"Found {len(urls)} URLs to process")
    
    results = []
    
    for i, url in enumerate(urls, 1):
        print(f"\nProcessing {i}/{len(urls)}: {url}")
        
        # Skip non-douyin URLs
        if 'douyin' not in url:
            print("  → Skipping (not a douyin URL)")
            results.append("no-thumbnail.com")  # Placeholder for skipped URLs
            continue
        
        thumbnail = extract_thumbnail(url)
        
        if thumbnail:
            print(f"  → Found thumbnail: {thumbnail[:60]}...")
            results.append(thumbnail)
        else:
            print("  → No thumbnail found")
            results.append("no-thumbnail.com")  # Placeholder for failed extractions
        
        # Small delay to be polite to the server
        if i < len(urls):
            time.sleep(1)
    
    # Save results
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(results))
    
    print(f"\n✅ Done! Results saved to {output_file}")
    print(f"Successfully extracted {len(results)} thumbnails out of {len(urls)} URLs")

if __name__ == "__main__":
    main()
