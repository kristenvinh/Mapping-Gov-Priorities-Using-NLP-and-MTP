# WEEK 2 DEMO: Mapping Gov Priorities Using NLP and MTP

---

## What are you building?
I’m building a data-scraping project, **Mapping Gov Priorities Using NLP and MTP**, that will scrape the core priorities of municipal governments in my region.

### The Process:
1. **Crawling & Scraping:** The process begins using `curl_cffi`, `requests`, and `BeautifulSoup` to crawl a list of municipality homepages, extract unique paragraph-like text blocks, skip common binary assets and PDFs (tracking skipped PDF URLs), rate-limit requests, and write results to JSON files.
2. **Topic Modeling:** The project uses NLP and BERT topic modeling to extract topics from scraped paragraphs. This idea comes from the paper *"Mapping Local Government Priorities: A Web-Mining Approach for Regional Research,"* which uses it to map government priorities in Germany. 
3. **Structured Extraction:** Then, I’ll feed the topic data from BERT to the Gemini AI API and ask it to extract priorities by defining explicit data structures representing civic priorities, requiring the LLM to return the priorities in that explicit structure.
4. **Development Approach:** The project will be built using AI (primarily Gemini) to help write code to move the project along quickly, with the goal of learning more about each process and fully understanding how each part of the project works.
5. **Analysis & Mapping:** I’ll then map how priorities shift across municipalities and analyze how they change relative to different census breakdowns of those municipalities.

---

## What did you make progress on this week?

### 1. Data Collection & Scraping
* Full website crawl and scrape of the four municipal websites and the county website, up to 500 webpages.

### 2. Data Cleaning
A cleaning of the paragraphs of each of the websites, using the following criteria:
* **Word Length:** Excludes paragraphs if the average word length is `< 3` or greater than `12`.
* **Symbol Density:** Excludes paragraphs if the ratio of symbols to words is greater than `0.1`.
* **Stop Words:** Excludes paragraphs if the number of stop words is less than `2`.

### 3. Quick Data Analysis
A quick analysis of the data collected and cleaned per unit:

| Metric | Value |
| :--- | :--- |
| Average amount of subpages | 453.4 |
| Average amount of cleaned subpages | 203 |
| Average amount of text paragraphs | 6,277.6 |
| Average amount of cleaned text paragraphs | 1,991 |
| Average amount of words **[RAW]** | 691,182.8 |
| Average amount of words **[CLEANED]** | 202,139 |
| Gini of cleaned text paragraphs | 0.14 |

### 4. Modeling & Integration
* Ran SBERT to create a list of topics and their related paragraphs for each municipality.
* Drafted a JAC script to begin feeding SBERT topic data to the `byllm()` model.
* Began an initial analysis of the priorities in the different municipalities.

---

## What challenges did you encounter?
* **API Rate Limits:** Encountered rate limits and “busy” limits with the Gemini LLM. 
* **Mitigation:** I had to change how I fed data to the LLM, spread the process over two days, and create multiple data files that I’ll have to compile together later.

---

## What’s next?
* Exploring the data I currently have and going deeper into the analysis.
* Downloading Census data and mapping out priorities against municipal breakdowns.