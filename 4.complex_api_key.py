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
def create_complexes_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Create Complexes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complexes (
            complex_id VARCHAR(50) PRIMARY KEY,
            complex_name VARCHAR(100) NOT NULL
        )
    """)

    # Create Venues Table with Foreign Key to Complexes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venues (
            venue_id VARCHAR(50) PRIMARY KEY,
            venue_name VARCHAR(100) NOT NULL,
            city_name VARCHAR(100) NOT NULL,
            country_name VARCHAR(100) NOT NULL,
            country_code CHAR(3) NOT NULL,
            timezone VARCHAR(100) NOT NULL,
            complex_id VARCHAR(50),
            FOREIGN KEY (complex_id) REFERENCES complexes(complex_id)
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()
    print("✅ Complexes & Venues Tables Created Successfully!")

# ✅ Fetch Data from API
def fetch_data(endpoint):
    url = f"{BASE_URL}/{endpoint}.json?api_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    print(f"❌ Error {response.status_code}: {response.text}")
    return None

# ✅ Insert Complexes Data
def insert_complexes():
    data = fetch_data("complexes")  # Fetch complexes data
    if data and "complexes" in data:
        complexes = data["complexes"]

        connection = get_db_connection()
        cursor = connection.cursor()

        for comp in complexes:
            cursor.execute("""
                INSERT IGNORE INTO complexes (complex_id, complex_name)
                VALUES (%s, %s)
            """, (comp.get("id"), comp.get("name")))

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Complexes Data Inserted Successfully!")
    else:
        print("⚠️ No complex data available or endpoint issue.")

# ✅ Insert Venues Data
def insert_venues():
    data = fetch_data("complexes")  # Fetch complexes data
    if data and "complexes" in data:
        complexes = data["complexes"]

        connection = get_db_connection()
        cursor = connection.cursor()

        for comp in complexes:
            complex_id = comp.get("id")

            for venue in comp.get("venues", []):
                cursor.execute("""
                    INSERT IGNORE INTO venues 
                    (venue_id, venue_name, city_name, country_name, country_code, timezone, complex_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (venue.get("id"), venue.get("name"), venue.get("city", "Unknown"), venue.get("country", "Unknown"),
                      venue.get("country_code", "N/A"), venue.get("timezone", "N/A"), complex_id))

        connection.commit()
        cursor.close()
        connection.close()
        print("✅ Venues Data Inserted Successfully!")
    else:
        print("⚠️ No venue data available or endpoint issue.")

# ✅ Main Execution
if __name__ == "__main__":
    create_complexes_tables()
    insert_complexes()
    insert_venues()