import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# ---------------------- DATABASE CONNECTION ----------------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",   # 🔁 replace with your actual MySQL password
        database="sport_radar"
    )

# ---------------------- QUERY EXECUTION ----------------------
def run_query(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ---------------------- STREAMLIT APP ----------------------
st.set_page_config(page_title="Sports Radar Dashboard", layout="wide")

st.title("🎾 Sports Radar Analytics Dashboard")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard", "🔍 Competitor Search", "🌍 Country Analysis",
    "🏆 Leaderboards", "📊 Competitions & Venues"
])

# ---------------------- Dashboard ----------------------
with tab1:
    total_competitors = run_query("SELECT COUNT(*) AS total FROM competitors;")
    total_countries = run_query("SELECT COUNT(DISTINCT country) AS countries FROM competitors;")
    top_points = run_query("SELECT MAX(points) AS max_points FROM competitor_rankings;")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Competitors", int(total_competitors['total'][0]))
    c2.metric("Countries Represented", int(total_countries['countries'][0]))
    c3.metric("Highest Points", int(top_points['max_points'][0]))

# ---------------------- Competitor Search ----------------------
with tab2:
    st.subheader("Search Competitors")
    name = st.text_input("Enter competitor name:")
    min_rank, max_rank = st.slider("Select rank range", 1, 1000, (1, 50))
    min_points = st.number_input("Minimum points:", min_value=0, value=1000)

    query = f"""
        SELECT comp.name, comp.country, cr.rank_position, cr.points
        FROM competitor_rankings cr
        JOIN competitors comp ON cr.competitor_id = comp.competitor_id
        WHERE cr.rank_position BETWEEN {min_rank} AND {max_rank}
          AND cr.points >= {min_points}
          {"AND comp.name LIKE '%" + name + "%'" if name else ""}
        ORDER BY cr.rank_position;
    """
    df = run_query(query)
    st.dataframe(df)

# ---------------------- Country-Wise Analysis ----------------------
with tab3:
    st.subheader("Country-wise Competitor Analysis")
    df = run_query("""
        SELECT comp.country, COUNT(comp.competitor_id) AS total_competitors,
               AVG(cr.points) AS avg_points
        FROM competitor_rankings cr
        JOIN competitors comp ON cr.competitor_id = comp.competitor_id
        GROUP BY comp.country
        ORDER BY total_competitors DESC;
    """)
    st.dataframe(df)
    st.plotly_chart(px.bar(df, x="country", y="total_competitors", title="Competitors per Country"))

# ---------------------- Leaderboards ----------------------
with tab4:
    st.subheader("Top 10 Competitors by Points")
    top10 = run_query("""
        SELECT comp.name, comp.country, cr.points
        FROM competitor_rankings cr
        JOIN competitors comp ON cr.competitor_id = comp.competitor_id
        ORDER BY cr.points DESC
        LIMIT 10;
    """)
    st.dataframe(top10)
    st.plotly_chart(px.bar(top10, x="name", y="points", color="country", title="Top 10 Competitors"))

# ---------------------- Competitions & Venues ----------------------
with tab5:
    st.subheader("Competitions & Venues Overview")

    c_df = run_query("""
        SELECT cat.category_name, COUNT(c.competition_id) AS total_competitions
        FROM competitions c
        JOIN categories cat ON c.category_id = cat.category_id
        GROUP BY cat.category_name;
    """)
    v_df = run_query("""
        SELECT country_name, COUNT(venue_id) AS total_venues
        FROM venues
        GROUP BY country_name
        ORDER BY total_venues DESC;
    """)

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(c_df, names="category_name", values="total_competitions", title="Competitions by Category"))
    with c2:
        st.plotly_chart(px.bar(v_df.head(10), x="country_name", y="total_venues", title="Top 10 Countries by Venues"))
