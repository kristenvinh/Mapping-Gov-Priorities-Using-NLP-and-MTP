# Mapping Gov Priorities Using NLP and MTP

Goal of this project is to map government priorities in Orange County North Carolina using Natural Language Processing for text summarization and Meaning-Typed Programming to extract government priorities.

Created using assistance from Gemini AI. 

## Files Prepping for BERTopic

Before running BERTopic modeling on the municipality website text, the text must be scraped from the various government websites in Orange County, NC, cleaned, and then analyzed. 

### initial_scrape.py 
A simple BFS site spider using curl_cffi.requests and BeautifulSoup that crawls a list of municipality homepages, extracts unique paragraph-like text blocks, skips common binary assets and PDFs (tracking skipped PDF URLs), rate-limits requests, and writes results to municipality_spider_data.json and skipped_pdfs.json. 

### json_cleaning.py
Cleans the JSON file using the following cleaning parameters to reduce characters fed to NLP or MTP: 
1. Excludes paragraphs if the average word length is < 3 or greater than 12
2. Excludes paragraphs if the ratio of symbols to words is greater than 0.1/
3. Excludes paragraphs if the number of stop words is less than 2.

### individual_stats.py
Calculates the statistics per municipality for:
- Raw subpages vs. cleaned subpages
- Raw paragraphs vs. cleaned paragraphs
- Raw words vs. cleaned words

Outputs file to municpality_counts_breakdown.csv

### text_analytics.py
Calculates the average statistics for:
- Raw subpages vs. cleaned subpages
- Raw paragraphs vs. cleaned paragraphs
- Raw words vs. cleaned words

Also calculates the gini index of the cleaned paragraphs:
    A Gini of 0 means perfect equality (all municipalities have the same amount of text).
    A Gini of 1 means maximal inequality (one municipality has all the text).

Outputs file to summary_average_stats.csv

## BERTopic Modeling - BERT.py
Here, SBERT is used to do topic modeling to further reduce and organize the text from the municipality websites before feeding them to an LLM using MTP. 

First, it initializes a multilingual SBERT model (paraphrase-multilingual-MiniLM-L12-v2) to handle text encoding and sets up an empty dictionary to track the topic models for each municipality.

Then it initializes a loop to process the data from each municipality:
1. It flattens the lists of text, strips out empty strings, and checks if there are at least 5 valid documents to ensure HDBSCAN clustering won't fail.
2. It converts the valid text strings into dense semantic vectors using SBERT.
3. To prevent crashes on smaller datasets, it dynamically scales the parameters for UMAP (dimensionality reduction) and HDBSCAN (clustering) based on the exact number of documents available for that specific municipality.
4. It initializes a CountVectorizer to remove English stopwords, builds the BERTopic model, fits it to the text embeddings, and extracts the topic metadata.
5. it takes the topic dataframes generated for each municipality, adds a column specifying the municipality name, merges them into one master dataset, and exports the results to both CSV and JSON formats. It also creates a JSON export made to be fed to the LLM using MTP that:
- Skip the outlier/noise topic, labeled as -1
- Gets the topic name, id, keywords and the paragraphs that were representative of that topic