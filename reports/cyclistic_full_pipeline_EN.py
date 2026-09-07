# =============================================================================
# Cyclistic Case Study — Full 12-Month Automated Cleaning Pipeline (Python)
# =============================================================================
# This script cleans all twelve monthly files (July 2025 - June 2026) directly
# from the raw CSV source, applying the same cleaning logic that was manually
# built and validated in Excel, then merges everything into a single,
# size-optimized annual file.
#
# How to use in Jupyter Notebook:
#   Copy each section (separated by # %%) into its own cell, or run the whole
#   file at once.
# =============================================================================

# %%
import pandas as pd
from pathlib import Path

# -----------------------------------------------------------------------------
# 1) Configuration
# -----------------------------------------------------------------------------
RAW_DATA_FOLDER = Path("1. Raw Data")            # folder containing raw CSVs
CLEANED_FOLDER = Path("2. Working Files")         # per-month cleaned working copies
FINAL_OUTPUT = Path("cyclistic_12months_cleaned.csv")
LOG_OUTPUT = Path("3. Documentation/cleaning_log.csv")

CLEANED_FOLDER.mkdir(parents=True, exist_ok=True)
LOG_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# All twelve months, cleaned directly from their raw source files
MONTHS_TO_CLEAN = [
    "202507", "202508", "202509", "202510", "202511", "202512",
    "202601", "202602", "202603", "202604", "202605", "202606",
]

FINAL_COLUMNS = [
    "ride_id", "rideable_type", "started_at", "ended_at",
    "start_station_name", "start_station_id", "end_station_name", "end_station_id",
    "start_lat", "start_lng", "end_lat", "end_lng",
    "member_casual", "ride_length", "day_of_week",
]


# %%
# -----------------------------------------------------------------------------
# 2) Convert weekday to Divvy's convention (1=Sunday ... 7=Saturday)
# -----------------------------------------------------------------------------
def to_divvy_weekday(dt_series: pd.Series) -> pd.Series:
    """pandas: Monday=0 ... Sunday=6  |  Divvy: Sunday=1 ... Saturday=7"""
    pandas_dow = dt_series.dt.dayofweek
    return ((pandas_dow + 1) % 7) + 1


# %%
# -----------------------------------------------------------------------------
# 3) Clean a single raw monthly file
# -----------------------------------------------------------------------------
def clean_month(filepath: Path):
    month_id = filepath.stem[:6]

    df = pd.read_csv(filepath)
    original_count = len(df)

    df["started_at"] = pd.to_datetime(df["started_at"])
    df["ended_at"] = pd.to_datetime(df["ended_at"])

    df["ride_length"] = df["ended_at"] - df["started_at"]
    df["day_of_week"] = to_divvy_weekday(df["started_at"])

    # --- Three quality checks ---
    negative_rides = (df["ride_length"] < pd.Timedelta(0)).sum()
    long_rides = (df["ride_length"] > pd.Timedelta(days=1)).sum()
    short_rides = (df["ride_length"] < pd.Timedelta(minutes=1)).sum()
    missing_end_coords = df["end_lat"].isna().sum()

    # --- Exclusion: >24h or <60s (negative durations are covered automatically) ---
    to_delete = (df["ride_length"] > pd.Timedelta(days=1)) | (
        df["ride_length"] < pd.Timedelta(minutes=1)
    )
    cleaned_df = df.loc[~to_delete, FINAL_COLUMNS].copy()

    stats = {
        "month": month_id,
        "original_rows": original_count,
        "negative_ride_length": int(negative_rides),
        "removed_gt_24h": int(long_rides),
        "removed_lt_60s": int(short_rides),
        "missing_end_lat_lng": int(missing_end_coords),
        "final_rows": len(cleaned_df),
    }
    return cleaned_df, stats


# %%
# -----------------------------------------------------------------------------
# 4) Run — clean all twelve months + build the documentation log
# -----------------------------------------------------------------------------
all_cleaned_frames = []
log_rows = []

