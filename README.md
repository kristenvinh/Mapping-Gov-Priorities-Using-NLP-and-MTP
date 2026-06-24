# Mapping Gov Priorities Using NLP and MTP

Goal of this project is to compare two methods for mapping government priorities in Orange County North Carolina: Natural Language Processing for text summarization and Meaning-Typed Programming LLM summarization.

Created using assistance from Gemini AI. 

## initial_scrape.py 
A simple BFS site spider using curl_cffi.requests and BeautifulSoup that crawls a list of municipality homepages, extracts unique paragraph-like text blocks, skips common binary assets and PDFs (tracking skipped PDF URLs), rate-limits requests, and writes results to municipality_spider_data.json and skipped_pdfs.json. 

## json_cleaning.py
Cleans the JSON file using the following cleaning parameters to reduce characters fed to NLP or MTP: 
1. Excludes paragraphs if the average word length is < 3 or greater than 12
2. Excludes paragraphs if the ratio of symbols to words is greater than 0.1/
3. Excludes paragraphs if the number of stop words is less than 2.

## individual_stats.py
Calculates the statistics per municipality for:
- Raw subpages vs. cleaned subpages
- Raw paragraphs vs. cleaned paragraphs
- Raw words vs. cleaned words

Outputs file to municpality_counts_breakdown.csv

## text_analytics.py
Calculates the average statistics for:
- Raw subpages vs. cleaned subpages
- Raw paragraphs vs. cleaned paragraphs
- Raw words vs. cleaned words

Also calculates the gini index of the cleaned paragraphs:
    A Gini of 0 means perfect equality (all municipalities have the same amount of text).
    A Gini of 1 means maximal inequality (one municipality has all the text).

Outputs file to summary_average_stats.csv