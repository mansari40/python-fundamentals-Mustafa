import pandas as pd
import numpy as np
from functools import partial


# Create sample data (task 1)
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Alice"],
    "Age": [25, "thirty", 35, np.nan, 45, 50, "55", 25],
    "City": [
        "New York",
        "Los Angeles",
        "Chicago",
        "Houston",
        "Phoenix",
        "Philadelphia",
        "San Antonio",
        "New York",
    ],
    "RegistrationDate": [
        "2020-01-01",
        "2021-02-02",
        "2022-03-03",
        np.nan,
        "2023-05-05",
        "2024-06-06",
        "2025-07-07",
        "2020-01-01",
    ],
}

# Turn it into a DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv("user_data.csv", index=False)
print("CSV file created: user_data.csv")

# Load the data back in
df = pd.read_csv("user_data.csv")
print(df)

# Simple Series with custom index (Task 2)
custom_index = ["user1", "user2", "user3"]
s = pd.Series([100, 200, 300], index=custom_index)
print("\nCustom Series:")
print(s)

# Create a pandas dataframe (Task3)
df = pd.DataFrame(data)

# Inspect the DataFrame (Task 4)
# Inspect basics
print("\nData types:")
print(df.dtypes)

print("\nFirst 3 rows:")
print(df.head(3))

print("\nLast 2 rows:")
print(df.tail(2))

print("\nSummary stats:")
print(df.describe())


# Data slicing by row position and column name (Task 5)

# Slice by row position (first 3 rows)
print("\nFirst 3 rows by position:")
print(df.iloc[0:3])

# Slice by column name (just Name and City)
print("\nName and City columns:")
print(df[["Name", "City"]])


# Slice using boolean flags and data range (Task 6)
flags = [True, False, True, False, True, False, True, False]
print("\nRows selected by boolean flags:")
print(df[flags])

# Filter by range (Ages between 30 and 50)
temp_df = df.copy()
temp_df["Age"] = pd.to_numeric(temp_df["Age"], errors="coerce")
print("\nAges between 30 and 50:")
print(temp_df[(temp_df["Age"] > 30) & (temp_df["Age"] <= 50)])

# Data cleaning with duplicated, nunique, drop_duplicates (Task 7)

# Check for duplicates
print("\nDuplicates:")
print(df.duplicated())

# Unique counts per column
print("\nUnique values per column:")
print(df.nunique())

# Drop duplicates
df_clean = df.drop_duplicates()
print("\nAfter dropping duplicates:")
print(df_clean)

# Safe type conversion with pd.to_numeric and pd.to_datetime (Task 8)

# Convert Age to numeric (strings like 'thirty' become NaN)
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

# Convert RegistrationDate to datetime
df["RegistrationDate"] = pd.to_datetime(df["RegistrationDate"], errors="coerce")

print("\nAfter type conversion:")
print(df.dtypes)
print(df)

# Set default values for missing data using .apply() (Task 9)


# Set default values for missing Age
def set_default(x: float) -> float:
    if pd.isna(x):
        return 30.0
    return float(x)


# Apply to Age
df["Age"] = df["Age"].apply(set_default)

print("\nAfter setting defaults for missing Age:")
print(df)
print(df.isnull().sum())

# Data cleaning pipeline with .pipe() for type conversion (Task 10)


# Define a cleaning function
def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
    df["RegistrationDate"] = pd.to_datetime(df["RegistrationDate"], errors="coerce")
    print("\nIn pipeline: dtypes after conversion")
    print(df.dtypes)
    print("Null counts:")
    print(df.isnull().sum())
    return df


# Reload original for demo
df = pd.read_csv("user_data.csv")

# Use pipe
df = df.pipe(convert_types)

print("\nFinal df after pipe:")
print(df)

# .pipe() with partial arguments and threshold (Task 11)


# Function with threshold
def drop_high_missing(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    missing_perc = df.isnull().mean()
    cols_to_drop = missing_perc[missing_perc > threshold].index
    df = df.drop(columns=cols_to_drop)
    print(f"\nIn pipeline: Dropped columns with >{threshold*100}% missing")
    print(df.columns)
    return df


# Use partial for threshold in pipe
df = df.pipe(partial(drop_high_missing, threshold=0.2))  # 20%

print("\nFinal df after threshold pipe:")
print(df)
