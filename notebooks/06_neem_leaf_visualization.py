
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Project root: the parent of the notebooks folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Path to the CSV exported from MySQL Workbench
csv_path = PROJECT_ROOT / "reports" / "neem_leaf_monthly_market_trends.csv"

# Load the exported data
df = pd.read_csv(csv_path)

# Expected columns
expected_columns = [
    "market",
    "source_year",
    "reporting_month",
    "reporting_month_name",
    "positive_observations",
    "monthly_median_price",
]

# Display basic information
print("File found:", csv_path.exists())
print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst five rows:")
print(df.head().to_string(index=False))

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nExpected columns present:")
print(set(expected_columns).issubset(df.columns))

if set(expected_columns).issubset(df.columns):
    print("\nMarkets:", sorted(df["market"].dropna().unique()))
    print("Years covered:", sorted(df["source_year"].dropna().unique()))
    print("Total observations:", df["positive_observations"].sum())
else:
    print("\nWARNING: One or more expected columns are missing.")

# Convert year and month into a real date for chronological plotting
df["month_date"] = pd.to_datetime(
    df["source_year"].astype(str)
    + "-"
    + df["reporting_month"].astype(str).str.zfill(2)
    + "-01"
)

# Create a directory for the chart
chart_dir = PROJECT_ROOT / "reports" / "charts"
chart_dir.mkdir(parents=True, exist_ok=True)

markets = ["Berhampur", "Kolkata", "Silliguri"]

for market in markets:
    market_df = (
        df[df["market"] == market]
        .sort_values("month_date")
        .copy()
    )

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        market_df["month_date"],
        market_df["monthly_median_price"],
        marker="o",
        linewidth=1.8,
        markersize=5,
        label="Monthly median price",
    )

    # Flag the confirmed source value that remains under review
    if market == "Kolkata":
        extreme = market_df[
            (market_df["source_year"] == 2023)
            & (market_df["reporting_month"] == 6)
        ]

        if not extreme.empty:
            ax.scatter(
                extreme["month_date"],
                extreme["monthly_median_price"],
                marker="X",
                s=110,
                label="Extreme value under review",
                zorder=5,
            )

            ax.annotate(
                "40,240: validate unit and context",
                xy=(
                    extreme["month_date"].iloc[0],
                    extreme["monthly_median_price"].iloc[0],
                ),
                xytext=(10, -25),
                textcoords="offset points",
                fontsize=9,
                arrowprops={"arrowstyle": "->"},
            )

    ax.set_title(f"Neem-Leaf Monthly Median Price: {market}")
    ax.set_xlabel("Month")
    ax.set_ylabel("Median price (source unit unconfirmed)")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    output_path = chart_dir / f"neem_leaf_monthly_trend_{market.lower()}.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight")

    print(f"Saved chart: {output_path}")

    plt.show()
    plt.close(fig)


# Step 13: Kolkata trend with a focused view and full-scale view

kolkata_df = (
    df[df["market"] == "Kolkata"]
    .sort_values("month_date")
    .copy()
)

fig, (ax_focus, ax_full) = plt.subplots(
    2, 1, figsize=(12, 8), sharex=True
)

# Panel 1: Focus on the ordinary price range
ax_focus.plot(
    kolkata_df["month_date"],
    kolkata_df["monthly_median_price"],
    marker="o",
    linewidth=1.8,
)
ax_focus.set_ylim(0, 200)
ax_focus.set_title("Kolkata: Focused View (0 to 200)")
ax_focus.set_ylabel("Median price")
ax_focus.grid(True, alpha=0.3)

# Panel 2: Preserve and display the complete value range
ax_full.plot(
    kolkata_df["month_date"],
    kolkata_df["monthly_median_price"],
    marker="o",
    linewidth=1.5,
)
ax_full.set_title("Kolkata: Full Price Range")
ax_full.set_ylabel("Median price")
ax_full.set_xlabel("Month")
ax_full.grid(True, alpha=0.3)

ax_full.xaxis.set_major_locator(mdates.YearLocator())
ax_full.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

fig.suptitle(
    "Neem-Leaf Monthly Median Price: Kolkata",
    fontsize=14,
)
fig.tight_layout()

output_path = (
    PROJECT_ROOT
    / "reports"
    / "charts"
    / "neem_leaf_monthly_trend_kolkata_comparison.png"
)

fig.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"Saved chart: {output_path}")

plt.show()
plt.close(fig)



# Step 14: Kolkata trend with the flagged observation shown separately

kolkata_df = (
    df[df["market"] == "Kolkata"]
    .sort_values("month_date")
    .copy()
)

# Identify the extreme observation
extreme_mask = (
    (kolkata_df["source_year"] == 2023)
    & (kolkata_df["reporting_month"] == 6)
)

extreme_df = kolkata_df[extreme_mask].copy()

# Exclude the flagged record from the focused trend line only.
# The original dataframe remains unchanged.
trend_df = kolkata_df[~extreme_mask].copy()
trend_df = trend_df.sort_values("month_date")

# Break the line across gaps longer than 35 days
month_gap = trend_df["month_date"].diff().dt.days > 35

trend_df["plot_price"] = trend_df["monthly_median_price"].where(
    ~month_gap
)

# Restore the first observation so the first segment is plotted
if not trend_df.empty:
    trend_df.loc[trend_df.index[0], "plot_price"] = (
        trend_df.loc[trend_df.index[0], "monthly_median_price"]
    )

# Create the chart
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    trend_df["month_date"],
    trend_df["plot_price"],  # Corrected: use plot_price
    marker="o",
    linewidth=1.8,
    label="Monthly median, excluding flagged point",
)

# Display the extreme source value separately
if not extreme_df.empty:
    ax.scatter(
        extreme_df["month_date"],
        extreme_df["monthly_median_price"],
        marker="X",
        s=110,
        label="Flagged source value: 40,240",
        zorder=5,
        clip_on=False,
    )

    ax.annotate(
        "June 2023: 40,240\nUnit and context unconfirmed",
        xy=(
            extreme_df["month_date"].iloc[0],
            extreme_df["monthly_median_price"].iloc[0],
        ),
        xytext=(10, 15),
        textcoords="offset points",
        arrowprops={"arrowstyle": "->"},
        fontsize=9,
    )

ax.set_ylim(0, 200)
ax.set_title("Neem-Leaf Monthly Median Price: Kolkata")
ax.set_xlabel("Month")
ax.set_ylabel("Median price (source unit unconfirmed)")

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

ax.grid(True, alpha=0.3)
ax.legend()
fig.tight_layout()

output_path = (
    PROJECT_ROOT
    / "reports"
    / "charts"
    / "neem_leaf_monthly_trend_kolkata_final.png"
)

fig.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"Saved chart: {output_path}")

plt.show()
plt.close(fig)
