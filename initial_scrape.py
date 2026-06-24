from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
# Import curl_cffi instead of requests or cloudscraper
from curl_cffi import requests 

TARGET_URLS = {
    "Chapel Hill": "https://www.chapelhillnc.gov/",
    "Carrboro": "https://www.carrboronc.gov/",
    "Hillsborough": "https://www.hillsboroughnc.gov/",
    "Mebane": "https://cityofmebanenc.gov/",
    "Orange County": "https://www.orangecountync.gov/",
}

skipped_pdfs_tracker = {}

def is_valid_link(url, base_domain, municipality_name):
    parsed_url = urlparse(url)
    
    if base_domain not in parsed_url.netloc:
        return False
        
    if url.lower().endswith('.pdf'):
        if municipality_name not in skipped_pdfs_tracker:
            skipped_pdfs_tracker[municipality_name] = []
        
        if url not in skipped_pdfs_tracker[municipality_name]:
            skipped_pdfs_tracker[municipality_name].append(url)
        return False
        
    ignored_extensions = ['.jpg', '.jpeg', '.png', '.doc', '.docx', '.xls', '.xlsx', '.zip']
    if any(url.lower().endswith(ext) for ext in ignored_extensions):
        return False
        
    return True

def spider_municipality(start_url, municipality_name, max_pages=500):
    base_domain = urlparse(start_url).netloc
    queue = [start_url]
    visited = set([start_url])
    
    # NEW: Dictionary to store paragraphs grouped by their specific URL
    site_pages_data = {}
    
    # NEW: Maintain a set to ensure global deduplication across the whole municipality
    seen_paragraphs = set()
    
    pages_scraped = 0

    while queue and pages_scraped < max_pages:
        current_url = queue.pop(0)
        print(f"  [{pages_scraped + 1}/{max_pages}] Scraping: {current_url}")
        
        try:
            response = requests.get(current_url, impersonate="chrome", timeout=15)
            
            # Catch bad status codes manually
            if response.status_code != 200:
                print(f"    Failed with status code: {response.status_code}")
                continue

            if 'text/html' not in response.headers.get('Content-Type', ''):
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')

            for tag in soup(['script', 'style', 'svg', 'nav', 'footer', 'header', 'noscript', 'meta', 'link']):
                tag.decompose()
            
            # Initialize the list for this specific URL
            site_pages_data[current_url] = []
            
            for element in soup.find_all(['p', 'div', 'li']): 
                text = element.get_text(separator=' ', strip=True)
                
                # Check against the global seen_paragraphs set to prevent duplicates
                if len(text) > 30 and text not in seen_paragraphs: 
                    seen_paragraphs.add(text)
                    site_pages_data[current_url].append(text)
            
            # Optional: If a page yielded no valid text blocks, you can choose to remove its key
            # if not site_pages_data[current_url]:
            #     del site_pages_data[current_url]
            
            pages_scraped += 1

            for link in soup.find_all('a', href=True):
                full_url = urljoin(current_url, link['href']).split('#')[0]

                if full_url not in visited and is_valid_link(full_url, base_domain, municipality_name):
                    visited.add(full_url)
                    queue.append(full_url)

        # Broad Exception catch to handle any network timeouts or TLS drops
        except Exception as e:
            print(f"    Error scraping {current_url}: {e}")

        time.sleep(1.5) 

    return site_pages_data

def main():
    spider_results = {}

    for name, start_url in TARGET_URLS.items():
        print(f"\n--- Starting Spider for: {name} ---")
        extracted_data = spider_municipality(start_url, name, max_pages=500) 
        spider_results[name] = extracted_data
        
        # Calculate total text blocks across all subpages for the print readout
        total_blocks = sum(len(paragraphs) for paragraphs in extracted_data.values())
        print(f"Finished {name}. Total text blocks extracted: {total_blocks}")

    with open('municipality_spider_data.json', 'w', encoding='utf-8') as f:
        json.dump(spider_results, f, ensure_ascii=False, indent=4)

    with open('skipped_pdfs.json', 'w', encoding='utf-8') as f:
        json.dump(skipped_pdfs_tracker, f, ensure_ascii=False, indent=4)
        
    print("\nAll spider data successfully saved to municipality_spider_data.json!")

if __name__ == "__main__":
    main()