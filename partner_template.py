import os
import pandas as pd
import altair as alt

alt.data_transformers.disable_max_rows()

os.makedirs("visualizations", exist_ok=True)

print("=" * 60)
print("Creating Part 1 Visualizations")
print("=" * 60)

def load_csv(fname: str) -> pd.DataFrame:
    path1 = os.path.join("data", "processed", fname)
    path2 = fname

    if os.path.exists(path1):
        print(f"Loading {path1}")
        return pd.read_csv(path1)
    elif os.path.exists(path2):
        print(f"Loading {path2}")
        return pd.read_csv(path2)
    else:
        raise FileNotFoundError(
            f"Could not find {fname} in data/processed/ or current directory."
        )

# ============================================================================
# Visualization 1: Geographic Distribution of Severe Cost Burden
# ============================================================================
print("\n1. Creating geographic distribution visualization...")

try:
    coverage = load_csv("policy_coverage.csv")
    mix = load_csv("policy_mix.csv")
    burden_geo = coverage.merge(
        mix[["city", "city_type"]], on="city", how="left"
    )

    chart1 = (
        alt.Chart(burden_geo)
        .mark_bar()
        .encode(
            x=alt.X(
                "city:N",
                title="City",
                axis=alt.Axis(labelAngle=-45),
                sort="-y",
            ),
            y=alt.Y(
                "severe_cost_burden_renters:Q",
                title="Severely Cost-Burdened Renters",
            ),
            color=alt.Color(
                "city_type:N",
                title="City Type",
            ),
            tooltip=[
                alt.Tooltip("city:N", title="City"),
                alt.Tooltip("city_type:N", title="City Type"),
                alt.Tooltip(
                    "severe_cost_burden_renters:Q",
                    format=",d",
                    title="Severely Burdened Renters",
                ),
                alt.Tooltip(
                    "subsidized_per_100_burdened:Q",
                    format=".1f",
                    title="Subsidized Units per 100 Burdened",
                ),
            ],
        )
        .properties(
            width=700,
            height=400,
            title="Where Severe Cost Burden Is Concentrated (by City)",
        )
    )

    chart1.save("visualizations/burden_geographic_distribution.html")
    print("Saved: visualizations/burden_geographic_distribution.html")

except FileNotFoundError:
    print(
        "WARNING: policy_coverage.csv or policy_mix.csv not found. "
        "Skipping chart 1."
    )
except Exception as e:
    print(f"ERROR creating chart 1: {e}")


# ============================================================================
# Visualization 2: Burden & Coverage by City Type
# (saved to burden_by_income_group.html to match the article)
# ============================================================================
print("\n2. Creating 'income group' visualization (by city type)...")

