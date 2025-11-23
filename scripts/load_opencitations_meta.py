import psycopg2
import csv
import os
import glob
from tqdm import tqdm

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="opencitations_meta",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS papers (
    id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    pub_date TEXT,
    venue TEXT,
    volume TEXT,
    issue TEXT,
    page TEXT,
    type TEXT,
    publisher TEXT,
    editor TEXT
);
""")
conn.commit()

# Path to CSV files
csv_dir_path = r"2022-12-19T100000_csv/csv"
csv_files = glob.glob(os.path.join(csv_dir_path, "*.csv"))

MAX_RECORDS = None   # Set to None to parse all
batch_size = 1000
processed_count = 0
batch_counter = 0

for csv_file_path in tqdm(csv_files, desc="Processing CSV files"):
    try:
        with open(csv_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if MAX_RECORDS and processed_count >= MAX_RECORDS:
                    break

                try:
                    # Fix date format: convert 'YYYY-MM' to 'YYYY-MM-01'
                    pub_date = row['pub_date']
                    if not pub_date or pub_date.strip() == '':
                        pub_date = None
                    elif len(pub_date) == 7 and pub_date[4] == '-':
                        pub_date = pub_date + '-01'
                    elif len(pub_date) == 4 and pub_date.isdigit():
                        pub_date = pub_date + '-01-01'
                    cur.execute("""
                        INSERT INTO papers (id, title, author, pub_date, venue, volume, issue, page, type, publisher, editor)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, (
                        row['id'],
                        row['title'],
                        row['author'],
                        pub_date,  # store as TEXT
                        row['venue'],
                        row['volume'],
                        row['issue'],
                        row['page'],
                        row['type'],
                        row['publisher'],
                        row['editor']
                    ))
                    processed_count += 1
                    batch_counter += 1

                except Exception as e_row:
                    print(f"Skipped row due to error: {e_row}")
                    conn.rollback()  # Reset transaction so future inserts work
                    continue

                # Commit every batch_size rows
                if batch_counter >= batch_size:
                    conn.commit()
                    batch_counter = 0

        # Commit after finishing each CSV
        if batch_counter > 0:
            conn.commit()
            batch_counter = 0

    except Exception as e_file:
        print(f"Error processing file {csv_file_path}: {e_file}")

conn.commit()
cur.close()
conn.close()

print(f"✅ Done! Total papers loaded: {processed_count}")
