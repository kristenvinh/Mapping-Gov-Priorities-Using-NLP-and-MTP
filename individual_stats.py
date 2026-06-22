import json
import pandas as pd

def generate_municipality_breakdown(raw_json_path, cleaned_json_path):
    # Load the data
    with open(raw_json_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
        
    with open(cleaned_json_path, 'r', encoding='utf-8') as f:
        cleaned_data = json.load(f)

    # Initialize a list to hold the row dictionaries
    metrics_list = []

    # Get the complete list of municipalities
    municipalities = list(raw_data.keys())

    for muni in municipalities:
        # Extract lists
        raw_texts = raw_data.get(muni, [])
        cleaned_texts = cleaned_data.get(muni, [])
        
        # Calculate paragraph counts
        raw_para_count = len(raw_texts)
        cleaned_para_count = len(cleaned_texts)
        
        # Calculate word counts (using simple whitespace split)
        raw_word_count = sum(len(text.split()) for text in raw_texts)
        cleaned_word_count = sum(len(text.split()) for text in cleaned_texts)
        
        # Calculate retention percentages safely to avoid division by zero
        para_retention = (cleaned_para_count / raw_para_count * 100) if raw_para_count > 0 else 0
        word_retention = (cleaned_word_count / raw_word_count * 100) if raw_word_count > 0 else 0

        # Append the municipality's stats to our list
        metrics_list.append({
            "Municipality": muni,
            "Raw Paragraphs": raw_para_count,
            "Cleaned Paragraphs": cleaned_para_count,
            "% Paragraphs Kept": round(para_retention, 2),
            "Raw Words": raw_word_count,
            "Cleaned Words": cleaned_word_count,
            "% Words Kept": round(word_retention, 2)
        })

    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(metrics_list)
    
    # Sort alphabetically by municipality for cleaner reading
    df = df.sort_values(by="Municipality").reset_index(drop=True)
    
    # Display the results
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print("\n--- Municipality Data Extraction Breakdown ---")
    print(df.to_string())
    
    # Export to CSV for further analysis or reporting
    export_filename = 'municipality_counts_breakdown.csv'
    df.to_csv(export_filename, index=False)
    print(f"\nDetailed breakdown saved to: {export_filename}")

if __name__ == "__main__":
    # Ensure these paths match your local environment
    RAW_FILE = 'municipality_spider_data.json'
    CLEAN_FILE = 'cleaned_municipality_spider_data.json'
    
    generate_municipality_breakdown(RAW_FILE, CLEAN_FILE)