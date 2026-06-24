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
    if isinstance(texts, dict):
        raw_texts = [
            text
            for text_list in texts.values()
            if isinstance(text_list, list)
            for text in text_list
        ]
    elif isinstance(texts, list):
        raw_texts = texts
    else:
        raw_texts = []

    # 1. Filter valid texts for just this municipality
    valid_texts = [text.strip() for text in raw_texts if isinstance(text, str) and text.strip()]
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
    mtp_extraction_data = []    # New list specifically for Stage 2 (MTP)

    for municipality, data in municipality_models.items():
        topic_model = data["model"]
        df_info = data["info"].copy()
        
        # Standard export data
        df_info['Municipality'] = municipality
        all_results.append(df_info)
        
        # --- NEW: Extract Representative Docs for MTP ---
        # This returns a dictionary of {topic_id: [doc1, doc2, doc3]}
        rep_docs_dict = topic_model.get_representative_docs()
        
        for topic_id, docs in rep_docs_dict.items():
            # Skip the outlier/noise topic, which BERTopic always labels as -1
            if topic_id == -1:
                continue
                
            # Grab the BERTopic generated name for context
            topic_name = str(df_info[df_info['Topic'] == topic_id]['Name'].iloc[0])
            
            # Extract the Representation column (which is a list of keywords)
            # We wrap it in list() just to be absolutely certain it is JSON-serializable
            topic_representation = list(df_info[df_info['Topic'] == topic_id]['Representation'].iloc[0])
            
            # Structure the data perfectly for your LLM batching
            mtp_extraction_data.append({
                "municipality": municipality,
                "topic_id": int(topic_id),
                "topic_name": topic_name,
                "representation": topic_representation,  # <--- NEW FIELD ADDED HERE
                "representative_documents": docs 
            })

    # Combine and save the standard topic metadata
    final_results_df = pd.concat(all_results, ignore_index=True)
    final_results_df.to_csv('independent_models_results.csv', index=False)
    final_results_df.to_json('independent_models_results.json', orient='records', indent=4)

    # Save the isolated representative documents for the byLLM extraction phase
    with open('mtp_representative_docs.json', 'w', encoding='utf-8') as f:
        json.dump(mtp_extraction_data, f, indent=4)
        
    print("Success! Created 'mtp_representative_docs.json' for the MTP pipeline.")