try:
    coverage = load_csv("policy_coverage.csv")
    mix = load_csv("policy_mix.csv")
    merged = coverage.merge(
        mix[["city", "city_type"]], on="city", how="left"
    )

    by_type = (
        merged.groupby("city_type", as_index=False)
        .agg(
            total_severe=("severe_cost_burden_renters", "sum"),
            total_subsidized=("total_subsidized", "sum"),
        )
    )

    # Share of all severely burdened renters by city type
    by_type["severely_burdened_pct"] = (
        by_type["total_severe"] / by_type["total_severe"].sum() * 100.0
    )

    # Subsidized units per 100 severely burdened renters
    by_type["subsidized_per_100_burdened"] = (
        by_type["total_subsidized"] / by_type["total_severe"] * 100.0
    )

    # Rename for backward compatibility with HTML (x-axis label will clarify)
    by_type = by_type.rename(columns={"city_type": "income_group"})

    # Add label offset based on position to avoid overlap
    # Use smaller, more reasonable offsets
    median_y = by_type["subsidized_per_100_burdened"].median()
    
    # Calculate size factor for dynamic offset (smaller range)
    max_size = by_type["total_severe"].max()
    min_size = by_type["total_severe"].min()
    
    # Simple strategy: labels above for lower points, below for upper points
    # Use moderate offsets that scale with circle size
    by_type["label_dy"] = by_type.apply(
        lambda row: -25 - (row["total_severe"] - min_size) / (max_size - min_size) * 10 if row["subsidized_per_100_burdened"] > median_y 
        else 25 + (row["total_severe"] - min_size) / (max_size - min_size) * 10, axis=1
    )
    # Small horizontal offset to avoid direct overlap
    by_type["label_dx"] = by_type.apply(
        lambda row: 1.5 + (row["total_severe"] - min_size) / (max_size - min_size) * 0.5, axis=1
    )

    # Overall reference values for lines
    overall_share = by_type["severely_burdened_pct"].mean()
    overall_coverage = by_type["subsidized_per_100_burdened"].mean()

    ref_x = pd.DataFrame({"severely_burdened_pct": [overall_share]})
    ref_y = pd.DataFrame({"subsidized_per_100_burdened": [overall_coverage]})

    # Interactive selection: click to highlight a city type
    select_type = alt.selection_point(fields=["income_group"], empty="all")

    base = alt.Chart(by_type).encode(
        x=alt.X(
            "severely_burdened_pct:Q",
            title="Share of All Severely Burdened Renters (%)"
        ),
        y=alt.Y(
            "subsidized_per_100_burdened:Q",
            title="Subsidized Units per 100 Severely Burdened"
        ),
        color=alt.Color(
            "income_group:N",
            title="City Type"
        ),
        tooltip=[
            alt.Tooltip("income_group:N", title="City Type"),
            alt.Tooltip(
                "total_severe:Q",
                format=",d",
                title="Severely Burdened Renters"
            ),
            alt.Tooltip(
                "severely_burdened_pct:Q",
                format=".1f",
                title="Share of All Severely Burdened (%)"
            ),
            alt.Tooltip(
                "subsidized_per_100_burdened:Q",
                format=".1f",
                title="Subsidized per 100 Burdened"
            ),
        ],
    )

    # Scatter points (size = total severe)
    points = base.mark_circle().encode(
        size=alt.Size(
            "total_severe:Q",
            title="Severely Burdened Renters",
            scale=alt.Scale(range=[300, 2000])
        ),
        opacity=alt.condition(select_type, alt.value(1.0), alt.value(0.35)),
    ).add_selection(select_type)

    # Labels with smart positioning to avoid overlap
    # Calculate label positions with larger offsets
    labels = alt.Chart(by_type).transform_calculate(
        label_x="datum.severely_burdened_pct + datum.label_dx",  # Offset in percentage points
        label_y="datum.subsidized_per_100_burdened + datum.label_dy"  # Offset in units
    ).mark_text(
        fontSize=13,
        fontWeight="bold",
        align="center",
        baseline="middle"
    ).encode(
        x=alt.X(
            "label_x:Q",
            title="Share of All Severely Burdened Renters (%)"
        ),
        y=alt.Y(
            "label_y:Q",
            title="Subsidized Units per 100 Severely Burdened"
        ),
        text="income_group:N",
        color=alt.Color(
            "income_group:N",
            title="City Type"
        ),
        opacity=alt.condition(select_type, alt.value(1.0), alt.value(0.7)),
        tooltip=[
            alt.Tooltip("income_group:N", title="City Type"),
            alt.Tooltip(
                "total_severe:Q",
                format=",d",
                title="Severely Burdened Renters"
            ),
            alt.Tooltip(
                "severely_burdened_pct:Q",
                format=".1f",
                title="Share of All Severely Burdened (%)"
            ),
            alt.Tooltip(
                "subsidized_per_100_burdened:Q",
                format=".1f",
                title="Subsidized per 100 Burdened"
            ),
        ],
    )

    # Vertical and horizontal reference lines for "overall" levels
    vline = alt.Chart(ref_x).mark_rule(strokeDash=[4, 4], color="gray").encode(
        x="severely_burdened_pct:Q"
    )

    hline = alt.Chart(ref_y).mark_rule(strokeDash=[4, 4], color="gray").encode(
        y="subsidized_per_100_burdened:Q"
    )

    chart2 = (
        alt.layer(points, labels, vline, hline)
        .properties(
            width=800,  # Increased width for more space
            height=500,  # Increased height for more space
            title="Cost Burden vs. Coverage by City Type"
        )
        .configure_view(
            strokeWidth=0,
            fill="#ffffff"
        )
    )

    chart2.save("visualizations/burden_by_income_group.html")
    print("Saved: visualizations/burden_by_income_group.html")

