#Import necessary libraries
import from typing { Optional }
import from datetime { datetime }
import time;
import json;


enum PolicyPriorityArea {
    HOUSING = "affordable housing and zoning",
    ENVIRONMENTAL_RESILIENCE = "climate action and clean energy",
    ECONOMIC_DEVELOPMENT = "job creation and business support",
    COMMUNITY_SAFETY = "police, fire, and emergency response",
    TRANSIT_INFRASTRUCTURE = "public transportation and roads",
    PARKS_AND_CULTURE = "parks, recreation, and public art",
    PUBLIC_ADMINISTRATION = "town governance, human resources, and board appointments",
    PUBLIC_WORKS = "waste management, stormwater, and infrastructure",
    CODE_ENFORCEMENT = "building permits, inspections, and local ordinances",
    UNKNOWN = "uncategorized initiatives"
}

obj PolicyInitiative {
    has municipality_name: str;
    has topic_id: int;                        # NEW: Links the LLM extraction back to the BERTopic cluster
    has primary_category: PolicyPriorityArea;
    has representation: list[str];            # NEW: The BERTopic keyword list you requested
    has budget_allocation: float | None;
    has impacted_stakeholders: list[str];     # NEW: Identifies who the policy affects (e.g., "Homeowners", "Contractors")
    has summary: str;
    has related_doc_count: int;
}

sem extract_initiatives = """
Analyze the input text and extract policy initiatives.
Return a list of PolicyInitiative objects.
""";

def extract_initiatives(web_text: str) -> list[PolicyInitiative] by llm();

with entry {
    file_path = 'mtp_representative_docs.json';
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S");
    export_path = f"extracted_initiatives_{timestamp}.json";
    
    file_content = open(file_path, "r").read();
    _list = json.loads(file_content);
    
    output_data = [];

    start_index = 150; # Change this to the index you want to resume from (0-based). For example, if you want to start from the 151st document, set it to 150. Helpful if the LLM call fails and you want to resume without reprocessing everything.
    
    # Define how many documents to send in a single LLM call
    batch_size = 10; 

    print(f"Resuming extraction from document {start_index + 1} with a batch size of {batch_size}...");
    
    try {
        # NEW: The range function now jumps forward by 'batch_size' each loop
        for i in range(start_index, len(_list), batch_size) {
            
            # Calculate where this current batch ends
            end_index = i + batch_size;
            if end_index > len(_list) {
                end_index = len(_list);
            }
            
            print(f"Processing documents {i+1} to {end_index} of {len(_list)}...");
            
            # Slice the list to grab just the current batch of documents
            batch_list = _list[i:end_index];
            chunk_str = json.dumps(batch_list);
            
            # Send the whole batch to the LLM at once
            extracted = extract_initiatives(chunk_str);
            
            if extracted {
                for init in extracted {
                    output_data.append({
                        "municipality_name": init.municipality_name,
                        "topic_id": init.topic_id,
                        "primary_category": init.primary_category.value,
                        "representation": init.representation,
                        "budget_allocation": init.budget_allocation,
                        "impacted_stakeholders": init.impacted_stakeholders,
                        "summary": init.summary,
                        "related_doc_count": init.related_doc_count
                    });
                }
                
                # Autosave after every batch
                with open(export_path, 'w') as f {
                    json.dump(output_data, f, indent=4);
                }
            }
            
            print("Sleeping to respect rate limits...");
            time.sleep(13); 
        }
        print(f"Done! All data saved to {export_path}");

    } except Exception as e {
        print(f"\n[!] Error encountered at index {i}: {e}");
        print(f"[!] Progress saved in {export_path}. To resume, set start_index to {i}.");
    }
}