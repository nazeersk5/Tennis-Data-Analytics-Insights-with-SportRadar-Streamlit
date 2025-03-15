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

# ✅ List all competitions along with their category name
query_1 = """
SELECT competitions.competition_id, competitions.competition_name, categories.category_name 
FROM competitions 
JOIN categories ON competitions.category_id = categories.category_id;
"""
execute_query(query_1, "List all competitions along with their category name")

# ✅ Count the number of competitions in each category
query_2 = """
SELECT categories.category_name, COUNT(competitions.competition_id) AS total_competitions 
FROM competitions 
JOIN categories ON competitions.category_id = categories.category_id
GROUP BY categories.category_name;
"""
execute_query(query_2, "Count the number of competitions in each category")

# ✅ Find all competitions of type 'doubles'
query_3 = """
SELECT competition_id, competition_name 
FROM competitions 
WHERE type = 'doubles';
"""
execute_query(query_3, "Find all competitions of type 'doubles'")

# ✅ Get competitions that belong to a specific category (e.g., ITF Men)
query_4 = """
SELECT competition_id, competition_name 
FROM competitions 
WHERE category_id = (SELECT category_id FROM categories WHERE category_name = 'ITF Men');
"""
execute_query(query_4, "Get competitions that belong to the category 'ITF Men'")

# ✅ Identify parent competitions and their sub-competitions
query_5 = """
SELECT parent.competition_name AS parent_competition, child.competition_name AS sub_competition 
FROM competitions AS child
JOIN competitions AS parent ON child.parent_id = parent.competition_id;
"""
execute_query(query_5, "Identify parent competitions and their sub-competitions")

# ✅ Analyze the distribution of competition types by category
query_6 = """
SELECT categories.category_name, competitions.type, COUNT(competitions.competition_id) AS total_competitions
FROM competitions 
JOIN categories ON competitions.category_id = categories.category_id
GROUP BY categories.category_name, competitions.type;
"""
execute_query(query_6, "Analyze the distribution of competition types by category")

# ✅ List all competitions with no parent (top-level competitions)
query_7 = """
SELECT competition_id, competition_name 
FROM competitions 
WHERE parent_id IS NULL;
"""
execute_query(query_7, "List all competitions with no parent (top-level competitions)")