except FileNotFoundError:
    print(
        "WARNING: policy_coverage.csv or policy_mix.csv not found. "
        "Skipping chart 2."
    )
except Exception as e:
    print(f"ERROR creating chart 2: {e}")


# ============================================================================
# Visualization 3: COVID-19 Impact Trends (Interactive Circle Plot, No Lines)
# ============================================================================
print("\n3. Creating COVID trends visualization...")

def load_from_data_folder(fname):
    path1 = os.path.join("data", fname)
    path2 = fname
    if os.path.exists(path1):
        print(f"Loading {path1}")
        return pd.read_csv(path1)
    if os.path.exists(path2):
        print(f"Loading {path2}")
        return pd.read_csv(path2)
    raise FileNotFoundError(f"{fname} not found in data/ or current directory.")

try:
    hpi = load_from_data_folder("hpi_master.csv")
    zhvi = load_from_data_folder("Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv")
    hpi_us = hpi[
        (hpi["place_name"] == "United States") &
        (hpi["frequency"] == "monthly")
    ].copy()

    hpi_us["month"] = hpi_us["period"].astype(int)
    hpi_us["date"] = pd.to_datetime(
        hpi_us["yr"].astype(str) + "-" + hpi_us["month"].astype(str) + "-01"
    )
    hpi_us["year"] = hpi_us["date"].dt.year

    hpi_year = (
        hpi_us.groupby("year", as_index=False)["index_sa"]
        .mean()
        .rename(columns={"index_sa": "hpi_index"})
    )
    hpi_year = hpi_year[hpi_year["year"] >= 2010]

    zhvi_us = zhvi[zhvi["RegionName"] == "United States"].copy()
    date_cols = [
        c for c in zhvi_us.columns
        if c not in ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]
    ]

    zhvi_long = zhvi_us.melt(
        id_vars=["RegionName"],
        value_vars=date_cols,
        var_name="date_str",
        value_name="zhvi"
    )

    zhvi_long["date"] = pd.to_datetime(zhvi_long["date_str"], errors="coerce")
    zhvi_long = zhvi_long.dropna(subset=["date"])
    zhvi_long["year"] = zhvi_long["date"].dt.year

    zhvi_year = zhvi_long.groupby("year", as_index=False)["zhvi"].mean()
    zhvi_year = zhvi_year[zhvi_year["year"] >= 2010]

    covid_trends = pd.merge(hpi_year, zhvi_year, on="year", how="inner")
    hover = alt.selection_point(fields=["year"], nearest=True, on="mouseover")
    brush = alt.selection_interval(encodings=["x"])

    base = (
        alt.Chart(covid_trends)
        .encode(x=alt.X("year:O", title="Year"))
        .add_selection(brush)
        .transform_filter(brush)
    )

    hpi_points = base.mark_circle(size=120, opacity=0.7, color="#e74c3c").encode(
        y=alt.Y("hpi_index:Q", title="FHFA House Price Index"),
        tooltip=[
            alt.Tooltip("year:O", title="Year"),
            alt.Tooltip("hpi_index:Q", format=".1f", title="FHFA HPI")
        ],
        opacity=alt.condition(hover, alt.value(1), alt.value(0.4))
    )

    zhvi_points = base.mark_circle(size=120, opacity=0.7, color="#3498db").encode(
        y=alt.Y("zhvi:Q", title="Typical Home Value ($)", axis=alt.Axis(format="$,.0f")),
        tooltip=[
            alt.Tooltip("year:O", title="Year"),
            alt.Tooltip("zhvi:Q", format="$,.0f", title="ZHVI (Home Value)")
        ],
        opacity=alt.condition(hover, alt.value(1), alt.value(0.4))
    )

    hover_rule = base.mark_rule(color="gray").encode(
        x="year:O"
    ).add_selection(hover)

    chart3 = (
        alt.layer(hpi_points, zhvi_points, hover_rule)
        .resolve_scale(y="independent")
        .properties(
            width=800,
            height=420,
            title="COVID-19 Housing Cost Surge"
        )
    )

    chart3.save("visualizations/covid_trends.html")
    print("Saved: visualizations/covid_trends.html")

except Exception as e:
    print(f"ERROR creating chart 3: {e}")
