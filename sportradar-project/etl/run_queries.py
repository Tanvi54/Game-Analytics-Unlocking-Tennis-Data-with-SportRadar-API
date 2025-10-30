import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tanp#1816",  # 🔁 replace with your actual MySQL password
    database="sport_radar"
)
cursor = conn.cursor()

# Define queries (updated for your schema)
queries = {
    # --- 1. COMPETITIONS ANALYSIS ---
    "List all competitions with category names":
        """SELECT c.competition_id, c.competition_name, cat.category_name
           FROM competitions c
           JOIN categories cat ON c.category_id = cat.category_id;""",

    "Count number of competitions in each category":
        """SELECT cat.category_name, COUNT(c.competition_id) AS total_competitions
           FROM competitions c
           JOIN categories cat ON c.category_id = cat.category_id
           GROUP BY cat.category_name;""",

    "Find competitions of type 'doubles'":
        """SELECT competition_id, competition_name, type
           FROM competitions
           WHERE type = 'doubles';""",

    "Get competitions in a specific category (e.g., ITF Men)":
        """SELECT c.competition_id, c.competition_name, cat.category_name
           FROM competitions c
           JOIN categories cat ON c.category_id = cat.category_id
           WHERE cat.category_name = 'ITF Men';""",

    "Identify parent competitions and their sub-competitions":
        """SELECT parent.competition_name AS parent_competition,
                  child.competition_name AS sub_competition
           FROM competitions parent
           JOIN competitions child ON parent.competition_id = child.category_id
           ORDER BY parent.competition_name;""",  # simplified since no parent_id column found

    "Analyze distribution of competition types by category":
        """SELECT cat.category_name, c.type, COUNT(*) AS total
           FROM competitions c
           JOIN categories cat ON c.category_id = cat.category_id
           GROUP BY cat.category_name, c.type
           ORDER BY cat.category_name;""",

    "List all top-level competitions (no parent)":
        """SELECT competition_id, competition_name
           FROM competitions
           WHERE category_id IS NULL;""",

    # --- 2. VENUE ANALYSIS ---
    "List all venues with their complex names":
        """SELECT v.venue_name, v.city_name, v.country_name, c.complex_name
           FROM venues v
           LEFT JOIN complexes c ON v.complex_id = c.complex_id;""",

    "Count number of venues in each complex":
        """SELECT c.complex_name, COUNT(v.venue_id) AS total_venues
           FROM venues v
           JOIN complexes c ON v.complex_id = c.complex_id
           GROUP BY c.complex_name;""",

    "Get details of venues in a specific country (e.g., India)":
        """SELECT venue_name, city_name, country_name, timezone
           FROM venues
           WHERE country_name = 'India';""",

    "Identify all venues with their timezones":
        """SELECT venue_name, timezone FROM venues;""",

    "Find complexes with more than one venue":
        """SELECT c.complex_name, COUNT(v.venue_id) AS total_venues
           FROM complexes c
           JOIN venues v ON c.complex_id = v.complex_id
           GROUP BY c.complex_name
           HAVING COUNT(v.venue_id) > 1;""",

    "List venues grouped by country":
        """SELECT country_name, COUNT(venue_id) AS total_venues
           FROM venues
           GROUP BY country_name;""",

    "Find all venues for a specific complex":
        """SELECT v.venue_name, v.city_name, v.country_name
           FROM venues v
           JOIN complexes c ON v.complex_id = c.complex_id
           WHERE c.complex_name = 'Melbourne Park';""",

    # --- 3. COMPETITOR RANKING ANALYSIS ---
    "Get all competitors with their rank and points":
        """SELECT comp.name, comp.country, r.rank_position, r.points
           FROM competitors comp
           JOIN competitor_rankings r ON comp.competitor_id = r.competitor_id;""",

    "Find competitors ranked in the top 5":
        """SELECT comp.name, comp.country, r.rank_position, r.points
           FROM competitors comp
           JOIN competitor_rankings r ON comp.competitor_id = r.competitor_id
           WHERE r.rank_position <= 5
           ORDER BY r.rank_position;""",

    "List competitors with no rank movement (stable rank)":
        """SELECT comp.name, comp.country, r.rank_position
           FROM competitors comp
           JOIN competitor_rankings r ON comp.competitor_id = r.competitor_id
           WHERE r.movement = 0;""",

    "Get total points of competitors from a specific country (e.g., USA)":
        """SELECT comp.country, SUM(r.points) AS total_points
           FROM competitors comp
           JOIN competitor_rankings r ON comp.competitor_id = r.competitor_id
           WHERE comp.country = 'USA'
           GROUP BY comp.country;""",

    "Count competitors per country":
        """SELECT country, COUNT(competitor_id) AS total_competitors
           FROM competitors
           GROUP BY country
           ORDER BY total_competitors DESC;""",

    "Find competitors with the highest points in the current week":
        """SELECT comp.name, comp.country, r.points
           FROM competitors comp
           JOIN competitor_rankings r ON comp.competitor_id = r.competitor_id
           WHERE r.points = (SELECT MAX(points) FROM competitor_rankings);"""
}

# Execute and display results
for title, query in queries.items():
    print(f"\n📊 {title}")
    print("-" * (len(title) + 3))
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        print("No results found.\n")
    else:
        for row in rows[:10]:  # limit to first 10 rows for readability
            print(row)
        if len(rows) > 10:
            print(f"... ({len(rows)} total rows)\n")

# Close connections
cursor.close()
conn.close()
print("\n✅ All queries executed successfully!")