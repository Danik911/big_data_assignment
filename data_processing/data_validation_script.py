import pandas as pd
import sqlite3
import os
import re
from scipy.stats import zscore

# Define schema for all sensors
SCHEMA = {
    "device_id": {"type": str, "required": True, "pattern": r"^[A-Za-z]+[0-9_]+$"},
    "timestamp": {"type": pd.Timestamp, "required": True},
    "temperature": {"type": float, "required": False, "min": -50, "max": 100},
    "humidity": {"type": float, "required": False, "min": 0, "max": 100},
    "air_quality": {"type": str, "required": False, "allowed": ["Good", "Moderate", "Poor"]},
    "particle_size": {"type": float, "required": False, "min": 0, "max": 10000},
}

# Validation functions
def validate_field(value, field_name, field_rules):
    """
    Validate a single field based on rules in the schema.
    """
    if value is None and field_rules.get("required", False):
        return False, f"{field_name} is required but missing."
    
    if value is not None:
        if "type" in field_rules and not isinstance(value, field_rules["type"]):
            return False, f"{field_name} must be of type {field_rules['type']}."
        
        if "pattern" in field_rules and not re.match(field_rules["pattern"], str(value)):
            return False, f"{field_name} does not match the pattern {field_rules['pattern']}."
        
        if "min" in field_rules and value < field_rules["min"]:
            return False, f"{field_name} must be >= {field_rules['min']}."
        
        if "max" in field_rules and value > field_rules["max"]:
            return False, f"{field_name} must be <= {field_rules['max']}."
        
        if "allowed" in field_rules and value not in field_rules["allowed"]:
            return False, f"{field_name} must be one of {field_rules['allowed']}."
    
    return True, ""

def validate_row(row):
    """
    Validate an entire row based on the schema.
    """
    errors = []
    for field_name, field_rules in SCHEMA.items():
        value = row.get(field_name)
        valid, error_message = validate_field(value, field_name, field_rules)
        if not valid:
            errors.append(error_message)
    return errors

# Clean a single CSV file
def clean_csv(file_path):
    """
    Load, validate, and clean a CSV file.
    """
    df = pd.read_csv(file_path)

    # Parse and standardize timestamp
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df.dropna(subset=["timestamp"], inplace=True)  # Drop rows with invalid timestamps

    validation_errors = []

    # Validate each row
    for index, row in df.iterrows():
        row_errors = validate_row(row)
        if row_errors:
            validation_errors.append((index, row_errors))
    
    if validation_errors:
        print(f"Validation errors in {file_path}:")
        for idx, errors in validation_errors:
            print(f"Row {idx}: {errors}")
    
    # Impute missing values
    df.fillna({
        "temperature": df["temperature"].mean() if "temperature" in df else None,
        "humidity": df["humidity"].mean() if "humidity" in df else None,
        "air_quality": "Unknown",
        "particle_size": df["particle_size"].median() if "particle_size" in df else None,
    }, inplace=True)

    # Standardize units
    for col in ["temperature", "particle_size"]:
        if col in df:
            df[col] = df[col].apply(lambda x: round(x, 2) if pd.notnull(x) else None)

    # Remove duplicates
    df.drop_duplicates(subset=["device_id", "timestamp"], inplace=True)

    # Identify and remove outliers using Z-score
    for col in ["temperature", "humidity", "particle_size"]:
        if col in df:
            df[col + "_zscore"] = zscore(df[col].fillna(0))  # Fill NA for zscore calculation
            df = df[(df[col + "_zscore"] >= -3) & (df[col + "_zscore"] <= 3)]
            df.drop(columns=[col + "_zscore"], inplace=True)

    return df

# Merge all CSV files
def merge_csv_files(directory):
    """
    Merge all structured CSV files in a directory.
    """
    combined_df = pd.DataFrame()
    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            cleaned_data = clean_csv(file_path)
            combined_df = pd.concat([combined_df, cleaned_data], ignore_index=True)

    # Ensure no duplicates after merge
    combined_df.drop_duplicates(subset=["device_id", "timestamp"], inplace=True)

    return combined_df

# Save merged data to SQLite
def save_to_database(df, db_name, table_name):
    """
    Save a DataFrame to an SQLite database.
    """
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"Data saved to database: {db_name}, table: {table_name}")

# Execute the pipeline
def main():
    csv_directory = "sensor_data"  # Directory containing CSV files
    database_name = "sensors_data.sqlite"
    table_name = "sensors"

    # Merge and save
    merged_data = merge_csv_files(csv_directory)
    save_to_database(merged_data, database_name, table_name)

if __name__ == "__main__":
    main()
