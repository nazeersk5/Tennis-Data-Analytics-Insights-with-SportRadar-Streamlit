import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# ✅ MySQL Configuration
MYSQL_USER = "root"
MYSQL_PASSWORD = "FIroza@2003"
MYSQL_HOST = "localhost"
MYSQL_DB = "tennis_db"

# ✅ Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# ✅ Fetch Data Function (Fix for SQL Syntax Error)
def fetch_data(query):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        data = cursor.fetchall()
    except mysql.connector.Error as e:
        st.error(f"MySQL Error: {e}")
        data = []
    finally:
        cursor.close()
        connection.close()
    return pd.DataFrame(data) if data else pd.DataFrame()

# ✅ Get All Competitors (Fix for "rank" column issue)
def get_competitors():
    query = """
        SELECT 
            c.competitor_id, c.name, c.country, c.country_code, c.abbreviation,
            cr.ranking_position AS `rank`, cr.movement, cr.points, cr.competitions_played
        FROM competitors c
        JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id;
    """
    return fetch_data(query)

# ✅ Get Summary Statistics
def get_summary_statistics():
    query = """
        SELECT 
            COUNT(DISTINCT c.competitor_id) AS total_competitors, 
            COUNT(DISTINCT c.country) AS total_countries, 
            MAX(cr.points) AS highest_points
        FROM competitors c
        JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id;
    """
    return fetch_data(query)

# ✅ Get Country-wise Analysis
def get_country_analysis():
    query = """
        SELECT 
            c.country, COUNT(c.competitor_id) AS total_competitors, 
            AVG(cr.points) AS avg_points
        FROM competitors c
        JOIN competitor_rankings cr ON c.competitor_id = cr.competitor_id
        GROUP BY c.country
        ORDER BY total_competitors DESC;
    """
    return fetch_data(query)

# ✅ Streamlit App
def main():
    st.set_page_config(page_title="Tennis Data Dashboard", layout="wide")
    st.title("🎾 Tennis Competitor Rankings Dashboard")
    st.sidebar.title("Filters & Navigation")

    # Load data
    df = get_competitors()
    summary = get_summary_statistics()
    country_analysis = get_country_analysis()

    # Sidebar filters
    st.sidebar.header("Filter Competitors")
    competitor_name = st.sidebar.text_input("Search Competitor by Name")
    if not df.empty:
        rank_range = st.sidebar.slider("Filter by Rank", int(df['rank'].min()), int(df['rank'].max()), (int(df['rank'].min()), int(df['rank'].max())))
        points_range = st.sidebar.slider("Filter by Points", int(df['points'].min()), int(df['points'].max()), (int(df['points'].min()), int(df['points'].max())))
        selected_country = st.sidebar.selectbox("Filter by Country", ["All"] + df['country'].unique().tolist())

        # Apply filters
        if competitor_name:
            df = df[df['name'].str.contains(competitor_name, case=False, na=False)]
        df = df[(df['rank'] >= rank_range[0]) & (df['rank'] <= rank_range[1])]
        df = df[(df['points'] >= points_range[0]) & (df['points'] <= points_range[1])]
        if selected_country != "All":
            df = df[df['country'] == selected_country]

    # 📌 **Homepage Dashboard**
    st.header("📊 Homepage Dashboard")
    if not summary.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Competitors", summary['total_competitors'][0])
        with col2:
            st.metric("Countries Represented", summary['total_countries'][0])
        with col3:
            st.metric("Highest Points", summary['highest_points'][0])

    # 🎾 **Competitor Data Table**
    st.header("🎾 Competitor Data")
    st.dataframe(df, use_container_width=True)

    # 👤 **Competitor Details Viewer**
    if not df.empty:
        st.header("👤 Competitor Details")
        selected_competitor = st.selectbox("Select a Competitor", df['name'].unique())
        competitor_details = df[df['name'] == selected_competitor].iloc[0]
        st.write(f"**Name:** {competitor_details['name']}")
        st.write(f"**Rank:** {competitor_details['rank']}")
        st.write(f"**Movement:** {competitor_details['movement']}")
        st.write(f"**Points:** {competitor_details['points']}")
        st.write(f"**Competitions Played:** {competitor_details['competitions_played']}")
        st.write(f"**Country:** {competitor_details['country']}")

    # 🌍 **Country-wise Analysis**
    st.header("🌍 Country-Wise Analysis")
    st.dataframe(country_analysis, use_container_width=True)

    # 🏆 **Leaderboards**
    if not df.empty:
        st.header("🏅 Leaderboards")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Top-Ranked Competitors")
            top_ranked = df.sort_values(by='rank').head(10)
            st.dataframe(top_ranked[['name', 'rank', 'country']], use_container_width=True)

        with col2:
            st.subheader("Competitors with Highest Points")
            top_points = df.sort_values(by='points', ascending=False).head(10)
            st.dataframe(top_points[['name', 'points', 'country']], use_container_width=True)

    # 📈 **Visualizations**
    st.header("📈 Visualizations")
    if not df.empty:
        fig1 = px.bar(df.sort_values(by='points', ascending=False).head(10), x='name', y='points', title="Top 10 Competitors by Points", color='points')
        st.plotly_chart(fig1, use_container_width=True)

    # 📌 **Dynamic SQL Query Execution**
    st.sidebar.header("Run SQL Queries")
    custom_query = st.sidebar.text_area("Enter SQL Query")
    if st.sidebar.button("Execute Query"):
        result_df = fetch_data(custom_query)
        st.dataframe(result_df, use_container_width=True)

    st.write("📊 Powered by Streamlit & MySQL")

# ✅ Run the App
if __name__ == "__main__":
    main()