import pandas as pd
import sqlite3

def save_enriched_data_to_database(df, db_path, table_name):
    """
    Save the enriched data to an SQLite database.

    Parameters:
    - df: The enriched DataFrame to save.
    - db_path: Path to the SQLite database file.
    - table_name: Name of the table to store the data.
    """
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Enriched data saved to database: {db_path}, table: {table_name}")

def enrich_data(sensor_data_path, master_db_path, enriched_data_output):
    """
    Enrich sensor data with master data and save the enriched dataset.
    
    Parameters:
    - sensor_data_path: Path to the validated sensor data CSV file.
    - master_db_path: Path to the SQLite database containing master data.
    - enriched_data_output: Path to save the enriched data as a CSV file.
    """
    # Load validated sensor data
    sensor_data = pd.read_csv(sensor_data_path)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(master_db_path)

    # Load master data
    master_devices = pd.read_sql_query("SELECT * FROM master_devices", conn)

    # Merge sensor data with master data
    enriched_data = pd.merge(sensor_data, master_devices, on="device_id", how="left")

    # Check for missing master data and log warnings
    if enriched_data['type'].isnull().any():
        print("Warning: Some device IDs are not found in master data.")

    # Save the enriched data to a CSV file
    enriched_data.to_csv(enriched_data_output, index=False)
    print(enriched_data.head())
    print(f"Enriched data saved to {enriched_data_output}")

    # Save the enriched data to a database
    save_enriched_data_to_database(enriched_data, enriched_db_path, table_name)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    # Define file paths
    sensor_data_path = "data/validated_data.csv"  # Path to validated sensor data
    master_db_path = "data/master_data.sqlite"  # Path to SQLite master data database
    enriched_data_output = "data/enriched_data.csv"  # Path to save enriched data
    enriched_db_path = "data/enriched_data.sqlite"  # Path to save enriched data in SQLite
    table_name = "enriched_sensors"  # Table name for enriched data

    # Enrich the data
    enrich_data(sensor_data_path, master_db_path, enriched_data_output, enriched_db_path, table_name)