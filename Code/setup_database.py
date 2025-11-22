import sqlite3
import pandas as pd
import os

# Configuration
db_file = 'school_data.db'
csv_file = 'cleaned_students.csv'

def create_dummy_csv():
    """
    Creates a dummy CSV file for testing purposes if it doesn't exist.
    Remove this function if you already have your real data file.
    """
    if not os.path.exists(csv_file):
        print(f"'{csv_file}' not found. Creating a dummy file for demonstration...")
        data = {
            'student_id': ['S001', 'S002', 'S003', 'S004', 'S005'],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'subject': ['Math', 'Math', 'Science', 'Science', 'History'],
            'score': [85.5, 78.0, 92.0, 88.5, 76.0],
            'date': ['2023-10-01', '2023-10-01', '2023-10-02', '2023-10-02', '2023-10-03'],
            'attendance': [95, 80, 100, 92, 85],
            'grade': ['A', 'C', 'A', 'B', 'C']
        }
        df = pd.DataFrame(data)
        df.to_csv(csv_file, index=False)
        print("Dummy CSV created successfully.\n")

def setup_database():
    # 0. Check for CSV (Optional helper)
    create_dummy_csv() 

    print(f"Connecting to database: {db_file}...")
    
    # 1. Create Database Connection
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 2. Create Table (Schema Definition)
    # We define the schema explicitly to ensure types and constraints (like PRIMARY KEY)
    create_table_query = """
    CREATE TABLE IF NOT EXISTS student_performance (
        student_id TEXT PRIMARY KEY,
        name TEXT,
        subject TEXT,
        score REAL,
        date TEXT,
        attendance INTEGER,
        grade TEXT
    );
    """
    cursor.execute(create_table_query)
    conn.commit()
    print("Table 'student_performance' ensured to exist.")

    # 3. Load Data using Pandas
    if os.path.exists(csv_file):
        print(f"Reading data from {csv_file}...")
        df = pd.read_csv(csv_file)

        # 'if_exists="replace"' will drop the table and recreate it with Pandas inferred types.
        # If you strictly want to keep the Primary Key schema defined above, change this to 'append'.
        df.to_sql('student_performance', conn, if_exists='replace', index=False)
        print(f"Data loaded successfully. ({len(df)} rows)")
    else:
        print(f"Error: {csv_file} not found. Please ensure the file is in the same directory.")
        conn.close()
        return

    # 4. Verify Data (Aggregation Query)
    print("\n--- Verification: Average Score per Subject ---")
    query = """
    SELECT subject, AVG(score) as average_score
    FROM student_performance
    GROUP BY subject;
    """
    
    try:
        verification_df = pd.read_sql(query, conn)
        print(verification_df)
    except Exception as e:
        print(f"Verification query failed: {e}")

    # Close connection
    conn.close()
    print("\nDatabase setup complete.")

if __name__ == "__main__":
    setup_database()