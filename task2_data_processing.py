import pandas as pd
import os

# -------------------------------
# Step 1: Load JSON file
# -------------------------------

# Find latest JSON file in data folder
data_folder = "data"
json_files = [f for f in os.listdir(data_folder) if f.startswith("trends_") and f.endswith(".json")]

if not json_files:
    print("No JSON file found in data/ folder")
    exit()

# Take latest file
json_files.sort(reverse=True)
file_path = os.path.join(data_folder, json_files[0])

# Load JSON into DataFrame
df = pd.read_json(file_path)

print(f"Loaded {len(df)} stories from {file_path}")

# -------------------------------
# Step 2: Clean Data
# -------------------------------

# Remove duplicates based on post_id
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# Remove rows with missing critical fields
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# Remove low quality stories (score < 5)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Remove extra whitespace from title
df["title"] = df["title"].str.strip()

# -------------------------------
# Step 3: Save as CSV
# -------------------------------

output_file = os.path.join(data_folder, "trends_clean.csv")
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# -------------------------------
# Summary: Stories per category
# -------------------------------

print("\nStories per category:")
print(df["category"].value_counts())