for month in MONTHS_TO_CLEAN:
    raw_file = RAW_DATA_FOLDER / f"{month}-divvy-tripdata.csv"
    if not raw_file.exists():
        print(f"⚠️  File not found, skipped: {raw_file}")
        continue

    print(f"Cleaning {month} ...")
    cleaned_df, stats = clean_month(raw_file)

    cleaned_df.to_csv(CLEANED_FOLDER / f"{month}-divvy-tripdata_cleaned.csv", index=False)

    all_cleaned_frames.append(cleaned_df)
    log_rows.append(stats)
    print(f"   ✅ {month}: {stats['original_rows']} → {stats['final_rows']} rows "
          f"(removed {stats['removed_gt_24h']} >24h, {stats['removed_lt_60s']} <60s)")


# %%
# -----------------------------------------------------------------------------
# 5) Final merge + size optimization + save (in the correct order) + log
# -----------------------------------------------------------------------------
final_df = pd.concat(all_cleaned_frames, ignore_index=True)
final_df = final_df.sort_values("started_at").reset_index(drop=True)

# --- Shrink file size before saving (must happen before to_csv) ---
final_df["ride_length"] = final_df["ride_length"].apply(
    lambda td: str(td).split(" ")[-1] if pd.notna(td) else td
)
final_df["started_at"] = final_df["started_at"].dt.strftime("%Y-%m-%d %H:%M:%S")
final_df["ended_at"] = final_df["ended_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

# --- Save now, after all transformations ---
final_df.to_csv(FINAL_OUTPUT, index=False)

log_df = pd.DataFrame(log_rows).sort_values("month")
log_df.to_csv(LOG_OUTPUT, index=False)

print("\n=== Final Summary ===")
print(f"Total rows in the combined annual file: {len(final_df):,}")
print(f"Final file: {FINAL_OUTPUT}")
print(f"Documentation log: {LOG_OUTPUT}")
print(log_df)


# %%
# -----------------------------------------------------------------------------
# 6) Analyze stage — prepare data for statistical analysis
# -----------------------------------------------------------------------------
df = pd.read_csv(FINAL_OUTPUT)

df["ride_length"] = pd.to_timedelta(df["ride_length"])
df["started_at"] = pd.to_datetime(df["started_at"])
df["ended_at"] = pd.to_datetime(df["ended_at"])
df["ride_length_sec"] = df["ride_length"].dt.total_seconds()

# --- Core comparison: ride duration by user type ---
duration_summary = df.groupby("member_casual")["ride_length_sec"].agg(["mean", "median", "count"])
print("\n=== Ride duration by user type (seconds) ===")
print(duration_summary)

# --- Ride count by day of week and user type ---
weekday_summary = df.groupby(["member_casual", "day_of_week"]).size().unstack(level=0)
print("\n=== Ride count by day of week ===")
print(weekday_summary)

# --- Bike type by user type (percentage) ---
ride_type_summary = df.groupby(["member_casual", "rideable_type"]).size().unstack(level=0)
ride_type_pct = ride_type_summary.div(ride_type_summary.sum(axis=0), axis=1) * 100
print("\n=== Bike type share by user type ===")
print(ride_type_pct.round(1))

# --- Monthly trend ---
df["month"] = df["started_at"].dt.to_period("M")
monthly_summary = df.groupby(["month", "member_casual"]).size().unstack(level=1)
print("\n=== Monthly trend ===")
print(monthly_summary)

# --- Export summary tables to Excel for charting ---
with pd.ExcelWriter("cyclistic_summary_tables.xlsx") as writer:
    duration_summary.to_excel(writer, sheet_name="ride_duration")
    weekday_summary.to_excel(writer, sheet_name="by_weekday")
    ride_type_pct.to_excel(writer, sheet_name="bike_type_pct")
    monthly_summary.to_excel(writer, sheet_name="monthly_trend")

print("\nSummary tables exported: cyclistic_summary_tables.xlsx")
