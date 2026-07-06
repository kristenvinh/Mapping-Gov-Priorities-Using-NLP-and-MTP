# WEEK 3 DEMO: Mapping Gov Priorities Using NLP and MTP

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

### Add census.py to fetch demographic data from the American Community Survey API for Orange County and nearby NC cities. 

Includes variables for housing, commuting, broadband access, income, population, and race/ethnicity. Adds acs_demographics.csv with the fetched baseline data. 
---

## What challenges did you encounter?
* **Census Data Issues:** Pulling from the Census API Data was buggy. 
* **Mitigation:** Eventually got it to work by pulling by FIPS codes.

---

## What’s next?  

### Conduct the Gap and Mismatch Analysis (Day 4)
Analyze the data for misalignments between public communication and demographic realities.

Identify Policy Gaps: A gap exists if objective indicators of community need are high (e.g., low broadband access or high poverty) but the local government's extracted priorities rarely mention it.

Spatial Mismatch: Look for signs of spatial mismatch, such as transit strategies that do not align with the neighborhoods experiencing the highest rates of public transit reliance or job sprawl.

Urban vs. Rural Divide: Evaluate if the stated priorities shift significantly based on the population size of the municipality, and whether those shifts are justified by the census data.

### Visualize and Synthesize Findings (Day 5)
Translate your findings into a visual format. Use GIS mapping tools to overlay the quantitative census data (like median income or cost burden) with your qualitative MTP data (like the presence of specific catalytic projects or strategic goals). This will provide a concise, accessible presentation of where local governance aligns perfectly with community needs and where significant policy gaps remain.