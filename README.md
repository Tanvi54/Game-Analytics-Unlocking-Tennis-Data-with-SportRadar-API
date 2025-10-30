# 🏆 SportRadar Data Analysis & Dashboard Project

## 📘 Overview
This project implements a **complete data engineering and analytics pipeline** for sports data from the SportRadar dataset.  
It covers everything from **data ingestion (JSON)** → **ETL to MySQL** → **SQL analytics** → **interactive dashboard visualization (Streamlit)**.  

---

## 🎯 Project Objectives
- ✅ Extract structured data from complex JSON files  
- ✅ Build an automated ETL process using Python + MySQL  
- ✅ Perform SQL-based analytics and generate insights  
- ✅ Visualize data through an interactive Streamlit dashboard  

---

## 📂 Project Structure
```bash
sportradar-project/
│
├── etl/
│   ├── app.py                     # Streamlit dashboard for analytics & visualization
│   ├── fetch_competitions.py      # Fetch & transform competitions data from JSON
│   ├── fetch_complexes.py         # Fetch & transform complexes data from JSON
│   ├── fetch_doubles_rankings.py  # Fetch & transform doubles rankings data
│   ├── load_to_mysql.py           # ETL script to load transformed data into MySQL
│   ├── run_queries.py             # Executes SQL analysis queries automatically
│   
├── sample_json/
│       ├── competitions.json      # Raw competitions data
│       ├── complexes.json         # Raw complexes data
│       └── doubles_rankings.json  # Raw player rankings data
│
├── .env                           # Environment variables (DB credentials, API key)
├── requirements.txt               # All Python dependencies
    
```


---

## 🧠 Data Sources
This project uses **three JSON data files** (`sample_json/`) as input:  
- 🏁 `competitions.json` — competition and category info  
- 🏟️ `complexes.json` — complexes and venues info  
- 🧍‍♂️ `doubles_rankings.json` — player stats and rankings  

After transformation, six relational tables are created in **MySQL**:

| Table Name | Description |
|-------------|-------------|
| `categories` | Derived from competition data |
| `competitions` | Sports competitions and metadata |
| `complexes` | Details of sports complexes |
| `venues` | Venue information with location details |
| `competitors` | Player / team information |
| `competitor_rankings` | Ranking and performance metrics |

---

## ⚙️ Setup Instructions

1️⃣ Clone and Open the Project
```bash
git clone <your-repository-url>
cd sportradar-project
```

2️⃣ Create a Virtual Environment
```bash
Copy code
python -m venv venv
venv\Scripts\activate       # (Windows)
source venv/bin/activate    # (Mac/Linux)
```

3️⃣ Install Dependencies
```bash
Copy code
pip install -r requirements.txt
```

4️⃣ Configure Environment Variables
Create a .env file in the root directory:

```bash
Copy code
SPORTRADAR_API_KEY = yourapikeyhere
DATABASE_URL= mysql+pymysql://root:password@localhost/sport_radar   # 🔁 replace with your actual MySQL password
```

🧩 Step 1 — Create Tables in MySQL
Run the schema file to set up tables

🧩 Step 2 — Load Data into MySQL
Execute the ETL script to populate all tables:

```bash
Copy code
python etl/load_to_mysql.py
```

✅ This will:

- Drop existing tables safely

- Recreate new schema

- Load parsed JSON data

- Confirm row counts inserted

🧩 Step 3 — Run Analytical SQL Queries
You can execute queries directly from MySQL Workbench Or run all predefined queries from Python:

```bash
Copy code
python etl/run_queries.py
```

🧩 Step 4 — Launch Streamlit Dashboard
Run the Streamlit app for interactive exploration:

```bash
Copy code
cd etl
streamlit run app.py
```
Then open the provided localhost link (e.g., http://localhost:8501) in your browser.

🖥️ Streamlit Dashboard Features
- 🏠 Homepage Dashboard
   - Total number of competitors

   - Number of countries represented

   - Highest points scored by a competitor


🔍 Competitor Search & Filter
- Search competitors by name

- Filter by rank range, country, or points threshold


🧾 Competitor Details Viewer

- Displays details such as:

    - Rank position

    - Movement

    - Competitions played

    - Country


🌍 Country-Wise Analysis
- List of countries with:

    - Total competitors

    - Average points


🏆 Leaderboards
- Displays top-ranked competitors

- Highest points scorers


🧾 SQL Analysis Highlights
- 🏁 Competitions Analysis
    - Count competitions by category

    - Filter by competition type (e.g., doubles)

    - Identify parent and sub-competitions


- 🏟️ Venue Analysis
    - Venues by complex

    - Venues grouped by country

    - Complexes with multiple venues


- 🧍‍♂️ Competitor Analysis
    - Top 5 ranked competitors

    - Competitors with stable ranks

    - Country-wise performance and points distribution


📊 Example Key Metrics (Dashboard Cards)
| Metric | Description |
|-------------|-------------|
| 🧍 Total Competitors | 1,000 |
| 🌍 Countries Represented| 80 |
| Highest Points | 12,300 |
| ⚖️ Average Rank Movement | ±2 |



📈 Technologies Used
| Category | Tools |
|-------------|-------------|
| Programming Language | Python 3.9+ |
| Database | MySQL Workbench |
| Visualization | Streamlit, Plotly |
| ETL | SQLAlchemy, Pandas |
| Environment Management| python-dotenv |
| Libraries | mysql-connector-python, pymysql |


🎥 Demo Walkthrough
- Run ETL: python etl/load_to_mysql.py

- Verify Tables: Using MySQL Workbench

- Execute Queries: SOURCE queries.sql

- Launch Dashboard: streamlit run app.py

- Explore: Interactive leaderboards, country filters, and insights

🧾 Requirements
```bash
Copy code
streamlit
pandas
sqlalchemy
pymysql
mysql-connector-python
plotly
python-dotenv
```
