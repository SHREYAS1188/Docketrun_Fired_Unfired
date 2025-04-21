import psycopg2
from psycopg2 import sql

def save_to_database(data: dict):
    """
    Saves the dictionary data to PostgreSQL database.
    :param data: Dictionary with keys 'ImagePath', 'bluePercentage', 'greyPercentage'
    """
    try:
        # Connect to PostgreSQL database
        conn = psycopg2.connect(
            dbname="your_database",
            user="your_user",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        cursor = conn.cursor()
        
        # Ensure the table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS my_table (
                id SERIAL PRIMARY KEY,
                ImagePath TEXT NOT NULL,
                bluePercentage FLOAT NOT NULL,
                greyPercentage FLOAT NOT NULL
            )
        ''')
        
        # Insert data into table
        insert_query = sql.SQL("""
            INSERT INTO my_table (ImagePath, bluePercentage, greyPercentage) 
            VALUES (%s, %s, %s)
        """
        )
        cursor.execute(insert_query, (data['ImagePath'], data['bluePercentage'], data['greyPercentage']))
        
        # Commit and close connection
        conn.commit()
        cursor.close()
        conn.close()
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error: {e}")


# example function
def main():
    # Example dictionary input
    data = {
        "ImagePath": "path/to/image.jpg",
        "greyPixel": 5000,
        "bluePixel": 3000,
        "greyRatio": 0.62,
        "blueRatio": 0.38
    }
    save_to_database(data)
'''
if __name__ == "__main__":
    main()
'''