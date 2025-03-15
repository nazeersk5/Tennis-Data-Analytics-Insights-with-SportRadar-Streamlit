import mysql.connector
import requests

# ✅ API Configuration
API_KEY = "5UHdnxnBkddTWCBjqyEGNhTALq7Klc0ZZbP5xisP"
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en/double_competitors_rankings.json"

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

# ✅ Create Tables
def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Create Competitors Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitors (
            competitor_id VARCHAR(50) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            country VARCHAR(100) NOT NULL,
            country_code CHAR(3) NOT NULL,
            abbreviation VARCHAR(10) NOT NULL
        )
    """)

    # ✅ Fix: Rename `rank` to `ranking_position` (Avoids SQL reserved keyword conflict)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitor_rankings (
            rank_id INT AUTO_INCREMENT PRIMARY KEY,
            ranking_position INT NOT NULL,
            movement INT NOT NULL,
            points INT NOT NULL,
            competitions_played INT NOT NULL,
            competitor_id VARCHAR(50),
            FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Competitors & Rankings Tables Created Successfully!")

# ✅ Fetch Data from API
def fetch_data():
    url = f"{BASE_URL}?api_key={API_KEY}"
    print(f"🌐 Fetching data from: {url}")  # ✅ Debugging API URL
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("✅ API Response: Successfully retrieved")  # ✅ Print confirmation
        return data

    print(f"❌ Error {response.status_code}: {response.text}")
    return None

# ✅ Insert Competitors Data
def insert_competitors():
    data = fetch_data()  # ✅ Fetch rankings data
    if data and "rankings" in data:
        rankings = data["rankings"]

        connection = get_db_connection()
        cursor = connection.cursor()

        competitors_inserted = set()

        for ranking in rankings:
            for competitor_data in ranking.get("competitor_rankings", []):  # ✅ Extract competitor rankings
                competitor = competitor_data.get("competitor", {})
                competitor_id = competitor.get("id")

                if competitor_id and competitor_id not in competitors_inserted:
                    cursor.execute("""
                        INSERT IGNORE INTO competitors 
                        (competitor_id, name, country, country_code, abbreviation)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (competitor_id, competitor.get("name", "Unknown"),
                          competitor.get("country", "Unknown"),
                          competitor.get("country_code", "N/A"),
                          competitor.get("abbreviation", "N/A")))
                    competitors_inserted.add(competitor_id)

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Competitors Data Inserted Successfully!")
    else:
        print("⚠️ No competitor data available or endpoint issue.")

# ✅ Insert Rankings Data
def insert_rankings():
    data = fetch_data()  # ✅ Fetch rankings data
    if data and "rankings" in data:
        rankings = data["rankings"]

        connection = get_db_connection()
        cursor = connection.cursor()

        for ranking in rankings:
            for competitor_data in ranking.get("competitor_rankings", []):  # ✅ Extract competitor rankings
                competitor = competitor_data.get("competitor", {})
                competitor_id = competitor.get("id")

                # ✅ Fix: Use `ranking_position` instead of `rank`
                cursor.execute("""
                    INSERT IGNORE INTO competitor_rankings 
                    (ranking_position, movement, points, competitions_played, competitor_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (competitor_data.get("rank"), competitor_data.get("movement"),
                      competitor_data.get("points"), competitor_data.get("competitions_played"),
                      competitor_id))

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Competitor Rankings Data Inserted Successfully!")
    else:
        print("⚠️ No rankings data available or endpoint issue.")

# ✅ Verify Data Insertion
def verify_data():
    connection = get_db_connection()
    cursor = connection.cursor()

    print("\n📌 Sample Competitors from Database:")
    cursor.execute("SELECT * FROM competitors LIMIT 3")
    competitors = cursor.fetchall()
    for comp in competitors:
        print(f"ID: {comp[0]}, Name: {comp[1]}, Country: {comp[2]}, Code: {comp[3]}, Abbreviation: {comp[4]}")

    print("\n📌 Sample Rankings from Database:")
    cursor.execute("SELECT * FROM competitor_rankings LIMIT 3")
    rankings = cursor.fetchall()
    for rank in rankings:
        print(f"Rank ID: {rank[0]}, Rank: {rank[1]}, Movement: {rank[2]}, Points: {rank[3]}, Competitions Played: {rank[4]}, Competitor ID: {rank[5]}")

    cursor.close()
    connection.close()

# ✅ Main Execution
if __name__ == "__main__":
    create_tables()
    insert_competitors()
    insert_rankings()
    verify_data()