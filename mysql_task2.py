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

# ✅ List all venues along with their associated complex name
query_1 = """
SELECT venues.venue_id, venues.venue_name, complexes.complex_name 
FROM venues 
JOIN complexes ON venues.complex_id = complexes.complex_id;
"""
execute_query(query_1, "List all venues along with their associated complex name")

# ✅ Count the number of venues in each complex
query_2 = """
SELECT complexes.complex_name, COUNT(venues.venue_id) AS total_venues 
FROM venues 
JOIN complexes ON venues.complex_id = complexes.complex_id
GROUP BY complexes.complex_name;
"""
execute_query(query_2, "Count the number of venues in each complex")

# ✅ Get details of venues in a specific country (e.g., Chile)
query_3 = """
SELECT venue_id, venue_name, city_name, country_name, timezone
FROM venues 
WHERE country_name = 'Chile';
"""
execute_query(query_3, "Get details of venues in Chile")

# ✅ Identify all venues and their timezones
query_4 = """
SELECT venue_id, venue_name, timezone 
FROM venues;
"""
execute_query(query_4, "Identify all venues and their timezones")

# ✅ Find complexes that have more than one venue
query_5 = """
SELECT complexes.complex_name, COUNT(venues.venue_id) AS total_venues
FROM venues
JOIN complexes ON venues.complex_id = complexes.complex_id
GROUP BY complexes.complex_name
HAVING total_venues > 1;
"""
execute_query(query_5, "Find complexes that have more than one venue")

# ✅ List venues grouped by country
query_6 = """
SELECT 
    country_name, 
    COUNT(venue_name) AS total_venue, 
    JSON_ARRAYAGG(venue_name) AS list_of_venues 
FROM venues 
GROUP BY country_name;;
"""
execute_query(query_6, "List venues grouped by country")

# ✅ Find all venues for a specific complex (e.g., Nacional)
query_7 = """
SELECT venue_id, venue_name 
FROM venues
WHERE complex_id = (SELECT complex_id FROM complexes WHERE complex_name = 'Nacional');
"""
execute_query(query_7, "Find all venues for the complex 'Nacional'")