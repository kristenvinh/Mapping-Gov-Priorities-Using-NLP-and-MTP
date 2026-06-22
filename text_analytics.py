import json
import numpy as np
import pandas as pd

def calculate_gini(array):
    """
    Calculates the Gini coefficient of a numpy array.
    A Gini of 0 means perfect equality (all municipalities have the same amount of text).
    A Gini of 1 means maximal inequality (one municipality has all the text).
    """
    array = np.array(array, dtype=np.float64).flatten()
    if np.amin(array) < 0:
        array -= np.amin(array) # Values cannot be negative
    array += 0.0000001 # Prevent zero-division
    array = np.sort(array)
    index = np.arange(1, array.shape[0] + 1)
    n = array.shape[0]
    return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

def generate_table_1(raw_json_path, cleaned_json_path):
    # 1. Load the data
    with open(raw_json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    with open(cleaned_json_path, 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)

    municipalities = list(raw_data.keys())
    N = len(municipalities)

    # 2. Initialize counters
    raw_para_counts = []
    cleaned_para_counts = []
    raw_word_counts = []
    cleaned_word_counts = []

    # 3. Extract metrics per municipality
    for muni in municipalities:
        # Raw Data Extraction
        raw_texts = raw_data.get(muni, [])
        raw_para_counts.append(len(raw_texts))
        
        # Simple word count approximation (splitting by whitespace)
        raw_words = sum(len(text.split()) for text in raw_texts)
        raw_word_counts.append(raw_words)

        # Cleaned Data Extraction
        cleaned_texts = cleaned_data.get(muni, [])
        cleaned_para_counts.append(len(cleaned_texts))
        
        cleaned_words = sum(len(text.split()) for text in cleaned_texts)
        cleaned_word_counts.append(cleaned_words)

    # 4. Calculate Averages and Gini
    stats = {
        "Metric": [
            f"Government Websites (N = {N})",
            "Average amount of text paragraphs (per unit)",
            "Average amount of cleaned text paragraphs (per unit)",
            "Average amount of words [RAW] (per unit)",
            "Average amount of words [CLEANED] (per unit)",
            "Gini of cleaned text paragraphs"
        ],
        "Value": [
            N,
            round(np.mean(raw_para_counts), 2),
            round(np.mean(cleaned_para_counts), 2),
            round(np.mean(raw_word_counts), 2),
            round(np.mean(cleaned_word_counts), 2),
            round(calculate_gini(cleaned_para_counts), 2)
        ]
    }

    # 5. Format as a clean table using Pandas
    df = pd.DataFrame(stats)
    print("Description of the processed data ---")
    print(df.to_string(index=False))
    
    # Export to CSV for inclusion in a report
    df.to_csv('summary_average_stats.csv', index=False)

if __name__ == "__main__":
    # Ensure these paths match where your files are located
    RAW_FILE = 'municipality_spider_data.json'
    CLEAN_FILE = 'cleaned_municipality_spider_data.json'
    
    generate_table_1(RAW_FILE, CLEAN_FILE)