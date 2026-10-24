
from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ==========================================
# 1. Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "UK_Road_Safety_Merged.csv"
RESULTS_DIR = BASE_DIR / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. Load dataset
# ==========================================

print("===== UK ROAD SAFETY ANALYSIS =====")

df = pd.read_csv(DATA_PATH, low_memory=False)

print("Total vehicle records:", len(df))
print("Total columns:", df.shape[1])

# One row per accident
accidents = df.drop_duplicates(
    subset=["Accident_Index"]
).copy()

print("Unique accidents:", len(accidents))

# Convert dates
accidents["Date"] = pd.to_datetime(
    accidents["Date"],
    dayfirst=True,
    errors="coerce"
)

accidents["Year"] = accidents["Date"].dt.year

# ==========================================
# Helper function
# ==========================================

def save_chart(filename):
    plt.tight_layout()
    plt.savefig(
        RESULTS_DIR / filename,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()


# ==========================================
# 3. Accident severity
# ==========================================

print("\n1. ACCIDENT SEVERITY")

severity = accidents[
    "Accident_Severity"
].fillna("Missing").value_counts()

print(severity)

severity.to_csv(
    RESULTS_DIR / "severity.csv"
)

severity.plot(
    kind="bar",
    figsize=(9, 5),
    title="Accident Severity Distribution"
)

plt.xlabel("Accident Severity")
plt.ylabel("Number of Accidents")
save_chart("01_accident_severity.png")


# ==========================================
# 4. Accidents by year
# ==========================================

print("\n2. ACCIDENTS BY YEAR")

yearly = accidents[
    "Year"
].value_counts().sort_index()

print(yearly)

yearly.to_csv(
    RESULTS_DIR / "accidents_by_year.csv"
)

yearly.plot(
    kind="line",
    marker="o",
    figsize=(10, 5),
    title="Annual Road Accident Trend"
)

plt.xlabel("Year")
plt.ylabel("Number of Accidents")
plt.grid(True, alpha=0.3)
save_chart("02_accidents_by_year.png")


# ==========================================
# 5. Weather conditions
# ==========================================

print("\n3. WEATHER CONDITIONS")

weather = accidents[
    "Weather_Conditions"
].fillna("Missing").value_counts()

print(weather)

weather.to_csv(
    RESULTS_DIR / "weather_conditions.csv"
)

weather.sort_values().plot(
    kind="barh",
    figsize=(11, 6),
    title="Accidents by Weather Conditions"
)

plt.xlabel("Number of Accidents")
plt.ylabel("Weather Conditions")
save_chart("03_weather_conditions.png")


# ==========================================
# 6. Road surface conditions
# ==========================================

print("\n4. ROAD SURFACE CONDITIONS")

road = accidents[
    "Road_Surface_Conditions"
].fillna("Missing").value_counts()

print(road)

road.to_csv(
    RESULTS_DIR / "road_surface.csv"
)

road.plot(
    kind="bar",
    figsize=(10, 5),
    title="Accidents by Road Surface Conditions"
)

plt.xlabel("Road Surface")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=35, ha="right")
save_chart("04_road_surface.png")


# ==========================================
# 7. Light conditions
# ==========================================

print("\n5. LIGHT CONDITIONS")

light = accidents[
    "Light_Conditions"
].fillna("Missing").value_counts()

print(light)

light.to_csv(
    RESULTS_DIR / "light_conditions.csv"
)

light.sort_values().plot(
    kind="barh",
    figsize=(11, 6),
    title="Accidents by Light Conditions"
)

plt.xlabel("Number of Accidents")
plt.ylabel("Light Conditions")
save_chart("05_light_conditions.png")


# ==========================================
# 8. Severity vs weather
# ==========================================

print("\n6. SEVERITY VS WEATHER")

weather_severity = pd.crosstab(
    accidents["Weather_Conditions"].fillna("Missing"),
    accidents["Accident_Severity"].fillna("Missing")
)

print(weather_severity)

weather_severity.to_csv(
    RESULTS_DIR / "severity_vs_weather.csv"
)

weather_severity.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 6),
    title="Accident Severity by Weather Conditions"
)

plt.xlabel("Weather Conditions")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=40, ha="right")
save_chart("06_severity_vs_weather.png")


# ==========================================
# 9. Severity vs road surface
# ==========================================

print("\n7. SEVERITY VS ROAD SURFACE")

road_severity = pd.crosstab(
    accidents["Road_Surface_Conditions"].fillna("Missing"),
    accidents["Accident_Severity"].fillna("Missing")
)

print(road_severity)

road_severity.to_csv(
    RESULTS_DIR / "severity_vs_road.csv"
)

road_severity.plot(
    kind="bar",
    stacked=True,
    figsize=(12, 6),
    title="Accident Severity by Road Surface"
)

plt.xlabel("Road Surface Conditions")
plt.ylabel("Number of Accidents")
plt.xticks(rotation=35, ha="right")
save_chart("07_severity_vs_road.png")


# ==========================================
# 10. Missing values
# ==========================================

print("\n8. MISSING VALUES")

missing = df.isnull().sum()

missing_percent = (
    df.isnull().mean() * 100
).round(2)

missing_table = pd.DataFrame({
    "Missing_Count": missing,
    "Missing_Percentage": missing_percent
})

print(missing_table)

missing_table.to_csv(
    RESULTS_DIR / "missing_values.csv"
)

missing.plot(
    kind="bar",
    figsize=(11, 5),
    title="Missing Values by Column"
)

plt.xlabel("Columns")
plt.ylabel("Missing Values Count")
plt.xticks(rotation=45, ha="right")
save_chart("08_missing_values.png")


# ==========================================
# 11. Final summary
# ==========================================

print("\n===== FINAL SUMMARY =====")
print("Vehicle records:", len(df))
print("Unique accidents:", len(accidents))
print("Columns:", df.shape[1])
print("Charts generated:", 8)
print("Results folder:", RESULTS_DIR)

print("\n===== ANALYSIS COMPLETED SUCCESSFULLY =====")
