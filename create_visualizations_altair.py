"""
Create visualizations using Altair
"""
import pandas as pd
import altair as alt
import json
import os

# Configure Altair
alt.data_transformers.disable_max_rows()

# Create visualizations directory
os.makedirs('visualizations', exist_ok=True)

print("="*60)
print("Creating Visualizations with Altair")
print("="*60)

# Load data
try:
    policy_coverage = pd.read_csv('data/processed/policy_coverage.csv')
    policy_mix = pd.read_csv('data/processed/policy_mix.csv')
    expiring_units = pd.read_csv('data/processed/expiring_units.csv')
    print("✓ Data loaded successfully")
except Exception as e:
    print(f"✗ Error loading data: {e}")
    exit(1)

# ============================================================================
# Visualization 1: Coverage Gap Analysis - Demand vs Supply
# ============================================================================
print("\n1. Creating coverage gap analysis visualization...")

# Prepare data: merge demand (cost burden renters) and supply (subsidized units)
coverage_viz_data = policy_coverage.melt(
    id_vars=['city'],
    value_vars=['severe_cost_burden_renters', 'total_subsidized'],
    var_name='type',
    value_name='count'
)

coverage_viz_data['type_label'] = coverage_viz_data['type'].map({
    'severe_cost_burden_renters': 'Severely Cost-Burdened Renters (Demand)',
    'total_subsidized': 'Subsidized Housing Units (Supply)'
})

