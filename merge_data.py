
from pathlib import Path
import dask.dataframe as dd

# ==========================================
# 1. File paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

ACCIDENT_FILE = DATA_DIR / "Accident_Information.csv"
VEHICLE_FILE = DATA_DIR / "Vehicle_Information.csv"
OUTPUT_FILE = DATA_DIR / "UK_Road_Safety_Merged.csv"

# ==========================================
# 2. Select important columns
# ==========================================

accident_columns = [
    "Accident_Index",
    "Accident_Severity",
    "Date",
    "Weather_Conditions",
    "Road_Surface_Conditions",
    "Light_Conditions"
]

vehicle_columns = [
    "Accident_Index",
    "Vehicle_Type",
    "Age_Band_of_Driver",
    "Sex_of_Driver",
    "Age_of_Vehicle"
]

# ==========================================
# 3. Read CSV files using Dask
# ==========================================

print("Reading CSV files...")

accidents = dd.read_csv(
    ACCIDENT_FILE,
    usecols=accident_columns,
    dtype="object",
    encoding="latin1",
    blocksize="32MB"
)

vehicles = dd.read_csv(
    VEHICLE_FILE,
    usecols=vehicle_columns,
    dtype="object",
    encoding="latin1",
    blocksize="32MB"
)

# ==========================================
# 4. Merge datasets
# ==========================================

print("Merging datasets...")

merged = vehicles.merge(
    accidents,
    on="Accident_Index",
    how="inner"
)

# ==========================================
# 5. Arrange final 10 columns
# ==========================================

final_columns = [
    "Accident_Index",
    "Accident_Severity",
    "Date",
    "Weather_Conditions",
    "Road_Surface_Conditions",
    "Light_Conditions",
    "Vehicle_Type",
    "Age_Band_of_Driver",
    "Sex_of_Driver",
    "Age_of_Vehicle"
]

merged = merged[final_columns]

# ==========================================
# 6. Save as a single CSV file
# ==========================================

print("Saving merged CSV file...")

merged.to_csv(
    str(OUTPUT_FILE),
    single_file=True,
    index=False
)

# ==========================================
# 7. Display results
# ==========================================

size_mb = OUTPUT_FILE.stat().st_size / (1024 ** 2)

print("\n===== MERGE COMPLETED =====")
print("Output file:", OUTPUT_FILE)
print("Number of columns:", len(final_columns))
print(f"File size: {size_mb:.2f} MB")
