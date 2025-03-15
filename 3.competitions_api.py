import mysql.connector
import requests

# ✅ API Configuration
API_KEY = "5UHdnxnBkddTWCBjqyEGNhTALq7Klc0ZZbP5xisP"
BASE_URL = "https://api.sportradar.com/tennis/trial/v3/en"

# ✅ Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="FIroza@2003",
        database="tennis_db"
    )

# ✅ Create Tables
def create_competitions_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Create Categories Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id VARCHAR(50) PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL
        )
    """)

    # Create Competitions Table with Foreign Key to Categories
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            competition_id VARCHAR(50) PRIMARY KEY,
            competition_name VARCHAR(100) NOT NULL,
            parent_id VARCHAR(50) NULL,
            type VARCHAR(20) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            category_id VARCHAR(50),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Competitions & Categories Tables Created Successfully!")

# ✅ Fetch Data from API
def fetch_data(endpoint):
    url = f"{BASE_URL}/{endpoint}.json?api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    print(f"❌ Error {response.status_code}: {response.text}")
    return None

# ✅ Insert Categories Data
def insert_categories():
    data = fetch_data("competitions")  # Fetch competitions data (contains category info)
    if data and "competitions" in data:
        competitions = data["competitions"]

        connection = get_db_connection()
        cursor = connection.cursor()

        categories_inserted = set()  # To track inserted categories & avoid duplicate inserts

        for comp in competitions:
            category_id = comp["category"]["id"]
            category_name = comp["category"]["name"]

            # ✅ Ensure category is inserted only once
            if category_id not in categories_inserted:
                cursor.execute("""
                    INSERT IGNORE INTO categories (category_id, category_name)
                    VALUES (%s, %s)
                """, (category_id, category_name))
                categories_inserted.add(category_id)  # Mark category as inserted

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Categories Data Inserted Successfully!")
    else:
        print("⚠️ No category data available or endpoint issue.")

# ✅ Insert Competitions Data
def insert_competitions():
    data = fetch_data("competitions")  # Fetch competitions data
    if data and "competitions" in data:
        competitions = data["competitions"]

        connection = get_db_connection()
        cursor = connection.cursor()

        for comp in competitions:
            category_id = comp["category"]["id"]  # Ensure category_id exists

            cursor.execute("""
                INSERT IGNORE INTO competitions 
                (competition_id, competition_name, parent_id, type, gender, category_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (comp["id"], comp["name"], comp.get("parent_id"), comp["type"], comp["gender"], category_id))

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Competitions Data Inserted Successfully!")
    else:
        print("⚠️ No competition data available or endpoint issue.")

# ✅ Main Execution
if __name__ == "__main__":
    create_competitions_tables()
    insert_categories()
    insert_competitions()