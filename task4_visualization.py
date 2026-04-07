import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------------
# Step 1: Load Data & Setup
# -------------------------------

file_path = "data/trends_analysed.csv"

if not os.path.exists(file_path):
    print("CSV not found. Run Task 3 first.")
    exit()

df = pd.read_csv(file_path)

# Create outputs folder
os.makedirs("outputs", exist_ok=True)

# -------------------------------
# Helper: shorten long titles
# -------------------------------
def shorten_title(title, max_len=50):
    return title if len(title) <= max_len else title[:max_len] + "..."

# -------------------------------
# Chart 1: Top 10 Stories by Score
# -------------------------------

top10 = df.sort_values(by="score", ascending=False).head(10)
titles = top10["title"].apply(shorten_title)

plt.figure()
plt.barh(titles, top10["score"])
plt.xlabel("Score")
plt.ylabel("Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# -------------------------------
# Chart 2: Stories per Category
# -------------------------------

category_counts = df["category"].value_counts()

plt.figure()
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

# -------------------------------
# Chart 3: Score vs Comments
# -------------------------------

plt.figure()

popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# -------------------------------
# Bonus: Dashboard
# -------------------------------

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Chart 1 (inside dashboard)
axes[0].barh(titles, top10["score"])
axes[0].set_title("Top Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# Chart 2
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Categories")
axes[1].set_xlabel("Category")

# Chart 3
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")

fig.suptitle("TrendPulse Dashboard")
axes[2].legend()

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

# -------------------------------
# Final Message
# -------------------------------

print("Charts saved successfully in outputs/ folder")
