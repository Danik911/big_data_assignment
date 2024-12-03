import sqlite3
import pandas as pd
import os

def extract_unique_devices(file_path, device_type):
    """
    Extract unique device IDs from a CSV file and associate them with a device type.
    """
    df = pd.read_csv(file_path)
    unique_devices = df['device_id'].unique()
    return [(device_id, device_type, "Active") for device_id in unique_devices]

def populate_master_devices():
    """
    Populate the master_devices table in master_data.sqlite.
    """
    # SQLite database path
    db_path = "data/master_data.sqlite"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create master_devices table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS master_devices (
        device_id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        status TEXT
    );
    """)

    # Extract devices from CSV files
    devices = []
    devices.extend(extract_unique_devices("data/structured_data/temp_sensor_data.csv", "Temperature Sensor"))
    devices.extend(extract_unique_devices("data/structured_data/humidi_probe_data.csv", "Humidity Probe"))
    devices.extend(extract_unique_devices("data/structured_data/eyecon2_data.csv", "Particle Size Sensor"))
    devices.extend(extract_unique_devices("data/structured_data/clean_monitor_data.csv", "Air Quality Monitor"))

    # Insert devices into master_devices table
    cursor.executemany("""
    INSERT OR IGNORE INTO master_devices (device_id, type, status)
    VALUES (?, ?, ?);
    """, devices)

    # Commit and close connection
    conn.commit()
    conn.close()
    print("Master devices table populated successfully.")

if __name__ == "__main__":
    populate_master_devices()
