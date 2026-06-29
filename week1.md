# WEEK 1 DEMO: Mapping Gov Priorities Using NLP and MTP

---

## What are you building?
I’m building a data-scraping project, **Mapping Gov Priorities Using NLP and MTP**, that will compare two pipelines for scraping the core priorities of municipal governments in my region.[cite: 3]

### Core Pipeline Foundation:
Both pipelines begin by using `curl_cffi`, `requests`, and `BeautifulSoup` to crawl a list of municipality homepages, extract unique paragraph-like text blocks, skip common binary assets and PDFs (tracking skipped PDF URLs), rate-limit requests, and write results to JSON files.[cite: 3]

### Pipeline 1: NLP and BERT Topic Modeling
* Uses NLP and BERT topic modeling to extract the key priorities, likely requiring some human input to further refine the topics after modeling.[cite: 3]
* This idea comes from the paper *"Mapping Local Government Priorities: A Web-Mining Approach for Regional Research,"* which uses this approach to map government priorities in Germany.[cite: 3]
* Additional work will be required to determine which priorities are present in the BERT topics by manually labeling the returned topics with priorities that align with the extracted topics.[cite: 3]

### Pipeline 2: Meaning-Typed Programming (MTP)
* Uses Meaning-Typed Programming, feeding the scraped JSON to the Gemini AI API and asking it to extract priorities.[cite: 3]
* It requires the LLM to return data in an explicit structure representing civic priorities (recommended by Gemini).[cite: 3]
* Additional work will be required here to map priorities by those mentioned most frequently.[cite: 3]

#### Proposed Data Structure:
```jac
enum StrategicCategory: str {
    HOUSING = "affordable housing and zoning",
    ENVIRONMENTAL_RESILIENCE = "climate action and clean energy",
    ECONOMIC_DEVELOPMENT = "job creation and business support",
    COMMUNITY_SAFETY = "police, fire, and emergency response",
    TRANSIT_INFRASTRUCTURE = "public transportation and roads",
    UNKNOWN = "uncategorized initiatives"
}

obj PolicyInitiative {
    has municipality_name: str;
    has primary_category: StrategicCategory;
    has budget_allocation: float | None;
    has summary: str;
}

def extract_initiatives(web_text: str) -> list[PolicyInitiative] by llm();
```[cite: 3]

### Development & Evaluation Approach:
* Both pipelines will be built using AI (primarily Gemini) to help write code quickly, with the goal of learning more about each process and fully understanding how each part works.[cite: 3]
* Evaluation will be based on **development time**, **lines of code**, and **code complexity** to determine whether an easy process can be developed to map priorities (as direct accuracy comparison likely won't be possible).[cite: 3]
* **Timeline:** Anticipate completing pipeline 1 during HYS 1 and pipeline 2 during HYS 2.[cite: 3]
* **Future Scope:** If time allows, I’d like to map how priorities shift across municipalities and analyze how they change relative to different census breakdowns.[cite: 3]

---

## What did you make progress on this week?
* **Project Architecture:** Designed a rough project outline.[cite: 3]
* **Initial Scraping & Crawling:** Used Gemini AI to help write the initial website crawler and ran a test on 100 pages scraped from each website.[cite: 3]
    * *Note: The ultimate goal is 500 pages, but a smaller sample was preferred to run BERTopic on initially.*[cite: 3]

---

## What challenges did you encounter?
* **Token & Data Volume Constraints:** MTP might not be possible given token limits and the need to feed the AI large amounts of data.[cite: 3]
    * *Pivot Plan:* If this occurs, the project might shift to a combination of the two processes (using NLP first, and then MTP on reduced text), with a greater focus on the analysis phase.[cite: 3]
* **MTP Implementation:** Unsure how best to use MTP as it’s not as simple as extracting priorities in a given text; will have to explore MTP usage further and do some experimentation.[cite: 3]

---

## What’s next?
* Testing BERTopic on the smaller sample.[cite: 3]
* Running a full 500-page scrape.[cite: 3]
* Full BERTopic run.[cite: 3]
* Additional MTP brainstorming.[cite: 3]