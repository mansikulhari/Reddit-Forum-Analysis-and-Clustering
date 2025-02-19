import mysql.connector
from mysql.connector import Error


def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="easy",
            database="reddit"
        )

        if connection.is_connected():
            print("Connection to MySQL DB successful")
            cursor = connection.cursor()

            # Modify the table creation queries
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Posts (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                Score INT,
                TotalComments INT
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Comments (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                Score INT,
                TotalReplies INT
            )
            """)

            # Keywords table remains unchanged
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Keywords (
                KeywordID INT AUTO_INCREMENT PRIMARY KEY,
                Keyword VARCHAR(255) UNIQUE
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS PostKeywords (
                PostID INT,
                KeywordID INT,
                FOREIGN KEY (PostID) REFERENCES Posts (ID),
                FOREIGN KEY (KeywordID) REFERENCES Keywords (KeywordID)
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS CommentKeywords (
                CommentID INT,
                KeywordID INT,
                FOREIGN KEY (CommentID) REFERENCES Comments (ID),
                FOREIGN KEY (KeywordID) REFERENCES Keywords (KeywordID)
            )
            """)

            print("Tables checked/created successfully")

    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            print(f"Executing {query} with {data}")  # Add this line
            cursor.execute(query, data)
        else:
            print(f"Executing {query}")  # And this line
            cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")



def insert_post_metadata(connection, post):
    query = """INSERT INTO Posts (Score, TotalComments) VALUES (%s, %s)"""
    if 'Score' not in post or 'Total Comments' not in post:
        return
    data = (post['Score'], post['Total Comments'])
    execute_query(connection, query, data)
    cursor = connection.cursor()
    cursor.execute("SELECT LAST_INSERT_ID();")
    return cursor.fetchone()[0]

def insert_comment_metadata(connection, comment):
    query = """INSERT INTO Comments (Score, TotalReplies) VALUES (%s, %s)"""
    if 'Score' not in comment or 'Total Replies' not in comment:
        return
    data = (comment['Score'], comment['Total Replies'])
    execute_query(connection, query, data)
    cursor = connection.cursor()
    cursor.execute("SELECT LAST_INSERT_ID();")
    return cursor.fetchone()[0]



def insert_keyword_get_id(connection, keyword):
    cursor = connection.cursor()
    query = """INSERT INTO Keywords (Keyword) VALUES (%s) ON DUPLICATE KEY UPDATE KeywordID=LAST_INSERT_ID(KeywordID), Keyword=VALUES(Keyword)"""
    data = (keyword[0],)
    execute_query(connection, query, data)
    cursor.execute("SELECT LAST_INSERT_ID();")  # Explicitly selecting the last insert id
    return cursor.fetchone()[0]  # Fetching the id as the first element of the first row of results



def insert_into_junction_table(connection, table_name, id, keyword_id):
    data = (id, keyword_id)
    query = f"""INSERT INTO {table_name} VALUES (%s, %s)"""
    execute_query(connection, query, data)


def comment_id_exists(connection, comment_id):
    cursor = connection.cursor()
    query = "SELECT CommentID FROM Comments WHERE CommentID = %s"
    cursor.execute(query, (comment_id,))
    return cursor.fetchone() is not None
