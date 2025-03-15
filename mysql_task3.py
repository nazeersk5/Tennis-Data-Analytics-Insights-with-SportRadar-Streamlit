import mysql.connector

# ✅ MySQL Configuration
MYSQL_USER = "root"
MYSQL_PASSWORD = "FIroza@2003"
MYSQL_HOST = "localhost"
MYSQL_DB = "tennis_db"

# ✅ Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

# ✅ Execute SQL Query & Print Results
def execute_query(query, description):
    connection = get_db_connection()
    cursor = connection.cursor()

    print(f"\n📌 {description}")
    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        for row in results:
            print(row)
    else:
        print("⚠️ No data found.")

    cursor.close()
    connection.close()

# ✅ Get all competitors with their rank and points
query_1 = """
SELECT competitors.name, competitor_rankings.ranking_position, competitor_rankings.points
FROM competitor_rankings
JOIN competitors ON competitor_rankings.competitor_id = competitors.competitor_id
ORDER BY competitor_rankings.ranking_position ASC;
"""
execute_query(query_1, "Get all competitors with their rank and points")

# ✅ Find competitors ranked in the top 5
query_2 = """
SELECT competitors.name, competitor_rankings.ranking_position, competitor_rankings.points
FROM competitor_rankings
JOIN competitors ON competitor_rankings.competitor_id = competitors.competitor_id
WHERE competitor_rankings.ranking_position <= 5
ORDER BY competitor_rankings.ranking_position ASC;
"""
execute_query(query_2, "Find competitors ranked in the top 5")

# ✅ List competitors with no rank movement (stable rank)
query_3 = """
SELECT competitors.name, competitor_rankings.ranking_position, competitor_rankings.points
FROM competitor_rankings
JOIN competitors ON competitor_rankings.competitor_id = competitors.competitor_id
WHERE competitor_rankings.movement = 0
ORDER BY competitor_rankings.ranking_position ASC;
"""
execute_query(query_3, "List competitors with no rank movement (stable rank)")

# ✅ Get the total points of competitors from a specific country (e.g., Croatia)
query_4 = """
SELECT competitors.country, SUM(competitor_rankings.points) AS total_points
FROM competitor_rankings
JOIN competitors ON competitor_rankings.competitor_id = competitors.competitor_id
WHERE competitors.country = 'Croatia'
GROUP BY competitors.country;
"""
execute_query(query_4, "Get the total points of competitors from Croatia")

# ✅ Count the number of competitors per country
query_5 = """
SELECT competitors.country, COUNT(competitors.competitor_id) AS total_competitors
FROM competitors
GROUP BY competitors.country
ORDER BY total_competitors DESC;
"""
execute_query(query_5, "Count the number of competitors per country")

# ✅ Find competitors with the highest points in the current week
query_6 = """
SELECT competitors.name, competitor_rankings.ranking_position, competitor_rankings.points
FROM competitor_rankings
JOIN competitors ON competitor_rankings.competitor_id = competitors.competitor_id
ORDER BY competitor_rankings.points DESC
LIMIT 1;
"""
execute_query(query_6, "Find competitors with the highest points in the current week")