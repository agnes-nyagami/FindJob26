## Agentic Job Search System
This project is an agentic job search system designed to identify job openings at companies with verified visa sponsorship history. It combines resume parsing, historical sponsorship data, and live job scraping into a deterministic, sponsor-aware pipeline powered by CrewAI and MCP servers.  
'''text  
+----------------------+
|        User          |
|  Query + Resume      |
+----------+-----------+
           |
           v
+----------------------+
|     Parser Agent     |
|  - role              |
|  - city/state        |
|  - skills            |
+----------+-----------+
           |
           v
+----------------------+        +--------------------------+
|    Sponsor Agent     | -----> |   Sponsorship MCP        |
|  (filters sponsors)  |        | (historical approvals)   |
+----------+-----------+        +--------------------------+
           |
           v
+----------------------+
|      Job Agent       |
|  (sponsor-only)      |
+----------+-----------+
           |
           v
+----------------------+        +--------------------------+
|   JobSpy MCP Server  | <----> |  Indeed / LinkedIn / ZR  |
| (live job scraping)  |        |  (via python-jobspy)     |
+----------+-----------+
           |
           v
+----------------------+
|  Sponsored Job List  |
+----------------------+  
'''
# 🧩 Architecture Overview  
1️⃣ Parser Agent -This agent converts unstructured inputs into structured job intent.  
'''bash  
Input:  
- User free-text query  
- Resume text  
'''
Output:  
- Target job role  
- City & state  
- Extracted technical skills  
- Role-relevant keywords  
    
2️⃣ Sponsor Agent - This ensures all downstream job searches are sponsor-verified.  

Input:  
- City and state from the parser agent  

Action:  
- Queries a Sponsorship MCP server backed by historical visa approval data  

Output:  
- Deduplicated list of employers with prior sponsorship approvals in the specified location  

3️⃣ Job Agent - Jobs are filtered post-scrape to guarantee employer validity.  

Input:  
- Job role (from parser agent)   
- Employer list (from sponsor agent)  
- Location  

Action:  
- Queries a JobSpy MCP server that scrapes live job postings  

Output:  
- Active job openings only at sponsoring companies    

# 🔌 MCP Servers    
🔹 Sponsorship MCP  
- Serves historical visa sponsorship data  
- Normalizes employer names  
- Filters by city/state  
- Acts as a hard gatekeeper for sponsor eligibility  

🔹 JobSpy MCP  
- Wraps python-jobspy behind an MCP interface  
- Scrapes Indeed, LinkedIn, and ZipRecruiter  
Requires:  
- role  
- location  
- non-empty sponsor employer list   

# 🛠️ Tech Stack  
CrewAI – agent orchestration  
MCP (FastMCP) – tool & data servers  
SQLITE - database management   
python-jobspy – live job scraping  
Pandas – data handling  
Python 3.10+  


