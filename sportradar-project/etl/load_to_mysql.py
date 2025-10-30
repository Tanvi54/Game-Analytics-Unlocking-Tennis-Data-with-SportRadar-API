import os
import json
import pandas as pd
from sqlalchemy import create_engine, text

# ----------------------------
# 1️⃣  Database Configuration
# ----------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Tanp#1816@localhost/sport_radar")

print(f"✅ Connected to Database: {DATABASE_URL}")

# Setup SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Define your JSON folder path
data_dir = os.path.join(os.path.dirname(__file__), "../sample_json")
print(f"ℹ️ Using data directory: {os.path.abspath(data_dir)}")

# ----------------------------
# 2️⃣  Helper Function
# ----------------------------
def load_json(filename):
    file_path = os.path.join(data_dir, filename)
    if not os.path.exists(file_path):
        print(f"❌ Missing file: {filename}")
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# ----------------------------
# 3️⃣  Load the JSON files
# ----------------------------
competitions_json = load_json("competitions.json")
complexes_json = load_json("complexes.json")
doubles_json = load_json("doubles_rankings.json")

# ----------------------------
# 4️⃣  Drop & Create Tables
# ----------------------------
with engine.begin() as conn:
    print("🧹 Dropping existing tables (disabling FK checks)...")
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    for tbl in ["competitor_rankings", "competitors", "venues", "complexes", "competitions", "categories"]:
        conn.execute(text(f"DROP TABLE IF EXISTS {tbl}"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    # Create tables
    print("✅ Creating fresh tables...")
    conn.execute(text("""
    CREATE TABLE categories (
        category_id VARCHAR(50) PRIMARY KEY,
        category_name VARCHAR(255)
    );
    """))

    conn.execute(text("""
    CREATE TABLE competitions (
        competition_id VARCHAR(50) PRIMARY KEY,
        competition_name VARCHAR(255),
        category_id VARCHAR(50),
        type VARCHAR(50),
        gender VARCHAR(50),
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    """))

    conn.execute(text("""
    CREATE TABLE complexes (
        complex_id VARCHAR(50) PRIMARY KEY,
        complex_name VARCHAR(255)
    );
    """))

    conn.execute(text("""
    CREATE TABLE venues (
        venue_id VARCHAR(50) PRIMARY KEY,
        venue_name VARCHAR(255),
        city_name VARCHAR(255),
        country_name VARCHAR(255),
        country_code VARCHAR(10),
        timezone VARCHAR(100),
        complex_id VARCHAR(50),
        FOREIGN KEY (complex_id) REFERENCES complexes(complex_id)
    );
    """))

    conn.execute(text("""
    CREATE TABLE competitors (
        competitor_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(255),
        country VARCHAR(100),
        country_code VARCHAR(10)
    );
    """))

    conn.execute(text("""
    CREATE TABLE competitor_rankings (
        rank_id INT AUTO_INCREMENT PRIMARY KEY,
        competitor_id VARCHAR(50),
        rank_position INT,
        movement INT,
        points INT,
        competitions_played INT,
        FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
    );
    """))
print("✅ Tables created successfully.")

# ----------------------------
# 5️⃣  Transform & Load Data
# ----------------------------

## Categories and Competitions
categories_data = []
competitions_data = []

if competitions_json and "competitions" in competitions_json:
    for comp in competitions_json["competitions"]:
        cat = comp.get("category", {})
        if cat:
            categories_data.append({
                "category_id": cat.get("id"),
                "category_name": cat.get("name")
            })
        competitions_data.append({
            "competition_id": comp.get("id"),
            "competition_name": comp.get("name"),
            "category_id": cat.get("id") if cat else None,
            "type": comp.get("type"),
            "gender": comp.get("gender")
        })

categories_df = pd.DataFrame(categories_data).drop_duplicates(subset=["category_id"])
competitions_df = pd.DataFrame(competitions_data)

## Complexes & Venues
complexes_data, venues_data = [], []
if complexes_json and "complexes" in complexes_json:
    for comp in complexes_json["complexes"]:
        complexes_data.append({
            "complex_id": comp.get("id"),
            "complex_name": comp.get("name")
        })
        for v in comp.get("venues", []):
            venues_data.append({
                "venue_id": v.get("id"),
                "venue_name": v.get("name"),
                "city_name": v.get("city_name"),
                "country_name": v.get("country_name"),
                "country_code": v.get("country_code"),
                "timezone": v.get("timezone"),
                "complex_id": comp.get("id")
            })

complexes_df = pd.DataFrame(complexes_data)
venues_df = pd.DataFrame(venues_data)

## Competitors & Rankings
competitors_data, rankings_data = [], []

if doubles_json and "rankings" in doubles_json:
    for ranking_group in doubles_json["rankings"]:
        for r in ranking_group.get("competitor_rankings", []):
            competitor = r.get("competitor", {})
            if competitor:
                competitors_data.append({
                    "competitor_id": competitor.get("id"),
                    "name": competitor.get("name"),
                    "country": competitor.get("country"),
                    "country_code": competitor.get("country_code")
                })
                rankings_data.append({
                    "competitor_id": competitor.get("id"),
                    "rank_position": r.get("rank"),
                    "movement": r.get("movement"),
                    "points": r.get("points"),
                    "competitions_played": r.get("competitions_played")
                })

competitors_df = pd.DataFrame(competitors_data).drop_duplicates(subset=["competitor_id"])
rankings_df = pd.DataFrame(rankings_data)

# ----------------------------
# 6️⃣  Insert into MySQL
# ----------------------------
with engine.begin() as conn:
    if not categories_df.empty:
        categories_df.to_sql("categories", conn, if_exists="append", index=False)
        print(f"✅ Inserted {len(categories_df)} rows into categories")

    if not complexes_df.empty:
        complexes_df.to_sql("complexes", conn, if_exists="append", index=False)
        print(f"✅ Inserted {len(complexes_df)} rows into complexes")

    if not competitions_df.empty:
        competitions_df.to_sql("competitions", conn, if_exists="append", index=False)
        print(f"✅ Inserted {len(competitions_df)} rows into competitions")

    if not venues_df.empty:
        venues_df.to_sql("venues", conn, if_exists="append", index=False)
        print(f"✅ Inserted {len(venues_df)} rows into venues")

    if not competitors_df.empty:
        competitors_df.to_sql("competitors", conn, if_exists="append", index=False)
        print(f"✅ Inserted {len(competitors_df)} rows into competitors")
    else:
        print("⚠️ No data to insert into competitors.")

    if not rankings_df.empty:
        rankings_df.to_sql("competitor_rankings", conn, if_exists="append", index=False)
        print(f"✅ Inserted {len(rankings_df)} rows into competitor_rankings")
    else:
        print("⚠️ No data to insert into competitor_rankings.")

print("\n🎉 All data loaded and relationships set successfully!")
