# Mapping Gov Priorities Using NLP and MTP

Goal of this project is to compare two methods for mapping government priorities in Orange County North Carolina: Natural Language Processing for text summarization and Meaning-Typed Programming LLM summarization.

Created using assistance from Gemini AI. 

## Initial_scrape.py 
A simple BFS site spider using curl_cffi.requesets and BeautifulSoup that crawls a list of municipality homepages, extracts unique paragraph-like text blocks, skips common binary assets and PDFs (tracking skipped PDF URLs), rate-limits requests, and writes results to municipality_spider_data.json and skipped_pdfs.json. 