import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer

with open('cleaned_municipality_spider_data.json', 'r') as file:
    spider_data = json.load(file)

embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
municipality_models = {}

for municipality, texts in spider_data.items():
    # 1. Filter valid texts for just this municipality
    valid_texts = [text.strip() for text in texts if isinstance(text, str) and text.strip()]
    doc_count = len(valid_texts)
    
    print(f"\nProcessing {municipality} ({doc_count} documents)...")
    
    # Safety Check: Skip if there isn't enough data to cluster
    if doc_count < 5:
        print(f"Skipping {municipality} - not enough data for HDBSCAN.")
        continue

    # 2. Encode just this municipality's documents
    embeddings = embedding_model.encode(valid_texts, show_progress_bar=False)

    # 3. Dynamically scale parameters based on document count
    # UMAP n_neighbors must be less than the total document count
    neighbors = min(15, doc_count - 1) if doc_count > 2 else 2
    
    # HDBSCAN cluster size must be small enough to find groups in small samples
    cluster_size = min(10, max(2, doc_count // 3)) 

    # 4. Re-instantiate the models inside the loop to clear previous state
    umap_model = UMAP(n_neighbors=neighbors, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
    hdbscan_model = HDBSCAN(min_cluster_size=cluster_size, metric='euclidean', cluster_selection_method='eom', prediction_data=True)


    # Create a vectorizer that removes common English stop words
    vectorizer_model = CountVectorizer(stop_words="english")
    
    topic_model = BERTopic(
        embedding_model=embedding_model,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer_model,
        language="multilingual"
    )

    # 5. Fit the isolated model
    topics, probabilities = topic_model.fit_transform(valid_texts, embeddings)
    
    # Store the results and the model for later inspection
    municipality_models[municipality] = {
        "model": topic_model,
        "info": topic_model.get_topic_info()
    }
    
    print(municipality_models[municipality]["info"].head(3))

all_results = []

# Iterate through the dictionary to extract the topic info
for municipality, data in municipality_models.items():
    # Make a copy of the dataframe so we don't alter the original
    df_info = data["info"].copy() 
    
    # Add a column so we know which municipality these topics belong to
    df_info['Municipality'] = municipality 
    
    all_results.append(df_info)

# Combine them all into one master dataframe
final_results_df = pd.concat(all_results, ignore_index=True)

# 1. Save the combined dataframe to CSV
final_results_df.to_csv('independent_models_results.csv', index=False)

# 2. Save the combined dataframe to JSON
final_results_df.to_json('independent_models_results.json', orient='records', indent=4)