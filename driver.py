import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the dataset (Assume CSV file with cost of living data)
data = pd.read_csv("./data/cost_of_living_us.csv")  # Update with actual file path


# Filter for Tennessee data only
tennessee_data = data[data["state"] == "TN"]


# Aggregate cost of living by county (taking the average)
tennessee_data_grouped = (
    tennessee_data.groupby("county").agg({"total_cost": "mean"}).reset_index()
)

# Remove " County" from county names in the cost-of-living dataset
tennessee_data_grouped["county"] = tennessee_data_grouped["county"].str.replace(
    " County", "", regex=True
)


# Load a shapefile of US counties (You may need to download it from a source like the US Census Bureau)
shapefile_path = (
    "./data/tennessee_shape/tennessee_counties.shp"  # Update with actual file path
)
tennessee_map = gpd.read_file(shapefile_path)


# Merge shapefile with cost of living data
tennessee_map = tennessee_map.merge(
    tennessee_data_grouped, left_on="NAME", right_on="county", how="left"
)


# Plot the heatmap
fig, ax = plt.subplots(figsize=(12, 8))
tennessee_map.plot(
    column="total_cost",
    cmap="OrRd",
    linewidth=0.8,
    edgecolor="black",
    legend=True,
    ax=ax,
    missing_kwds={"color": "lightgrey", "label": "No Data"},
)

ax.set_title("Cost of Living Heatmap by County in Tennessee", fontsize=14)
ax.axis("off")

# Show the heatmap
plt.show()