chart1 = alt.Chart(coverage_viz_data).mark_bar().encode(
    x=alt.X('city:N', title='City', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('count:Q', title='Count', scale=alt.Scale(type='log')),
    color=alt.Color('type_label:N', 
                   title='Type',
                   scale=alt.Scale(domain=['Severely Cost-Burdened Renters (Demand)', 'Subsidized Housing Units (Supply)'],
                                  range=['#d62728', '#2ca02c'])),
    column=alt.Column('type_label:N', header=alt.Header(title='')),
    tooltip=['city', 'type_label', alt.Tooltip('count:Q', format=',.0f')]
).properties(
    width=300,
    height=300,
    title='Affordable Housing Coverage Gap: Demand vs Supply'
).configure_view(
    stroke=None
).configure_axis(
    labelFontSize=11,
    titleFontSize=12
)

chart1.save('visualizations/coverage_gap_altair.html')
print("✓ Saved: visualizations/coverage_gap_altair.html")

# Create coverage ratio chart
coverage_ratio_chart = alt.Chart(policy_coverage).mark_bar().encode(
    x=alt.X('city:N', title='City', sort='-y', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('subsidized_per_100_burdened:Q', 
            title='Subsidized Units per 100 Severely Burdened Renters',
            scale=alt.Scale(domain=[0, 150])),
    color=alt.Color('subsidized_per_100_burdened:Q',
                   scale=alt.Scale(scheme='redyellowgreen', domain=[0, 100]),
                   legend=alt.Legend(title='Coverage Ratio')),
    tooltip=['city', 
            alt.Tooltip('severe_cost_burden_renters:Q', format=',.0f', title='Severely Burdened Renters'),
            alt.Tooltip('total_subsidized:Q', format=',.0f', title='Subsidized Units'),
            alt.Tooltip('subsidized_per_100_burdened:Q', format='.1f', title='Coverage Ratio')]
).properties(
    width=600,
    height=400,
    title='Affordable Housing Coverage Ratio: Subsidized Units vs Demand'
).configure_axis(
    labelFontSize=11,
    titleFontSize=12
)

coverage_ratio_chart.save('visualizations/coverage_ratio_altair.html')
print("✓ Saved: visualizations/coverage_ratio_altair.html")

# ============================================================================
# Visualization 2: Policy Mix Comparison
# ============================================================================
print("\n2. Creating policy mix comparison visualization...")

# Prepare stacked bar chart data
policy_mix_long = policy_mix.melt(
    id_vars=['city', 'city_type'],
    value_vars=['public_housing_pct', 'voucher_pct', 'lihtc_pct', 'section8_pct', 'iz_pct'],
    var_name='policy_tool',
    value_name='percentage'
)

policy_mix_long['policy_label'] = policy_mix_long['policy_tool'].map({
    'public_housing_pct': 'Public Housing',
    'voucher_pct': 'Housing Vouchers',
    'lihtc_pct': 'LIHTC',
    'section8_pct': 'Section 8 Project-Based',
    'iz_pct': 'Inclusionary Zoning (IZ)'
})

chart2 = alt.Chart(policy_mix_long).mark_bar().encode(
    x=alt.X('city:N', title='City', sort='-y', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('percentage:Q', title='Percentage (%)', stack='normalize'),
    color=alt.Color('policy_label:N',
                   title='Policy Tool',
                   scale=alt.Scale(scheme='category10')),
    order=alt.Order('policy_tool:O', sort='ascending'),
    tooltip=['city', 'city_type', 'policy_label', 
            alt.Tooltip('percentage:Q', format='.1f', title='Percentage (%)')]
).properties(
    width=700,
    height=400,
    title='Affordable Housing Policy Tool Mix by City'
).configure_axis(
    labelFontSize=11,
    titleFontSize=12
)

chart2.save('visualizations/policy_mix_altair.html')
print("✓ Saved: visualizations/policy_mix_altair.html")

# Grouped by city type version
chart2_grouped = alt.Chart(policy_mix_long).mark_bar().encode(
    x=alt.X('city:N', title='City', axis=alt.Axis(labelAngle=-45)),
    y=alt.Y('percentage:Q', title='Percentage (%)', stack='normalize'),
    color=alt.Color('policy_label:N',
                   title='Policy Tool',
                   scale=alt.Scale(scheme='category10')),
    column=alt.Column('city_type:N', header=alt.Header(title='City Type')),
    order=alt.Order('policy_tool:O', sort='ascending'),
    tooltip=['city', 'policy_label', 
            alt.Tooltip('percentage:Q', format='.1f', title='Percentage (%)')]
).properties(
    width=200,
    height=300,
    title='Policy Tool Mix Grouped by City Type'
).configure_view(
    stroke=None
)

chart2_grouped.save('visualizations/policy_mix_by_type_altair.html')
print("✓ Saved: visualizations/policy_mix_by_type_altair.html")

# ============================================================================
# Visualization 3: Future Risk Analysis - Expiring Affordable Units
# ============================================================================
print("\n3. Creating future risk analysis visualization...")

# Aggregate by city and year
expiring_summary = expiring_units.groupby(['city', 'year']).agg({
    'expiring_units': 'sum'
}).reset_index()

chart3 = alt.Chart(expiring_summary).mark_line(point=True).encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y('expiring_units:Q', title='Expiring Units', aggregate='sum'),
    color=alt.Color('city:N', title='City', scale=alt.Scale(scheme='category20')),
    tooltip=['city', 'year', 
            alt.Tooltip('expiring_units:Q', format=',.0f', title='Expiring Units')]
).properties(
    width=800,
    height=400,
    title='Affordable Housing Unit Expiration Forecast: Next 20 Years'
).configure_axis(
    labelFontSize=11,
    titleFontSize=12
)

chart3.save('visualizations/expiring_units_timeline_altair.html')
print("✓ Saved: visualizations/expiring_units_timeline_altair.html")

# Create stacked area chart showing cumulative risk
expiring_cumulative = expiring_units.groupby(['city', 'year']).agg({
    'expiring_units': 'sum'
}).reset_index().sort_values(['city', 'year'])

expiring_cumulative['cumulative'] = expiring_cumulative.groupby('city')['expiring_units'].cumsum()

chart3_area = alt.Chart(expiring_cumulative).mark_area(opacity=0.7).encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y('cumulative:Q', title='Cumulative Expiring Units', stack='normalize'),
    color=alt.Color('city:N', title='City', scale=alt.Scale(scheme='category20')),
    tooltip=['city', 'year', 
            alt.Tooltip('expiring_units:Q', format=',.0f', title='Expiring This Year'),
            alt.Tooltip('cumulative:Q', format=',.0f', title='Cumulative Expiring')]
).properties(
    width=800,
    height=400,
    title='Cumulative Expiring Units Forecast (Normalized)'
).configure_axis(
    labelFontSize=11,
    titleFontSize=12
)

chart3_area.save('visualizations/expiring_units_cumulative_altair.html')
print("✓ Saved: visualizations/expiring_units_cumulative_altair.html")

# Create heatmap showing risk concentration
chart3_heatmap = alt.Chart(expiring_summary).mark_rect().encode(
    x=alt.X('year:O', title='Year'),
    y=alt.Y('city:N', title='City', sort='-x'),
    color=alt.Color('expiring_units:Q',
                   title='Expiring Units',
                   scale=alt.Scale(scheme='reds')),
    tooltip=['city', 'year', 
            alt.Tooltip('expiring_units:Q', format=',.0f', title='Expiring Units')]
).properties(
    width=900,
    height=400,
    title='Affordable Housing Unit Expiration Risk Heatmap'
).configure_axis(
    labelFontSize=11,
    titleFontSize=12
)

chart3_heatmap.save('visualizations/expiring_units_heatmap_altair.html')
print("✓ Saved: visualizations/expiring_units_heatmap_altair.html")

print("\n" + "="*60)
print("All Altair visualizations created successfully!")
print("="*60)
print("\nGenerated files:")
print("  - visualizations/coverage_gap_altair.html")
print("  - visualizations/coverage_ratio_altair.html")
print("  - visualizations/policy_mix_altair.html")
print("  - visualizations/policy_mix_by_type_altair.html")
print("  - visualizations/expiring_units_timeline_altair.html")
print("  - visualizations/expiring_units_cumulative_altair.html")
print("  - visualizations/expiring_units_heatmap_altair.html")

