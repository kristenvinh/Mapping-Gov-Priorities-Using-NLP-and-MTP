import json
import re

# Stopwords
ENGLISH_STOPWORDS = {
    "the", "and", "a", "to", "of", "in", "i", "is", "that", "it", "on",
    "you", "this", "for", "but", "with", "are", "have", "be", "at", "or",
    "as", "was", "so", "if", "out", "not", "by", "an", "from", "they", "we"
}

# Text Quality Filter -- set cleaning parameters to reduce characters fed to NLP or MTP 
#1. Excludes paragraphs if the average word length is < 3 or greater than 12
#2. Excludes paragraphs if the ratio of symbols to words is greater than 0.1/
#3. Excludes paragraphs if the number of stop words is less than 2.

def passes_text_quality_filter(text: str) -> bool:
    """Evaluates text against Rae et al. (2021) heuristics."""
    clean_words = re.findall(r'\b\w+\b', text.lower())
    num_words = len(clean_words)

    if num_words == 0:
        return False

    # 1. Word Length Analysis
    total_chars = sum(len(word) for word in clean_words)
    avg_word_length = total_chars / num_words
    if not (3 <= avg_word_length <= 12):
        return False

    # 2. Symbol-to-Word Ratio
    num_symbols = len(re.findall(r'[^\w\s]', text))
    symbol_ratio = num_symbols / num_words
    if symbol_ratio > 0.15:
        return False

    # 3. Stopword Presence
    stopword_count = sum(1 for word in clean_words if word in ENGLISH_STOPWORDS)
    if stopword_count < 2:
        return False

    return True

def clean_municipality_json(input_filepath: str, output_filepath: str):
    """Loads a JSON file, filters the text strings, and saves a cleaned version."""
    
    # Load the raw JSON data
    # Load the raw JSON data
    with open(input_filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    cleaned_data = {}
    
    # Iterate through the dictionary keys (e.g., "Mebane") and their subpages
    for municipality, url_data in data.items():
        # Initialize the municipality in our clean dictionary
        cleaned_data[municipality] = {}
        
        for url, text_list in url_data.items():
            cleaned_paragraphs = []
            
            # Apply the filter to each string element in the list
            for text_snippet in text_list:
                if passes_text_quality_filter(text_snippet):
                    cleaned_paragraphs.append(text_snippet)
                    
            # NEW: Only store the URL if there is actually cleaned text left
            if len(cleaned_paragraphs) > 0:
                cleaned_data[municipality][url] = cleaned_paragraphs
            
            # Print statistics
            print(f"[{url}] Processed {len(text_list)} raw strings.")
            print(f"[{url}] Kept {len(cleaned_paragraphs)} clean strings.")
            
        # Optional: If a municipality ended up with ZERO valid URLs, you can remove it entirely
        if not cleaned_data[municipality]:
            del cleaned_data[municipality]

    # Save the cleaned data to a new JSON file
    with open(output_filepath, 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, indent=4)

# --- Example Usage ---
if __name__ == "__main__":
    # Replace these with your actual file paths
    INPUT_FILE = 'municipality_spider_data.json'
    OUTPUT_FILE = 'cleaned_municipality_spider_data.json'
    
    clean_municipality_json(INPUT_FILE, OUTPUT_FILE)