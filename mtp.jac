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
    # 1. Define input file
    file_path = 'mtp_representative_docs.json';
    
    # 2. Generate a unique, timestamped filename
    # This will result in something like: extracted_2026-06-24_14-45-05.json
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S");
    export_path = f"extracted_initiatives_{timestamp}.json";
    
    # 3. Read input
    file_content = open(file_path, "r").read();
    _list = json.loads(file_content);
    
    output_data = [];

    # CHANGE THIS NUMBER to the index where it failed.

    start_index = 12; 

    print(f"Resuming extraction from document {start_index + 1}...");

    print(f"Starting extraction to file: {export_path}");
    
    try {
        for i in range(start_index, len(_list)) {
            print(f"Processing document {i+1} of {len(_list)}...");
            
            chunk_str = json.dumps(_list[i]);
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
                
                # Overwrite the timestamped file as we go
                with open(export_path, 'w') as f {
                    json.dump(output_data, f, indent=4);
                }
            }
            # Sleep for 13 seconds between requests. 
            # 60 seconds / 13 seconds = ~4.6 requests per minute.
            # This keeps you safely under the 5 RPM limit.
            print("Sleeping to respect rate limits...");
            time.sleep(13);
        }
        print(f"Done! All data saved to {export_path}");

    } except Exception as e {
        print(f"\n[!] Error encountered at index {i}: {e}");
        print(f"[!] Progress saved in {export_path}.");
    }
}